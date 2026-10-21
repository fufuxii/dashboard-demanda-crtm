import pandas as pd
import streamlit as st
from scr.logic.historial import (
    cargar_historico,
    guardar_historico,
    preparar_tabla_historial,
)
from scr.logic.tarjetas import mostrar_fila_tarjetas
from scr.logic.variables import GENERACIONES_RECIENTES


@st.cache_data(ttl=300, show_spinner="Leyendo el histórico de z/OS...")
def cargar_historial():
    '''Lee las últimas generaciones del GDG.'''

    return cargar_historico()


def lanzar_snapshot():
    '''Ejecuta el JCL desde el proyecto y refresca el historial.'''

    with st.spinner("Ejecutando el JCL en z/OS..."):
        guardar_historico()

    # Se vacía la caché para que la lectura siguiente incluya la nueva generación.
    cargar_historial.clear()
    st.success("Nueva generación guardada en el GDG.")


def mostrar_tarjetas_historial(df_historial):
    '''Muestra el estado de la última generación del GDG.'''

    # El historial llega ordenado, así que la última fila es la más reciente.
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

    mostrar_fila_tarjetas(tarjetas)


def mostrar_tabla_historial(df_historial):
    '''Muestra una fila por generación, de la más reciente a la más antigua.'''

    tabla = preparar_tabla_historial(df_historial)

    columnas = {
        "GENERACION": st.column_config.TextColumn("Generación"),
        "SNAPSHOT": st.column_config.DateColumn(
            "Snapshot", format="DD/MM/YYYY"
        ),
    }

    # Las columnas de cada tabla son de filas (número) o de fechas.
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

    df_historial = cargar_historial()

    if df_historial.empty:
        st.info("Todavía no hay generaciones en el GDG.")
        return

    mostrar_tarjetas_historial(df_historial)
    mostrar_tabla_historial(df_historial)