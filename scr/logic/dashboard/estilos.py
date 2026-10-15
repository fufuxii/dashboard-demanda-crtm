import streamlit as st


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
ROJO = "#EE6A5B"
ROJO_CLARO = "#FDE0DC"

NARANJA_OSCURO = "#D9730D"
NARANJA = "#F28C28"
NARANJA_CLARO = "#FFE9D0"

LAVANDA = "#7C5CE0"
LAVANDA_CLARO = "#E6E0FB"

AZUL_PASTEL = "#2F80ED"
AZUL_CLARO = "#DCEBFF"

VERDE_PASTEL = "#16A37F"
VERDE_CLARO = "#D3F3E8"

AMARILLO_PASTEL = "#E8B100"
GRIS_PASTEL = "#9AA3B5"

COLORES_TRANSPORTE = {
    "METRO": ROJO_OSCURO,
    "EMT": AZUL_PASTEL,
    "CARRETERA": NARANJA,
    "RENFE": VERDE_PASTEL,
    "TOTAL": LAVANDA,
}

COLORES_TIPO_DIA = {
    "Laborables": AZUL_PASTEL,
    "Fines de semana": LAVANDA,
    "Festivos": NARANJA,
}

COLORES_PASTEL = [
    AZUL_PASTEL,
    VERDE_PASTEL,
    NARANJA,
    LAVANDA,
    ROJO_OSCURO,
    AMARILLO_PASTEL,
]

FUENTE = "Montserrat, sans-serif"


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


ESTILOS_BASE = """
    html,
    body,
    [data-testid="stApp"],
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stHeader"] {
        font-family: "Montserrat", sans-serif !important;
        background: var(--fondo) !important;
        color: var(--texto) !important;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1400px;
        margin: auto;
        padding: 4rem 2rem 1.5rem;
    }

    [data-testid="stVerticalBlock"] {
        gap: 0.75rem;
    }

    h1, h2, h3 {
        color: var(--titulo) !important;
        font-family: "Montserrat", sans-serif !important;
    }

    h2, h3 {
        font-weight: 700 !important;
        font-size: 1.25rem !important;
        margin-top: 0.75rem !important;
    }

    p, label {
        color: var(--texto) !important;
        font-family: "Montserrat", sans-serif !important;
    }

    [data-testid="stCaptionContainer"] {
        color: var(--texto-secundario) !important;
    }

    hr {
        border-color: var(--borde) !important;
        margin: 1.25rem 0 !important;
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

    li[role="option"]:hover,
    div[role="option"]:hover {
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

    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    textarea {
        color: var(--texto) !important;
        border-radius: 8px !important;
    }

    [data-testid="stTextInput"] input:focus,
    [data-testid="stNumberInput"] input:focus,
    textarea:focus {
        border-color: var(--control) !important;
        box-shadow: 0 0 0 1px var(--control) !important;
    }

    .stButton > button,
    [data-testid="stDownloadButton"] > button {
        background: var(--control) !important;
        border: 1px solid var(--control) !important;
        border-radius: 8px !important;
        font-family: "Montserrat", sans-serif !important;
    }

    .stButton > button:hover,
    [data-testid="stDownloadButton"] > button:hover {
        background: var(--titulo) !important;
        border-color: var(--titulo) !important;
    }

    .stButton > button p,
    [data-testid="stDownloadButton"] > button p {
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

    [data-testid="stDataFrame"],
    [data-testid="stTable"] {
        border: 1px solid var(--borde) !important;
        border-radius: 10px !important;
        overflow: hidden;
    }

    [data-testid="stExpander"] {
        background: var(--fondo-secundario) !important;
        border: 1px solid var(--borde) !important;
        border-radius: 8px !important;
    }
"""


ESTILOS_MOVIL = """
    @media (max-width: 600px) {
        [data-testid="stMainBlockContainer"] {
            padding: 4rem 1rem 1rem;
        }

        .crtm-banner {
            padding: 1.1rem 1.25rem;
        }

        .crtm-banner h1 {
            font-size: 1.4rem !important;
        }
    }
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
        + ESTILOS_MOVIL
    )

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)