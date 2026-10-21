import ibm_db
import pandas as pd
from scr.bd.conexion import conectar_bd


def ejecutar_consulta(consulta):
    '''Ejecuta una consulta en DB2 y devuelve las filas como diccionarios.'''

    conn = conectar_bd()

    try:
        resultado = ibm_db.exec_immediate(conn, consulta)

        # Recuperar todas las filas y juntarlas
        filas = []
        fila = ibm_db.fetch_assoc(resultado)
        while fila:
            filas.append(fila)
            fila = ibm_db.fetch_assoc(resultado)

        return filas

    finally:
        # Cerrar conexión tanto si hay error como si no
        ibm_db.close(conn)


def obtener_datos_de_db2(tabla):
    """Obtiene los datos de demanda desde DB2."""

    consulta = f"SELECT * FROM {tabla} ORDER BY FECHA"

    # Convertir los resultados a dataframe
    return pd.DataFrame(ejecutar_consulta(consulta))