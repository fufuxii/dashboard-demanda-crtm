import os, re, time, csv, io
import requests, ibm_db, pandas as pd
from datetime import date
from scr.bd.conectar_bd import conectar_bd
from scr.logic.variables import SQL_QUERY


HOST = os.getenv("ZOS_HOST")
AUTH = (os.getenv("ZOS_UID"), os.getenv("ZOS_PASSWORD"))
H = {"X-CSRF-ZOSMF-HEADER": "true"}
PATRON_GENERACION = re.compile(r"G\d{4}V\d{2}")
COLUMNAS_ESPERADAS = {"SNAPSHOT", "TABLA", "NUM_FILAS", 
                      "FECHA_MIN", "FECHA_MAX"}
EXTRACTO = "TSOPSS1.PROYECTO.EXTRDATA"
GDG_HISTORICO = "TSOPSS1.PROYECTO.SNAPSHOT"
PDS_JCL = "TSOPSS1.PROYECTO.JCL"


def extraer_datos():
    '''Lee los metadatos de DEMANDA y CALENDARIO desde DB2
       y los devuelve como filas listas para escribir en CSV.'''

    conn = conectar_bd()
    hoy = str(date.today())

    filas = [["SNAPSHOT", "TABLA", "NUM_FILAS",
              "FECHA_MIN", "FECHA_MAX"]]

    stmt = ibm_db.exec_immediate(conn, SQL_QUERY)
    fila = ibm_db.fetch_tuple(stmt)

    while fila:
        filas.append([hoy] + [str(v) for v in fila])
        fila = ibm_db.fetch_tuple(stmt)

    ibm_db.close(conn)
    return filas


def subir_datos(filas):
    '''Convierte las filas a texto separado por ";" y las sube
       al dataset intermedio EXTRACTO (lo sobrescribe).'''

    buf = io.StringIO()
    csv.writer(buf, delimiter=";", lineterminator="\n").writerows(filas)

    r = requests.put(
        f"{HOST}/zosmf/restfiles/ds/{EXTRACTO}",
        auth=AUTH, verify=False,
        headers={**H, "Content-Type": "text/plain", "X-IBM-Data-Type": "text"},
        data=buf.getvalue().encode("utf-8"))
    r.raise_for_status()


def lanzar_miembro(miembro):
    '''Lanza un JCL guardado en z/OS, espera a que termine
       y devuelve el nombre del job, su id y el código de retorno.'''

    r = requests.put(
        f"{HOST}/zosmf/restjobs/jobs",
        auth=AUTH, verify=False,
        headers={**H, "Content-Type": "application/json"},
        json={"file": f"//'{PDS_JCL}({miembro})'"})
    job = r.json()
    nombre, jid = job["jobname"], job["jobid"]

    estado = {}
    while estado.get("status") != "OUTPUT":
        time.sleep(2)
        estado = requests.get(f"{HOST}/zosmf/restjobs/jobs/{nombre}/{jid}",
                              auth=AUTH, verify=False, headers=H).json()

    return nombre, jid, estado["retcode"]


def guardar_historico():
    '''Extrae los metadatos de DB2, los sube a z/OS y ejecuta
       el JCL que los copia como nueva generación del GDG.'''

    filas = extraer_datos()
    subir_datos(filas)

    nombre, jid, rc = lanzar_miembro("COPYDATA")
    print(f"{len(filas) - 1} tablas guardadas en el histórico ({rc}).")


def comprobar_respuesta(respuesta):
    '''Lanza un error con el detalle que devuelve z/OSMF si la petición falla.'''

    if not respuesta.ok:
        raise RuntimeError(
            f"z/OSMF respondió {respuesta.status_code}: "
            f"{respuesta.text[:300]}"
        )


def listar_generaciones():
    '''Devuelve los nombres de las generaciones del GDG,
       de la más antigua a la más reciente.'''

    for patron in (f"{GDG_HISTORICO}.G*", f"{GDG_HISTORICO}.*"):
        r = requests.get(
            f"{HOST}/zosmf/restfiles/ds",
            params={"dslevel": patron},
            auth=AUTH, verify=False, headers=H, timeout=30)
        comprobar_respuesta(r)

        nombres = [item["dsname"] for item in r.json().get("items", [])]
        generaciones = [
            nombre for nombre in nombres
            if PATRON_GENERACION.fullmatch(nombre.rsplit(".", 1)[-1])
        ]

        if generaciones:
            return sorted(generaciones)

    return []


def leer_generacion(nombre):
    '''Lee una generación del GDG y la devuelve como dataframe.'''

    r = requests.get(
        f"{HOST}/zosmf/restfiles/ds/{nombre}",
        auth=AUTH, verify=False, timeout=30,
        headers={**H, "X-IBM-Data-Type": "text"})
    comprobar_respuesta(r)

    lineas = [linea.strip() for linea in r.text.splitlines()]
    texto = "\n".join(linea for linea in lineas if linea)

    df = pd.read_csv(
        io.StringIO(texto), sep=r"[;\s]+", engine="python", dtype=str
    )

    if not COLUMNAS_ESPERADAS.issubset(df.columns):
        raise ValueError(
            f"{nombre} no tiene el formato esperado. "
            f"Columnas leídas: {list(df.columns)}"
        )

    df["GENERACION"] = nombre.rsplit(".", 1)[-1]

    return df


def preparar_historico(df):
    '''Convierte fechas y números a su tipo y ordena las filas.'''

    df = df.copy()

    df["SNAPSHOT"] = pd.to_datetime(df["SNAPSHOT"], errors="coerce")
    df["FECHA_MIN"] = pd.to_datetime(df["FECHA_MIN"], errors="coerce")
    df["FECHA_MAX"] = pd.to_datetime(df["FECHA_MAX"], errors="coerce")
    df["NUM_FILAS"] = pd.to_numeric(df["NUM_FILAS"], errors="coerce")

    return df.sort_values(["GENERACION", "TABLA"]).reset_index(drop=True)


def cargar_historico(limite=5):
    '''Lee las últimas generaciones del GDG y las junta en un dataframe.'''

    generaciones = listar_generaciones()[-limite:]

    if not generaciones:
        return pd.DataFrame()

    df = pd.concat(
        [leer_generacion(nombre) for nombre in generaciones],
        ignore_index=True,
    )

    return preparar_historico(df)