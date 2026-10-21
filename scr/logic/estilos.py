import streamlit as st

FUENTE = "Montserrat, sans-serif"

FONDO = "#FFFFFF"
FONDO_SECUNDARIO = "#F4F8FD"
BORDE = "#CFDBEC"
REJILLA = "#E4ECF6"

TEXTO = "#22293D"
TEXTO_SECUNDARIO = "#5D6781"
TITULO = "#1B2A55"

ACENTO = "#12949F"
ACENTO_CLARO = "#CDEFF2"

ROJO_OSCURO = "#D8403F"
NARANJA = "#F28C28"
LAVANDA = "#7C5CE0"
AZUL_PASTEL = "#2F80ED"
AZUL_CLARO = "#DCEBFF"
VERDE_PASTEL = "#16A37F"
AMARILLO_PASTEL = "#E8B100"

COLORES_TRANSPORTE = {
    "METRO": ROJO_OSCURO,
    "EMT": AZUL_PASTEL,
    "CARRETERA": NARANJA,
    "RENFE": VERDE_PASTEL,
    "TOTAL": LAVANDA,
}

COLORES_PASTEL = [
    AZUL_PASTEL,
    VERDE_PASTEL,
    NARANJA,
    LAVANDA,
    ROJO_OSCURO,
    AMARILLO_PASTEL,
]

ESTILOS_BASE = """
    html,
    body,
    [data-testid="stApp"],
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        font-family: "Montserrat", sans-serif !important;
        background: var(--fondo) !important;
        color: var(--texto) !important;
    }

    [data-testid="stVerticalBlock"] {
        gap: 0.75rem;
    }

    [data-testid="stHeader"] {
        display: none;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1400px;
        margin: auto;
        padding: 0.8rem;
    }

    p, label {
        color: var(--texto) !important;
        font-family: "Montserrat", sans-serif !important;
    }

    [data-testid="stCaptionContainer"] {
        color: var(--texto-secundario) !important;
    }
"""

ESTILOS_CABECERA = """
    .crtm-banner {
        background: var(--titulo);
        border-left: 8px solid var(--acento);
        border-radius: 12px;
        padding: 1rem 1.75rem;
        margin-bottom: 0;
    }

    .crtm-banner h1 {
        color: #FFFFFF !important;
        font-family: "Montserrat", sans-serif !important;
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        line-height: 1.3 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow-wrap: anywhere;
    }

    .crtm-banner p {
        color: var(--acento-claro) !important;
        font-size: 0.9rem;
        margin: 0.25rem 0 0;
    }
"""

ESTILOS_CONTROLES = """
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--fondo-secundario) !important;
        border: 1px solid var(--borde) !important;
        border-radius: 12px !important;
        padding: 0.25rem 0.5rem;
    }

    [data-testid="stWidgetLabel"] p {
        color: var(--titulo) !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }

    div[data-baseweb="select"] > div {
        background: var(--fondo) !important;
        border: 1px solid var(--borde) !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="select"] input,
    div[data-baseweb="select"] span {
        color: var(--texto) !important;
    }

    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    li[role="option"],
    div[role="option"] {
        background: var(--fondo) !important;
        color: var(--texto) !important;
    }

    li[role="option"] > div:hover,
    div[role="option"] > div:hover {
        background: var(--control-claro) !important;
    }

    div[role="radiogroup"] {
        gap: 0.75rem;
        min-height: 2.5rem;
        align-items: center;
    }

    label[data-baseweb="radio"]:has(input:checked) > div:first-child {
        background-color: var(--control) !important;
        border-color: var(--control) !important;
    }

    input[type="radio"] {
        accent-color: var(--control);
    }

    div[role="radiogroup"] label p {
        color: var(--texto) !important;
    }

    div[data-baseweb="select"] > div > div,
    div[data-baseweb="select"] input {
        background: var(--fondo) !important;
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        outline: none !important;
    }

    div[data-baseweb="select"] > div:focus-within {
        border-color: var(--control) !important;
        box-shadow: 0 0 0 1px var(--control) !important;
    }

    .stButton > button {
        background: var(--control) !important;
        border: 1px solid var(--control) !important;
        border-radius: 8px !important;
        font-family: "Montserrat", sans-serif !important;
    }

    .stButton > button:hover {
        background: var(--titulo) !important;
        border-color: var(--titulo) !important;
    }

    .stButton > button p {
        color: #FFFFFF !important;
    }
"""

ESTILOS_RESULTADOS = """
    [data-testid="stMetric"] {
        background: var(--fondo-secundario) !important;
        border: 1px solid var(--borde) !important;
        border-left: 5px solid var(--acento) !important;
        border-radius: 10px !important;
        padding: 0.6rem 1rem !important;
        min-height: 6.25rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    [data-testid="stColumn"]:nth-child(1) [data-testid="stMetric"],
    [data-testid="column"]:nth-child(1) [data-testid="stMetric"] {
        border-left-color: var(--azul) !important;
    }

    [data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"],
    [data-testid="column"]:nth-child(2) [data-testid="stMetric"] {
        border-left-color: var(--verde) !important;
    }

    [data-testid="stColumn"]:nth-child(3) [data-testid="stMetric"],
    [data-testid="column"]:nth-child(3) [data-testid="stMetric"] {
        border-left-color: var(--naranja) !important;
    }

    [data-testid="stColumn"]:nth-child(4) [data-testid="stMetric"],
    [data-testid="column"]:nth-child(4) [data-testid="stMetric"] {
        border-left-color: var(--lavanda) !important;
    }

    [data-testid="stColumn"]:nth-child(5) [data-testid="stMetric"],
    [data-testid="column"]:nth-child(5) [data-testid="stMetric"] {
        border-left-color: var(--rojo) !important;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] p {
        color: var(--texto-secundario) !important;
        font-size: 0.85rem !important;
    }

    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] > div {
        color: var(--titulo) !important;
        font-weight: 700 !important;
        font-size: clamp(1.1rem, 1.6vw, 1.5rem) !important;
        line-height: 1.3 !important;
        white-space: nowrap;
        overflow: visible !important;
        text-overflow: clip !important;
    }

    [data-testid="stMetricDelta"] {
        font-size: 0.75rem !important;
    }

    [data-testid="stPlotlyChart"] {
        background: var(--fondo) !important;
        border: 1px solid var(--borde) !important;
        border-radius: 12px !important;
        padding: 0 !important;
        overflow: hidden;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--borde) !important;
        border-radius: 10px !important;
        overflow: hidden;
    }
"""

ESTILOS_PESTANAS = """
    button[data-baseweb="tab"] p {
        color: var(--texto-secundario) !important;
        font-weight: 600 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] p {
        color: var(--titulo) !important;
    }

    [data-baseweb="tab-highlight"] {
        background-color: var(--acento) !important;
    }

    [data-baseweb="tab-border"] {
        background-color: var(--borde) !important;
    }
"""


def aplicar_estilo_grafico(fig):
    '''Aplica un estilo uniforme a los gráficos.'''

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor=FONDO,
        plot_bgcolor=FONDO,
        font=dict(family=FUENTE, color=TEXTO, size=13),
        title=dict(
            font=dict(family=FUENTE, color=TITULO, size=18),
            x=0,
            xanchor="left",
        ),
        colorway=COLORES_PASTEL,
        margin=dict(l=25, r=25, t=60, b=50),
        legend_title_text="",
        bargap=0.25,
        hoverlabel=dict(
            bgcolor=FONDO_SECUNDARIO,
            font_color=TEXTO,
            bordercolor=BORDE,
            font_family=FUENTE,
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor=REJILLA,
        tickfont=dict(color=TEXTO_SECUNDARIO),
        title_font=dict(color=TEXTO_SECUNDARIO, size=12),
    )

    fig.update_yaxes(
        gridcolor=REJILLA,
        linecolor=FONDO,
        tickfont=dict(color=TEXTO_SECUNDARIO),
        title_font=dict(color=TEXTO_SECUNDARIO, size=12),
        tickformat=",.0f",
        rangemode="tozero",
        zeroline=False,
    )

    return fig


def generar_variables():
    '''Devuelve las variables CSS construidas con la paleta.'''

    return f"""
        :root {{
            --fondo: {FONDO};
            --fondo-secundario: {FONDO_SECUNDARIO};
            --texto: {TEXTO};
            --texto-secundario: {TEXTO_SECUNDARIO};
            --titulo: {TITULO};
            --acento: {ACENTO};
            --acento-claro: {ACENTO_CLARO};
            --control: {AZUL_PASTEL};
            --control-claro: {AZUL_CLARO};
            --borde: {BORDE};
            --azul: {AZUL_PASTEL};
            --verde: {VERDE_PASTEL};
            --naranja: {NARANJA};
            --lavanda: {LAVANDA};
            --rojo: {ROJO_OSCURO};
        }}
    """


def aplicar_estilo_interfaz():
    '''Aplica los estilos generales del dashboard.'''

    fuente = (
        "@import url('https://fonts.googleapis.com/css2"
        "?family=Montserrat:wght@400;500;600;700;800&display=swap');"
    )

    css = (
        fuente
        + generar_variables()
        + ESTILOS_BASE
        + ESTILOS_CABECERA
        + ESTILOS_CONTROLES
        + ESTILOS_RESULTADOS
        + ESTILOS_PESTANAS
    )

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)