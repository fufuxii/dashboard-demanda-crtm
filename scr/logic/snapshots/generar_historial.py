import time, csv, io, requests, ibm_db
from datetime import date
from scr.bd.conectar_bd import conectar_bd
from scr.logic.snapshots.variables import (
    HOST, AUTH, H, EXTRACTO, PDS_JCL, SQL
)


def extraer_datos():
    '''Lee los metadatos de DEMANDA y CALENDARIO desde DB2
       y los devuelve como filas listas para escribir en CSV.'''

    conn = conectar_bd()
    hoy = str(date.today())

    filas = [["SNAPSHOT", "TABLA", "NUM_FILAS",
              "FECHA_MIN", "FECHA_MAX"]]

    stmt = ibm_db.exec_immediate(conn, SQL)
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