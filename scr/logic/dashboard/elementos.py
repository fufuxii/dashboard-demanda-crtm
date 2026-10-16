import plotly.express as px
from scr.logic.dashboard.estilos import (
    COLORES_TRANSPORTE,
    NARANJA_OSCURO,
    ROJO_OSCURO,
    aplicar_estilo_grafico,
)
from scr.logic.dashboard.variables import (
    TRANSPORTES, MESES, ALTURA_GRAFICO
)


def obtener_color_transporte(transporte="TODOS"):
    '''Devuelve el color asociado al transporte seleccionado.'''

    if transporte == "TODOS":
        transporte = "TOTAL"

    return COLORES_TRANSPORTE.get(transporte, ROJO_OSCURO)


def crear_figura(parametros, tipo_grafico, color):
    '''Crea un gráfico de barras o de líneas con un único color.'''

    if tipo_grafico == "Líneas":
        fig = px.line(**parametros, markers=True)
        fig.update_traces(
            line=dict(color=color, width=3),
            marker=dict(color=color, size=7),
        )
    else:
        fig = px.bar(**parametros, color_discrete_sequence=[color])

    return fig


def crear_grafico_demanda_mensual(df_mensual, anio, transporte="TODOS", tipo_grafico="Barras"):
    '''Muestra los viajes acumulados de cada mes.'''

    parametros = {
        "data_frame": df_mensual,
        "x": "MES_NOMBRE",
        "y": "VIAJES",
        "title": f"Demanda mensual - {anio} - {TRANSPORTES[transporte]}",
        "labels": {"MES_NOMBRE": "Mes", "VIAJES": "Viajes"},
        "category_orders": {"MES_NOMBRE": list(MESES.values())},
    }

    color = obtener_color_transporte(transporte)
    fig = crear_figura(parametros, tipo_grafico, color)

    fig.update_traces(
        hovertemplate="%{x}<br>%{y:,.0f} viajes<extra></extra>"
    )

    fig.update_layout(
        xaxis_title="Mes",
        yaxis_title="Viajes acumulados",
        height=ALTURA_GRAFICO,
    )

    return aplicar_estilo_grafico(fig)


def crear_grafico_picos_mensuales(df_picos, anio):
    '''Muestra el máximo diario registrado en cada mes.'''

    fig = px.bar(
        df_picos,
        x="MES_NOMBRE",
        y="PICO_VIAJES",
        title=f"Pico de demanda diaria por mes - {anio}",
        labels={
            "MES_NOMBRE": "Mes",
            "PICO_VIAJES": "Viajes",
            "FECHA_PICO": "Fecha del pico",
        },
        hover_data=["FECHA_PICO"],
        color_discrete_sequence=[NARANJA_OSCURO],
        category_orders={"MES_NOMBRE": list(MESES.values())},
    )

    fig.update_layout(
        xaxis_title="Mes",
        yaxis_title="Máximo de viajes en un día",
        height=ALTURA_GRAFICO,
    )

    return aplicar_estilo_grafico(fig)


def crear_grafico_demanda_diaria(df_diaria, anio, mes, transporte, tipo_grafico):
    '''Muestra los viajes registrados cada día del mes.'''

    titulo = (
        f"Demanda diaria - {MESES[mes]} de {anio}"
        f" - {TRANSPORTES[transporte]}"
    )

    parametros = {
        "data_frame": df_diaria,
        "x": "FECHA",
        "y": "VIAJES",
        "title": titulo,
        "labels": {"FECHA": "Día", "VIAJES": "Viajes"},
    }

    color = obtener_color_transporte(transporte)
    fig = crear_figura(parametros, tipo_grafico, color)

    fig.update_traces(
        hovertemplate="%{x|%d/%m/%Y}<br>%{y:,.0f} viajes<extra></extra>"
    )

    fig.update_layout(
        xaxis_title="Día del mes",
        yaxis_title="Número de viajes",
        height=ALTURA_GRAFICO,
    )

    fig.update_xaxes(tickformat="%d", dtick="D1")

    return aplicar_estilo_grafico(fig)


def crear_grafico_demanda_por_transporte(df_transporte, anio, mes=None):
    '''Compara los viajes acumulados de cada transporte.'''

    datos = df_transporte.copy()
    total = datos["VIAJES"].sum() or 1

    datos["NOMBRE"] = datos["TRANSPORTE"].map(TRANSPORTES)
    datos["TEXTO"] = [
        f"{viajes / 1e6:,.0f} M ({viajes / total:.0%})"
        for viajes in datos["VIAJES"]
    ]
    datos = datos.sort_values("VIAJES")

    periodo = str(anio) if mes is None else f"{MESES[mes]} {anio}"

    fig = px.bar(
        datos,
        x="VIAJES",
        y="NOMBRE",
        orientation="h",
        color="TRANSPORTE",
        text="TEXTO",
        title=f"Reparto por transporte - {periodo}",
        labels={"NOMBRE": "Transporte", "VIAJES": "Viajes"},
        color_discrete_map=COLORES_TRANSPORTE,
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{y}<br>%{x:,.0f} viajes<extra></extra>",
    )

    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False,
        height=ALTURA_GRAFICO,
    )

    fig = aplicar_estilo_grafico(fig)

    fig.update_xaxes(visible=False, range=[0, datos["VIAJES"].max() * 1.5])

    return fig