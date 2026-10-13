import pandas as pd

# Archivos
archivo_festivos = "data/calendario-festivos-23-26.xlsx"
archivo_salida = "data/calendario.csv"

# fechas
fecha_inicio = "2023-01-01"
fecha_fin = "2026-12-31"

# -------------------------------------
# CONSTRUCCIÓN DEL CSV DE CALENDARIO
# Se añade información de la fecha.
# -------------------------------------

# PASO 1: Crear todas las fechas

fechas = pd.date_range(
    start=fecha_inicio,
    end=fecha_fin,
    freq="D"
)

calendario = pd.DataFrame({
    "fecha": fechas
})

# PASO 2: Información de la fecha

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

calendario["dia_semana_nombre"] = calendario["fecha"].dt.dayofweek.map(dias_semana)
calendario["dia_semana_num"] = calendario["fecha"].dt.dayofweek + 1

calendario["dia_mes_num"] = calendario["fecha"].dt.day
calendario["mes_num"] = calendario["fecha"].dt.month
calendario["mes_nombre"] = calendario["mes_num"].map(meses)

calendario["trimestre_num"] = calendario["fecha"].dt.quarter
calendario["anio_num"] = calendario["fecha"].dt.year

# PASO 3: Días del fin de semana

calendario["es_fin_de_semana"] = calendario["fecha"].dt.dayofweek >= 5

calendario["es_fin_de_semana"] = calendario["es_fin_de_semana"].map({
    True: "S",
    False: "N"
})

# PASO 4: Información de los festivos

festivos = pd.read_excel(archivo_festivos)

festivos["fecha"] = pd.to_datetime(
    festivos["fecha"],
    dayfirst=True
)

festivos = festivos.rename(
    columns={"festivo": "festivo_nombre"}
)

# PASO 5: Cruzar calendario con festivos

calendario = calendario.merge(
    festivos,
    on="fecha",
    how="left"
)

# PASO 6: Indicar si es festivo

calendario["es_festivo"] = calendario["festivo_nombre"].notna().map({
    True: "S",
    False: "N"
})

# PASO 7: Ordenar calendario

calendario = calendario[
    [
        "fecha",
        "dia_semana_nombre",
        "dia_semana_num",
        "dia_mes_num",
        "mes_num",
        "mes_nombre",
        "trimestre_num",
        "anio_num",
        "es_fin_de_semana",
        "es_festivo",
        "festivo_nombre"
    ]
]

# PASO 8: Crear el archivo csv

calendario["fecha"] = calendario["fecha"].dt.strftime("%d-%m-%Y")

calendario.to_csv(
    archivo_salida,
    index=False,
    encoding="utf-8-sig"
)

print(f"CSV creado correctamente: {archivo_salida}")