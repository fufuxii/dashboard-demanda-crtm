import ibm_db, pandas as pd, streamlit as st
from scr.bd.conectar_bd import conectar_bd
from scr.logic.historial import cargar_historico, guardar_historico
from scr.logic.estilos import aplicar_estilo_interfaz
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
from scr.logic.variables import (
    MESES, TRANSPORTES, TIPOS_DIA, VISTAS, 
    TIPOS_GRAFICO, GENERACIONES_RECIENTES,
)


def obtener_datos_de_db2(tabla):
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

        # Convertir los resultados a dataframe
        df = pd.DataFrame(filas)

        return df

    finally:
        # Cerrar conexión tanto si hay error como si no
        if conn is not None:
            ibm_db.close(conn)


def configurar_pagina():
    '''Configura la página y aplica los estilos.'''

    st.set_page_config(
        page_title="Dashboard CRTM",
        page_icon="🚌",
        layout="wide",
    )

    aplicar_estilo_interfaz()


def mostrar_cabecera():
    '''Muestra el banner con el título del dashboard.'''

    st.markdown(
        """
        <div class="crtm-banner">
            <h1>Demanda del transporte público de Madrid</h1>
            <p>
                Análisis de la demanda por transporte de cada año (2023-2026)
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(ttl=3600, show_spinner="Cargando datos...")
def cargar_datos():
    '''Carga las tablas de DB2 y prepara los datos.'''

    df_demanda = obtener_datos_de_db2("DEMANDA")
    if df_demanda.empty:
        return None
    else:
        print("Tabla DEMANDA cargada correctamente.")

    df_calendario = obtener_datos_de_db2("CALENDARIO")
    if df_calendario.empty:
        return None
    else:
        print("Tabla CALENDARIO cargada correctamente.")

    return preparar_datos(df_demanda, df_calendario)


@st.cache_data(ttl=300, show_spinner="Leyendo el histórico de z/OS...")
def cargar_historial():
    '''Lee las últimas generaciones del GDG.'''

    return cargar_historico(GENERACIONES_RECIENTES)


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


def mostrar_grafico_global(df, anio, transporte, tipo_dia, tipo_grafico):
    '''Muestra los viajes acumulados de cada mes.'''

    df_grafico = calcular_demanda_por_mes(
        df,
        anio=anio,
        transporte=transporte,
        tipo_dia=tipo_dia,
    )

    if df_grafico.empty:
        st.info("No hay datos para los filtros seleccionados.")
        return None

    fig = crear_grafico_demanda_mensual(
        df_grafico,
        anio,
        transporte,
        tipo_grafico,
    )

    st.plotly_chart(fig, width="stretch")

    return df_grafico


def mostrar_grafico_mensual(df, anio, mes, transporte, tipo_dia, tipo_grafico):
    '''Muestra los viajes de cada día del mes seleccionado.'''

    df_grafico = calcular_demanda_diaria(
        df,
        anio=anio,
        mes=mes,
        transporte=transporte,
        tipo_dia=tipo_dia,
    )

    if df_grafico.empty:
        st.info("No hay datos para los filtros seleccionados.")
        return None

    fig = crear_grafico_demanda_diaria(
        df_grafico,
        anio,
        mes,
        transporte,
        tipo_grafico,
    )

    st.plotly_chart(fig, width="stretch")

    return df_grafico


def mostrar_grafico_transportes(df, anio, mes, tipo_dia):
    '''Muestra el reparto de viajes entre los transportes.'''

    df_transporte = calcular_demanda_por_transporte(
        df,
        anio=anio,
        mes=mes,
        tipo_dia=tipo_dia,
    )

    fig = crear_grafico_demanda_por_transporte(df_transporte, anio, mes)

    st.plotly_chart(fig, width="stretch")


def crear_tarjeta(columna, etiqueta, valor, detalle=None):
    '''Muestra una tarjeta con un valor y un texto de apoyo opcional.'''

    columna.metric(
        etiqueta,
        valor,
        delta=detalle,
        delta_color="off",
        delta_arrow="off",
    )


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

    if filtros["vista"] == "Global":
        fecha_pico = resumen["fecha_pico"]
        tarjetas.append((
            "Pico diario",
            f"{resumen['pico_diario']:,.0f}",
            fecha_pico.strftime("%d/%m/%Y") if fecha_pico is not None else None,
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

    for columna, tarjeta in zip(st.columns(len(tarjetas)), tarjetas):
        crear_tarjeta(columna, *tarjeta)


def mostrar_resultados(df, filtros):
    '''Muestra las tarjetas y los gráficos del periodo seleccionado.'''

    anio = filtros["anio"]
    mes = filtros["mes"]
    transporte = filtros["transporte"]
    tipo_dia = filtros["tipo_dia"]
    tipo_grafico = filtros["tipo_grafico"]

    zona_tarjetas = st.container()
    columna_principal, columna_transportes = st.columns([2, 1])

    with columna_principal:
        if filtros["vista"] == "Global":
            df_grafico = mostrar_grafico_global(
                df, anio, transporte, tipo_dia, tipo_grafico
            )
        else:
            df_grafico = mostrar_grafico_mensual(
                df, anio, mes, transporte, tipo_dia, tipo_grafico
            )

    if df_grafico is None or df_grafico.empty:
        return

    with columna_transportes:
        mostrar_grafico_transportes(df, anio, mes, tipo_dia)

    with zona_tarjetas:
        mostrar_tarjetas(df, df_grafico, filtros)


def mostrar_dashboard():
    '''Muestra los filtros y los resultados de la demanda.'''

    try:
        df = cargar_datos()

        if df is None:
            st.warning("No hay datos disponibles en la base de datos.")
            return

        filtros = mostrar_filtros(df)

        if filtros is None:
            return

        mostrar_resultados(df, filtros)

    except Exception as e:
        st.error(f"Error al cargar el dashboard: {e}")


def lanzar_snapshot():
    '''Ejecuta el JCL desde el proyecto y refresca el historial.'''

    try:
        with st.spinner("Ejecutando el JCL en z/OS..."):
            guardar_historico()

        cargar_historial.clear()
        st.success("Nueva generación guardada en el GDG.")

    except Exception as e:
        st.error(f"No se pudo generar el snapshot: {e}")


def mostrar_tarjetas_historial(df_historial):
    '''Muestra el estado de la última generación del GDG.'''

    ultima = df_historial["GENERACION"].iloc[-1]
    datos = df_historial[df_historial["GENERACION"] == ultima]

    fecha = datos["SNAPSHOT"].max()

    tarjetas = [
        (
            "Último snapshot",
            fecha.strftime("%d/%m/%Y") if pd.notna(fecha) else "-",
            ultima,
        ),
    ]

    for _, fila in datos.iterrows():
        rango = (
            f"{fila['FECHA_MIN']:%d/%m/%Y} - {fila['FECHA_MAX']:%d/%m/%Y}"
            if pd.notna(fila["FECHA_MIN"]) and pd.notna(fila["FECHA_MAX"])
            else None
        )
        tarjetas.append(
            (f"Filas de {fila['TABLA']}", f"{fila['NUM_FILAS']:,.0f}", rango)
        )

    for columna, tarjeta in zip(st.columns(len(tarjetas)), tarjetas):
        crear_tarjeta(columna, *tarjeta)


def preparar_tabla_historial(df_historial):
    '''Devuelve una fila por generación con los datos de cada tabla en columnas.'''

    resultado = (
        df_historial[["GENERACION", "SNAPSHOT"]]
        .drop_duplicates(subset="GENERACION")
    )

    for tabla in df_historial["TABLA"].unique():
        datos = df_historial.loc[
            df_historial["TABLA"] == tabla,
            ["GENERACION", "NUM_FILAS", "FECHA_MIN", "FECHA_MAX"],
        ].rename(columns={
            "NUM_FILAS": f"Filas {tabla}",
            "FECHA_MIN": f"{tabla}: desde",
            "FECHA_MAX": f"{tabla}: hasta",
        })

        resultado = resultado.merge(datos, on="GENERACION", how="left")

    return resultado.sort_values("GENERACION", ascending=False)


def mostrar_tabla_historial(df_historial):
    '''Muestra una fila por generación, de la más reciente a la más antigua.'''

    tabla = preparar_tabla_historial(df_historial)

    columnas = {
        "GENERACION": st.column_config.TextColumn("Generación"),
        "SNAPSHOT": st.column_config.DateColumn(
            "Snapshot", format="DD/MM/YYYY"
        ),
    }

    for columna in tabla.columns[2:]:
        if columna.startswith("Filas"):
            columnas[columna] = st.column_config.NumberColumn(
                columna, format="localized"
            )
        else:
            columnas[columna] = st.column_config.DateColumn(
                columna, format="DD/MM/YYYY"
            )

    st.dataframe(
        tabla,
        width="stretch",
        hide_index=True,
        column_config=columnas,
    )


def mostrar_historial():
    '''Muestra las últimas generaciones del GDG creadas desde el JCL.'''

    columna_texto, columna_boton = st.columns([4, 1], vertical_alignment="center")

    columna_texto.caption(
        f"Últimas {GENERACIONES_RECIENTES} generaciones guardadas en z/OS."
    )

    if columna_boton.button("Guardar nuevo snapshot", width="stretch"):
        lanzar_snapshot()

    try:
        df_historial = cargar_historial()
    except Exception as e:
        st.error(f"No se pudo leer el histórico: {e}")
        return

    if df_historial.empty:
        st.info("Todavía no hay generaciones en el GDG.")
        return

    mostrar_tarjetas_historial(df_historial)
    mostrar_tabla_historial(df_historial)


def mostrar_panel():
    '''Coordina la página y sus pestañas.'''

    configurar_pagina()
    mostrar_cabecera()

    pestana_dashboard, pestana_historial = st.tabs(["Dashboard", "Historial"])

    with pestana_dashboard:
        mostrar_dashboard()

    with pestana_historial:
        mostrar_historial()