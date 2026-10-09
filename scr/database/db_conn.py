import os
import ibm_db
from dotenv import load_dotenv

print("Conectando...")

load_dotenv()
NAME = os.getenv("DB_NAME")
HOSTNAME = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
PROTOCOL = os.getenv("DB_PROTOCOL")
USER = os.getenv("DB_UID")
PASSWORD = os.getenv("DB_PASSWORD")

conn_str = (
    f"DATABASE={NAME};"
    f"HOSTNAME={HOSTNAME};"
    f"PORT={PORT};"
    f"PROTOCOL={PROTOCOL};"
    f"UID={USER};"
    f"PWD={PASSWORD};"
)

try:
    conn = ibm_db.connect(conn_str, "", "")
    print("Conectado correctamente")

    sql = """
        SELECT *    
        FROM TSOPSS1.EMPLEADO
        --FETCH FIRST 10 ROWS ONLY
    """

    print("Ejecutando:", sql)

    stmt = ibm_db.exec_immediate(conn, sql)

    if stmt is False:
        print("ERROR ejecutando SELECT:")
        print(ibm_db.stmt_errormsg())
    else:
        print("SELECT ejecutado correctamente")

        filas = 0

        while True:
            row = ibm_db.fetch_assoc(stmt)

            if row is False:
                break

            print("Fila:", row)
            filas += 1

        print("Total filas:", filas)

    ibm_db.close(conn)

except Exception as e:
    print("ERROR DE CONEXIÓN:")
    print(e)