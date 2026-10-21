import streamlit as st
from scr.bd.consultas import obtener_datos_de_db2
from scr.logic.metricas import (
    preparar_datos,
    calcular_demanda_global,
    calcular_demanda_por_mes,
    calcular_demanda_diaria,
    calcular_demanda_por_transporte,
)
from scr.logic.elementos import (
    crear_grafico_demanda_mensual,
    crear_grafico_demanda_diaria,
    crear_grafico_demanda_por_transporte,
)
from scr.logic.tarjetas import mostrar_fila_tarjetas
from scr.logic.variables import (
    MESES, TRANSPORTES, TIPOS_DIA, VISTAS, TIPOS_GRAFICO,
)


@st.cache_data(ttl=3600, show_spinner="Cargando datos...")
def cargar_datos():
    '''Carga las tablas de DB2 y prepara los datos.'''

    df_demanda = obtener_datos_de_db2("DEMANDA")
    df_calendario = obtener_datos_de_db2("CALENDARIO")

    if df_demanda.empty or df_calendario.empty:
        return None

    print("Tablas DEMANDA y CALENDARIO cargadas correctamente.")

    return preparar_datos(df_demanda, df_calendario)


def seleccionar_mes(df, anio, activo=True):
    '''Pide el mes entre los disponibles; queda desactivado en la vista global.'''

    meses_disponibles = sorted(
        df.loc[df["ANIO_NUM"] == anio, "MES_NUM"]
        .dropna()
        .astype(int)
        .unique()
        .tolist()
    )

    if not meses_disponibles:
        if activo:
            st.warning("No hay meses disponibles para este año.")
        return None

    mes = st.selectbox(
        "Mes",
        options=meses_disponibles,
        format_func=lambda x: MESES[x],
        disabled=not activo,
    )

    return mes if activo else None


def mostrar_filtros(df):
    '''Muestra los filtros en una barra superior y devuelve las selecciones.'''

    anios = sorted(df["ANIO_NUM"].dropna().astype(int).unique().tolist())

    if not anios:
        st.warning("No hay años disponibles.")
        return None

    with st.container(border=True):
        columnas = st.columns([1, 1.1, 1.5, 1.5, 1.9, 1.5])

        # La vista se lee antes que el mes porque decide si el mes se activa.
        vista = columnas[4].radio("Vista", options=VISTAS, horizontal=True)
        tipo_grafico = columnas[5].radio(
            "Tipo de gráfico",
            options=TIPOS_GRAFICO,
            horizontal=True,
        )

        anio = columnas[0].selectbox(
            "Año",
            options=anios,
            index=len(anios) - 1,
        )

        with columnas[1]:
            mes = seleccionar_mes(df, anio, vista == "Detalle mensual")

        transporte = columnas[2].selectbox(
            "Transporte",
            options=list(TRANSPORTES),
            format_func=TRANSPORTES.get,
        )

        tipo_dia = columnas[3].selectbox(
            "Tipo de día",
            options=list(TIPOS_DIA),
            format_func=TIPOS_DIA.get,
        )

    if vista == "Detalle mensual" and mes is None:
        return None

    return {
        "anio": anio,
        "transporte": transporte,
        "tipo_dia": tipo_dia,
        "vista": vista,
        "mes": mes,
        "tipo_grafico": tipo_grafico,
    }


def mostrar_grafico_global(df, filtros):
    '''Muestra los viajes acumulados de cada mes.'''

    df_grafico = calcular_demanda_por_mes(
        df,
        anio=filtros["anio"],
        transporte=filtros["transporte"],
        tipo_dia=filtros["tipo_dia"],
    )

    if df_grafico.empty:
        st.info("No hay datos para los filtros seleccionados.")
    else:
        fig = crear_grafico_demanda_mensual(
            df_grafico,
            filtros["anio"],
            filtros["transporte"],
            filtros["tipo_grafico"],
        )
        st.plotly_chart(fig, width="stretch")

    return df_grafico


def mostrar_grafico_mensual(df, filtros):
    '''Muestra los viajes de cada día del mes seleccionado.'''

    df_grafico = calcular_demanda_diaria(
        df,
        anio=filtros["anio"],
        mes=filtros["mes"],
        transporte=filtros["transporte"],
        tipo_dia=filtros["tipo_dia"],
    )

    if df_grafico.empty:
        st.info("No hay datos para los filtros seleccionados.")
    else:
        fig = crear_grafico_demanda_diaria(
            df_grafico,
            filtros["anio"],
            filtros["mes"],
            filtros["transporte"],
            filtros["tipo_grafico"],
        )
        st.plotly_chart(fig, width="stretch")

    return df_grafico


def mostrar_grafico_transportes(df, filtros):
    '''Muestra el reparto de viajes entre los transportes.'''

    df_transporte = calcular_demanda_por_transporte(
        df,
        anio=filtros["anio"],
        mes=filtros["mes"],
        tipo_dia=filtros["tipo_dia"],
    )

    fig = crear_grafico_demanda_por_transporte(
        df_transporte, filtros["anio"], filtros["mes"]
    )

    st.plotly_chart(fig, width="stretch")


def mostrar_tarjetas(df, df_grafico, filtros):
    '''Muestra en una sola fila los indicadores del periodo.'''

    resumen = calcular_demanda_global(
        df,
        anio=filtros["anio"],
        mes=filtros["mes"],
        transporte=filtros["transporte"],
        tipo_dia=filtros["tipo_dia"],
    )

    datos = df_grafico.dropna(subset=["VIAJES"])
    maximo = datos.loc[datos["VIAJES"].idxmax()]
    minimo = datos.loc[datos["VIAJES"].idxmin()]

    tarjetas = [
        ("Viajes acumulados", f"{resumen['viajes_totales']:,.0f}", None),
        ("Media diaria", f"{resumen['media_diaria']:,.0f}", None),
    ]

    # En la vista global el máximo y el mínimo son meses; en el detalle,
    # días. Por eso solo la vista global añade la tarjeta del pico diario.
    if filtros["vista"] == "Global":
        tarjetas.append((
            "Pico diario",
            f"{resumen['pico_diario']:,.0f}",
            resumen["fecha_pico"].strftime("%d/%m/%Y"),
        ))
        unidad = "Mes"
        nombre_maximo = maximo["MES_NOMBRE"]
        nombre_minimo = minimo["MES_NOMBRE"]
    else:
        unidad = "Día"
        nombre_maximo = maximo["FECHA"].strftime("%d/%m/%Y")
        nombre_minimo = minimo["FECHA"].strftime("%d/%m/%Y")

    tarjetas += [
        (f"{unidad} con más viajes", f"{maximo['VIAJES']:,.0f}", nombre_maximo),
        (f"{unidad} con menos viajes", f"{minimo['VIAJES']:,.0f}", nombre_minimo),
    ]

    mostrar_fila_tarjetas(tarjetas)


def mostrar_resultados(df, filtros):
    '''Muestra las tarjetas y los gráficos del periodo seleccionado.'''

    # Las tarjetas van arriba pero se rellenan al final, porque
    # dependen de los datos del gráfico.
    zona_tarjetas = st.container()
    columna_principal, columna_transportes = st.columns([2, 1])

    with columna_principal:
        if filtros["vista"] == "Global":
            df_grafico = mostrar_grafico_global(df, filtros)
        else:
            df_grafico = mostrar_grafico_mensual(df, filtros)

    if df_grafico.empty:
        return

    with columna_transportes:
        mostrar_grafico_transportes(df, filtros)

    with zona_tarjetas:
        mostrar_tarjetas(df, df_grafico, filtros)


def mostrar_dashboard():
    '''Muestra los filtros y los resultados de la demanda.'''

    df = cargar_datos()

    if df is None:
        st.warning("No hay datos disponibles en la base de datos.")
        return

    filtros = mostrar_filtros(df)

    if filtros is not None:
        mostrar_resultados(df, filtros)