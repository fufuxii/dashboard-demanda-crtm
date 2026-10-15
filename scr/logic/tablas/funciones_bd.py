import ibm_db
import pandas as pd
from pathlib import Path
from scr.logic.tablas.variables import TABLAS
from scr.bd.conectar_bd import conectar_bd


def leer_csv(nombre_archivo, tabla):
    '''Limpia los datos de las tablas que están en formato CSV.'''

    ruta = Path("data") / nombre_archivo

    # Convertir los datos del CSV a un dataframe
    df = pd.read_csv(ruta, dtype=str, keep_default_na=False)
    columnas_csv = tabla["columnas_csv"]
    df = df[columnas_csv].copy()

    # Convertir cadenas vacías en nulos
    df = df.replace(r"^\s*$", None, regex=True)

    # Convertir la fecha a formato ISO
    df["fecha"] = pd.to_datetime(
        df["fecha"],
        format="%d-%m-%Y",
        errors="raise"
    ).dt.strftime("%Y-%m-%d")

    # Convertir las columnas numéricas a enteros
    for columna in tabla.get("columnas_numericas", []):
        valores = df[columna].str.replace(".", "", regex=False)
        df[columna] = pd.to_numeric(
            valores, errors="raise"
        ).astype("Int64")

    # Convertir los nulos a None para DB2
    df = df.astype(object).where(pd.notna(df), None)

    return df


def crear_query(nombre_tabla, columnas_db):
    '''Crea la consulta base SQL con el operador INSERT.'''

    valores = []

    # Los "?" indican la posición de los valores
    for columna in columnas_db:
        if columna == "FECHA":
            valores.append("CAST(? AS DATE)")
        else:
            valores.append("?")

    # Creación de la consulta
    columnas = ", ".join(columnas_db)
    valores_sql = ", ".join(valores)
    consulta = (
        f"INSERT INTO {nombre_tabla} "
        f"({columnas}) VALUES ({valores_sql})"
    )

    return consulta


def ejecutar_query(conn, sql, datos):
    '''Ejecuta la consulta SQL mediante la conexión con IBM.'''

    # Preparar la consulta SQL
    query = ibm_db.prepare(conn, sql)
    if query is False:
        raise RuntimeError(
            f"Error preparando SQL: {ibm_db.stmt_errormsg()}"
        )

    # Insertar cada fila del dataFrame
    for fila in datos.itertuples(index=False, name=None):
        resultado = ibm_db.execute(query, fila)
        if resultado is False:
            raise RuntimeError(
                f"Error insertando registro: {ibm_db.stmt_errormsg()}"
            )

    # Devolver el número de registros procesados para
    # saber que se han insertado las filas esperadas
    return len(datos)


def insertar_datos_en_db2(nombre_archivo, nombre_tabla):
    '''Llama a las funciones leer_csv, crear_query y ejecutar_query
       para insertar los datos en DB2.'''

    # Revisar si la tabla existe para continuar el proceso
    if nombre_tabla not in TABLAS:
        raise ValueError(f"Tabla no configurada: {nombre_tabla}")

    tabla = TABLAS[nombre_tabla]
    columnas_db = tabla["columnas_db"]

    datos = leer_csv(nombre_archivo, tabla)
    sql = crear_query(nombre_tabla, columnas_db)
    
    conn = None

    try:
        conn = conectar_bd()
        total_filas_insertadas = ejecutar_query(conn, sql, datos)
        ibm_db.commit(conn) # Confirmar cambios en la bd

        print(
            f"{nombre_tabla}: "
            f"{total_filas_insertadas} registros insertados correctamente."
        )

    except Exception as e:
        # Deshacer cambios pendientes si hay error
        if conn is not None: 
            ibm_db.rollback(conn) 
        print(f"ERROR insertando en {nombre_tabla}:", e)
        raise

    finally:
        # Cerrar conexión tanto si hay error como si no
        if conn is not None: 
            ibm_db.close(conn)