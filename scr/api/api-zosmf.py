import os
import requests
import urllib3
from dotenv import load_dotenv
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
url = os.getenv("ZOS_LINK")
usuario = os.getenv("ZOS_UID")
password = os.getenv("ZOS_PASSWORD")

# Cabeceras requeridas por la API de z/OSMF
cabeceras = {
    "X-IBM-Max-Items": "0"
}

# Ejecutar la petición GET
response = requests.get(
    url, 
    auth=(usuario, password), 
    headers=cabeceras, 
    verify=False
)

# Procesar y mostrar la respuesta
if response.status_code == 200:
    datos_json = response.json()
    print("Datasets encontrados:")
    print("-" * 25)
    for item in datos_json.get("items", []):
        print(item.get("dsname"))
else:
    print(f"Fallo en la conexión. Código HTTP: {response.status_code}")
    print(response.text)