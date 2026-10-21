import io, requests
import pandas as pd
from scr.logic.snapshots.variables import (
    HOST, AUTH, H, GDG_HISTORICO,
    PATRON_GENERACION, COLUMNAS_ESPERADAS
)


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