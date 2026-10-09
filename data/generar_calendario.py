import pandas as pd

# Archivos
ARCHIVO_FESTIVOS = "data/festivos-23-26.xlsx"
ARCHIVO_SALIDA = "data/calendario.csv"

# Fechas
FECHA_INICIO = "2023-01-01"
FECHA_FIN = "2026-12-31"


# -----------------------------------
# 1. CREAR TODAS LAS FECHAS
# -----------------------------------

fechas = pd.date_range(
    start=FECHA_INICIO,
    end=FECHA_FIN,
    freq="D"
)

calendario = pd.DataFrame({
    "FECHA": fechas
})

# -----------------------------------
# 2. INFORMACIÓN DE LA FECHA
# -----------------------------------

dias_semana = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
    6: "Domingo"
}

meses = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre"
}

calendario["DIA_SEMANA"] = calendario["FECHA"].dt.dayofweek.map(dias_semana)
calendario["NUM_DIA_SEMANA"] = calendario["FECHA"].dt.dayofweek + 1

calendario["DIA"] = calendario["FECHA"].dt.day
calendario["MES"] = calendario["FECHA"].dt.month
calendario["NOMBRE_MES"] = calendario["MES"].map(meses)

calendario["TRIMESTRE"] = calendario["FECHA"].dt.quarter
calendario["AÑO"] = calendario["FECHA"].dt.year

# -----------------------------------
# 3. FIN DE SEMANA
# -----------------------------------

calendario["FIN_DE_SEMANA"] = calendario["FECHA"].dt.dayofweek >= 5

calendario["FIN_DE_SEMANA"] = calendario["FIN_DE_SEMANA"].map({
    True: "Sí",
    False: "No"
})

# -----------------------------------
# 4. LEER FESTIVOS
# -----------------------------------

festivos = pd.read_excel(ARCHIVO_FESTIVOS)

festivos["FECHA"] = pd.to_datetime(
    festivos["FECHA"],
    dayfirst=True
)

festivos = festivos.rename(
    columns={"FESTIVO": "NOMBRE_FESTIVO"}
)

# -----------------------------------
# 5. CRUZAR CALENDARIO CON FESTIVOS
# -----------------------------------

calendario = calendario.merge(
    festivos,
    on="FECHA",
    how="left"
)

# -----------------------------------
# 6. INDICAR SI ES FESTIVO
# -----------------------------------

calendario["ES_FESTIVO"] = calendario["NOMBRE_FESTIVO"].notna().map({
    True: "Sí",
    False: "No"
})

# -----------------------------------
# 7. ORDENAR COLUMNAS
# -----------------------------------

calendario = calendario[
    [
        "FECHA",
        "DIA_SEMANA",
        "NUM_DIA_SEMANA",
        "DIA",
        "MES",
        "NOMBRE_MES",
        "TRIMESTRE",
        "AÑO",
        "FIN_DE_SEMANA",
        "ES_FESTIVO",
        "NOMBRE_FESTIVO"
    ]
]

# -----------------------------------
# 8. GUARDAR CSV
# -----------------------------------

calendario["FECHA"] = calendario["FECHA"].dt.strftime("%d-%m-%Y")

calendario.to_csv(
    ARCHIVO_SALIDA,
    index=False,
    encoding="utf-8-sig"
)

print(f"Calendario creado correctamente: {ARCHIVO_SALIDA}")