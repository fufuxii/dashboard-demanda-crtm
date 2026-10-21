import pandas as pd
from scr.logic.variables import TRANSPORTES


def preparar_datos(df_demanda, df_calendario):
    '''Une la demanda y el calendario mediante la fecha y
       crea un dataframe completo con la información de los dos.'''

    demanda = df_demanda.copy()
    calendario = df_calendario.copy()

    demanda["FECHA"] = pd.to_datetime(demanda["FECHA"])
    calendario["FECHA"] = pd.to_datetime(calendario["FECHA"])

    columnas_calendario = [
        "FECHA",
        "MES_NUM",
        "MES_NOMBRE",
        "ANIO_NUM",
        "ES_FESTIVO",
        "ES_FIN_DE_SEMANA",
    ]

    calendario = calendario[columnas_calendario]

    # validate evita duplicar filas de demanda si el calendario
    # tuviera una fecha repetida.
    df = demanda.merge(
        calendario,
        on="FECHA",
        how="left",
        validate="many_to_one",
    )

    return df


def filtrar_por_anio(df, anio):
    '''Filtra los registros de un año concreto.'''

    return df[df["FECHA"].dt.year == anio]


def filtrar_por_mes(df, mes=None):
    '''Filtra un mes y, si mes es None, conserva todos los meses.'''

    if mes is None:
        return df

    return df[df["FECHA"].dt.month == mes]


def filtrar_por_tipo_dia(df, tipo_dia="TODOS"):
    '''Tipos de día: TODOS, FESTIVOS, FINES_SEMANA, LABORABLES.'''

    tipo_dia = tipo_dia.upper()

    if tipo_dia == "TODOS":
        return df

    if tipo_dia == "FESTIVOS":
        return df[df["ES_FESTIVO"] == "S"]

    if tipo_dia == "FINES_SEMANA":
        return df[df["ES_FIN_DE_SEMANA"] == "S"]

    # Laborable: ni fin de semana ni festivo.
    if tipo_dia == "LABORABLES":
        return df[
            (df["ES_FIN_DE_SEMANA"] == "N")
            & (df["ES_FESTIVO"] == "N")
        ]

    raise ValueError(f"Tipo de día no válido: {tipo_dia}")


def obtener_transporte(transporte="TODOS"):
    '''Devuelve la columna de demanda que se debe analizar.'''

    transporte = transporte.upper()

    # La columna TOTAL ya suma todos los transportes.
    if transporte == "TODOS":
        return "TOTAL"

    if transporte not in TRANSPORTES:
        raise ValueError(f"Transporte no válido: {transporte}")

    return transporte


def aplicar_filtros(df, anio, mes=None, tipo_dia="TODOS"):
    '''Aplica los filtros temporales y de tipo de día.'''

    resultado = filtrar_por_anio(df, anio)
    resultado = filtrar_por_mes(resultado, mes)
    resultado = filtrar_por_tipo_dia(resultado, tipo_dia)

    return resultado


def calcular_demanda_global(
    df, anio, mes=None, transporte="TODOS", tipo_dia="TODOS"
):
    '''Calcula indicadores generales del periodo seleccionado.'''

    datos = aplicar_filtros(df, anio, mes, tipo_dia)
    columna = obtener_transporte(transporte)

    if datos.empty:
        return {
            "viajes_totales": 0,
            "media_diaria": 0,
            "pico_diario": 0,
            "fecha_pico": None,
        }

    # idxmax localiza la fila del día con más viajes (el pico).
    idx_maximo = datos[columna].idxmax()

    return {
        "viajes_totales": datos[columna].sum(),
        "media_diaria": datos[columna].mean(),
        "pico_diario": datos.loc[idx_maximo, columna],
        "fecha_pico": datos.loc[idx_maximo, "FECHA"],
    }


def calcular_demanda_por_mes(df, anio, transporte="TODOS", tipo_dia="TODOS"):
    """Calcula los viajes acumulados de cada mes."""

    datos = aplicar_filtros(df, anio, tipo_dia=tipo_dia)
    columna = obtener_transporte(transporte)

    # Se suman los viajes de todos los días de cada mes.
    resultado = (
        datos.groupby(["MES_NUM", "MES_NOMBRE"], as_index=False)[columna]
        .sum()
        .rename(columns={columna: "VIAJES"})
        .sort_values("MES_NUM")
    )

    return resultado


def calcular_demanda_por_transporte(df, anio, mes=None, tipo_dia="TODOS"):
    """Calcula el reparto de viajes entre los transportes."""

    datos = aplicar_filtros(df, anio, mes, tipo_dia)

    # TODOS solo sirve para filtrar: no es una columna de demanda.
    transportes = [t for t in TRANSPORTES if t != "TODOS"]
    viajes = datos[transportes].sum()

    return pd.DataFrame({
        "TRANSPORTE": viajes.index,
        "VIAJES": viajes.values,
    })


def calcular_demanda_diaria(
    df, anio, mes=None, transporte="TODOS", tipo_dia="TODOS"
):
    '''Devuelve la evolución diaria del periodo seleccionado.'''

    datos = aplicar_filtros(df, anio, mes, tipo_dia)
    columna = obtener_transporte(transporte)

    return (
        datos[["FECHA", columna]]
        .rename(columns={columna: "VIAJES"})
        .sort_values("FECHA")
        .reset_index(drop=True)
    )