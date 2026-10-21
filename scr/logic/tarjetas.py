import streamlit as st


def crear_tarjeta(columna, etiqueta, valor, detalle=None):
    '''Muestra una tarjeta con un valor y un texto de apoyo opcional.'''

    columna.metric(
        etiqueta,
        valor,
        delta=detalle,
        delta_color="off",
        delta_arrow="off",
    )


def mostrar_fila_tarjetas(tarjetas):
    '''Muestra las tarjetas en una sola fila, una columna por tarjeta.'''

    for columna, tarjeta in zip(st.columns(len(tarjetas)), tarjetas):
        crear_tarjeta(columna, *tarjeta)