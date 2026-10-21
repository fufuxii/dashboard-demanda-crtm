import csv
import io
import os
import re
import time
import pandas as pd
import requests
from datetime import date
from scr.bd.consultas import ejecutar_consulta
from scr.logic.variables import (
    SQL_QUERY, EXTRACTO, GDG_HISTORICO, PDS_JCL,
    COLUMNAS_HISTORICO, GENERACIONES_RECIENTES,
)


HOST = os.getenv("ZOS_HOST")
AUTH = (os.getenv("ZOS_UID"), os.getenv("ZOS_PASSWORD"))
H = {"X-CSRF-ZOSMF-HEADER": "true"}
PATRON_GENERACION = re.compile(r"G\d{4}V\d{2}")


def solicitar(metodo, ruta, headers=None, **kwargs):
    '''Envía una petición a z/OSMF y lanza un error con su detalle si falla.'''

    r = requests.request(
        metodo, f"{HOST}/zosmf{ruta}",
        auth=AUTH, verify=False, timeout=30,
        headers={**H, **(headers or {})}, **kwargs)

    if not r.ok:
        raise RuntimeError(f"z/OSMF respondió {r.status_code}: {r.text[:300]}")

    return r


def extraer_datos():
    '''Lee los metadatos de DEMANDA y CALENDARIO desde DB2
       y los devuelve como filas listas para escribir en CSV.'''

    hoy = str(date.today())
    filas = [COLUMNAS_HISTORICO]

    for fila in ejecutar_consulta(SQL_QUERY):
        filas.append([hoy] + [str(v) for v in fila.values()])

    return filas


def subir_datos(filas):
    '''Convierte las filas a texto separado por ";" y las sube
       al dataset intermedio EXTRACTO (lo sobrescribe).'''

    buf = io.StringIO()
    csv.writer(buf, delimiter=";", lineterminator="\n").writerows(filas)

    solicitar(
        "PUT", f"/restfiles/ds/{EXTRACTO}",
        headers={"Content-Type": "text/plain", "X-IBM-Data-Type": "text"},
        data=buf.getvalue().encode("utf-8"))


def lanzar_miembro(miembro):
    '''Lanza un JCL guardado en z/OS, espera a que termine
       y devuelve el nombre del job, su id y el código de retorno.'''

    r = solicitar(
        "PUT", "/restjobs/jobs",
        headers={"Content-Type": "application/json"},
        json={"file": f"//'{PDS_JCL}({miembro})'"})
    job = r.json()
    nombre, jid = job["jobname"], job["jobid"]

    # Se consulta el estado cada 2 s, hasta un máximo de 2 minutos.
    for _ in range(60):
        time.sleep(2)
        estado = solicitar("GET", f"/restjobs/jobs/{nombre}/{jid}").json()

        if estado["status"] == "OUTPUT":
            return nombre, jid, estado["retcode"]

    raise TimeoutError(f"El job {nombre} ({jid}) no terminó a tiempo.")


def guardar_historico():
    '''Extrae los metadatos de DB2, los sube a z/OS y ejecuta
       el JCL que los copia como nueva generación del GDG.'''

    filas = extraer_datos()
    subir_datos(filas)

    nombre, jid, rc = lanzar_miembro("COPYDATA")

    # Si el JCL falla no se crea la generación: no debe darse por buena.
    if rc != "CC 0000":
        raise RuntimeError(f"El job {nombre} ({jid}) terminó con {rc}.")

    print(f"{len(filas) - 1} tablas guardadas en el histórico ({rc}).")


def listar_generaciones():
    '''Devuelve los nombres de las generaciones del GDG,
       de la más antigua a la más reciente.'''

    r = solicitar(
        "GET", "/restfiles/ds",
        params={"dslevel": f"{GDG_HISTORICO}.*"})
    nombres = [item["dsname"] for item in r.json().get("items", [])]

    # Se descarta el nombre base del GDG y se dejan solo las generaciones.
    generaciones = [
        nombre for nombre in nombres
        if PATRON_GENERACION.fullmatch(nombre.rsplit(".", 1)[-1])
    ]

    return sorted(generaciones)


def leer_generacion(nombre):
    '''Lee una generación del GDG y la devuelve como dataframe.'''

    r = solicitar(
        "GET", f"/restfiles/ds/{nombre}",
        headers={"X-IBM-Data-Type": "text"})

    # El JCL deja las columnas alineadas con espacios (registros de
    # longitud fija), así que se separa por espacios o por ";".
    lineas = [linea.strip() for linea in r.text.splitlines()]

    df = pd.read_csv(
        io.StringIO("\n".join(lineas)),
        sep=r"[;\s]+", engine="python", dtype=str,
    )

    if not set(COLUMNAS_HISTORICO).issubset(df.columns):
        raise ValueError(
            f"{nombre} no tiene el formato esperado. "
            f"Columnas leídas: {list(df.columns)}"
        )

    df["GENERACION"] = nombre.rsplit(".", 1)[-1]

    return df


def preparar_historico(df):
    '''Convierte fechas y números a su tipo y ordena las filas.'''

    df = df.copy()

    for columna in ("SNAPSHOT", "FECHA_MIN", "FECHA_MAX"):
        df[columna] = pd.to_datetime(df[columna], errors="coerce")

    df["NUM_FILAS"] = pd.to_numeric(df["NUM_FILAS"], errors="coerce")

    return df.sort_values(["GENERACION", "TABLA"]).reset_index(drop=True)


def preparar_tabla_historial(df_historial):
    '''Devuelve una fila por generación con los datos de cada tabla en columnas.'''

    resultado = (
        df_historial[["GENERACION", "SNAPSHOT"]]
        .drop_duplicates(subset="GENERACION")
    )

    for tabla in df_historial["TABLA"].unique():
        datos = df_historial.loc[
            df_historial["TABLA"] == tabla,
            ["GENERACION", "NUM_FILAS", "FECHA_MIN", "FECHA_MAX"],
        ].rename(columns={
            "NUM_FILAS": f"Filas {tabla}",
            "FECHA_MIN": f"{tabla}: desde",
            "FECHA_MAX": f"{tabla}: hasta",
        })

        resultado = resultado.merge(datos, on="GENERACION", how="left")

    return resultado.sort_values("GENERACION", ascending=False)


def cargar_historico(limite=GENERACIONES_RECIENTES):
    '''Lee las últimas generaciones del GDG y las junta en un dataframe.'''

    generaciones = listar_generaciones()[-limite:]

    if not generaciones:
        return pd.DataFrame()

    df = pd.concat(
        [leer_generacion(nombre) for nombre in generaciones],
        ignore_index=True,
    )

    return preparar_historico(df)