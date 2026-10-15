import pandas as pd
import ibm_db
from scr.bd.conectar_bd import conectar_bd


def obtener_datos(tabla):
    """Obtiene los datos de demanda desde DB2."""

    conn = conectar_bd()

    try:
        consulta = f"""
            SELECT *
            FROM {tabla}
            ORDER BY FECHA
        """
        
        resultado = ibm_db.exec_immediate(conn, consulta)

        # Recuperar todas las filas y juntarlas
        filas = []
        fila = ibm_db.fetch_assoc(resultado)
        while fila:
            filas.append(fila)
            fila = ibm_db.fetch_assoc(resultado)

        # Convertir los resultados a dataFrame
        df = pd.DataFrame(filas)

        return df

    finally:
        # Cerrar conexión tanto si hay error como si no
        if conn is not None:
            ibm_db.close(conn)