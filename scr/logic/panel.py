import streamlit as st
from scr.logic.estilos import aplicar_estilo_interfaz
from scr.logic.panel_dashboard import mostrar_dashboard
from scr.logic.panel_historial import mostrar_historial


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


def mostrar_pestana(mostrar, nombre):
    '''Ejecuta una pestaña y, si falla, muestra el error sin afectar a la otra.'''

    try:
        mostrar()
    except Exception as e:
        st.error(f"Error en la pestaña {nombre}: {e}")


def mostrar_panel():
    '''Coordina la página y sus pestañas.'''

    configurar_pagina()
    mostrar_cabecera()

    pestana_dashboard, pestana_historial = st.tabs(["Dashboard", "Historial"])

    with pestana_dashboard:
        mostrar_pestana(mostrar_dashboard, "Dashboard")

    with pestana_historial:
        mostrar_pestana(mostrar_historial, "Historial")