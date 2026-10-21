ALTURA_GRAFICO = 320

GENERACIONES_RECIENTES = 5

VISTAS = ["Global", "Detalle mensual"]

TIPOS_GRAFICO = ["Barras", "Líneas"]

TIPOS_DIA = {
    "TODOS": "Todos los días",
    "FESTIVOS": "Festivos",
    "FINES_SEMANA": "Fines de semana",
    "LABORABLES": "Laborables no festivos",
}

TRANSPORTES = {
    "TODOS": "Todos los transportes",
    "METRO": "Metro",
    "EMT": "EMT",
    "CARRETERA": "Carretera",
    "RENFE": "Renfe",
}

MESES = {
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
    12: "Diciembre",
}

EXTRACTO = "TSOPSS1.PROYECTO.EXTRDATA"

GDG_HISTORICO = "TSOPSS1.PROYECTO.SNAPSHOT"

PDS_JCL = "TSOPSS1.PROYECTO.JCL"

COLUMNAS_HISTORICO = [
    "SNAPSHOT", "TABLA", "NUM_FILAS", "FECHA_MIN", "FECHA_MAX",
]

SQL_QUERY = """
SELECT 'DEMANDA' AS TABLA, COUNT(*) AS NUM_DIAS,
       MIN(FECHA) AS FECHA_MIN, MAX(FECHA) AS FECHA_MAX
FROM DEMANDA
UNION ALL
SELECT 'CALENDARIO', COUNT(*),
       MIN(FECHA), MAX(FECHA)
FROM CALENDARIO
"""