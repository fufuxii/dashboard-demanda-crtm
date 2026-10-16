import streamlit as st
from scr.logic.dashboard.panel import mostrar_panel
from scr.logic.historial.historial import guardar_historico


@st.cache_resource
def historico_una_vez():
    '''Guarda el histórico solo la primera vez que se ejecuta
       mientras el servidor siga encendido.'''
    guardar_historico()
    return True


mostrar_panel()
historico_una_vez()