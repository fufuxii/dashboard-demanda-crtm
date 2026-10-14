import pandas as pd

# Archivos
archivo_entrada = "data/demanda_diaria_crtm.xlsx"
archivo_salida = "data/demanda.csv"

# Leer Excel
demanda = pd.read_excel(archivo_entrada)

# -------------------------------------
# CONSTRUCCIÓN DEL CSV DE DEMANDA
# Se convierte el Excel a CSV.
# -------------------------------------

# Convertir fechas al formato DD-MM-YYYY
demanda["fecha"] = pd.to_datetime(
    demanda["fecha"],
    dayfirst=True
).dt.strftime("%d-%m-%Y")

# Convertir a números enteros
columnas_numericas = [
    "metro",
    "emt",
    "carretera",
    "renfe",
    "total"
]

for columna in columnas_numericas:
    demanda[columna] = (
        demanda[columna]
        .astype(str)
        .str.replace(".", "", regex=False)
        .astype("int64")
    )

# Guardar CSV
demanda.to_csv(
    archivo_salida,
    index=False,
    encoding="utf-8-sig"
)

print(f"CSV creado correctamente: {archivo_salida}")