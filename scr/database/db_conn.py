import os
import ibm_db
from dotenv import load_dotenv

load_dotenv()
# Extraer datos de conexión
NAME = os.getenv("DB_NAME")
HOSTNAME = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
PROTOCOL = os.getenv("DB_PROTOCOL")
USER = os.getenv("DB_UID")
PASSWORD = os.getenv("DB_PASSWORD")

def conectar_bd():
    print("Conectando a la bd...")

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
        print("Conectado a la bd correctamente.")
        return conn

    except Exception as e:
        print("Error al conectar la bd:", e)
        raise