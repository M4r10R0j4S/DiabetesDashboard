import pandas as pd
import plotly.graph_objects as go

from config import COLORS_TASA, COLORS_RR, COLORS_CAMBIO


def crear_mapa(df, geojson, indicador):

    # ========================================================
    # 1. TASA DE DETECCIÓN
    # ========================================================

    if indicador == "Tasa de detección":

        z = df["nivel_tasa"]
        hover = df["hover_tasa"]

        titulo = "Tasa de detección de diabetes"

        colorscale = COLORS_TASA

        zmin = 1
        zmax = 5
        zmid = None

        tickvals = [1, 2, 3, 4, 5]

        ticktext = [
            "Muy bajo",
            "Bajo",
            "Medio",
            "Alto",
            "Muy alto"
        ]


    # ========================================================
    # 2. RDI / RDRI
    # ========================================================

    elif indicador == "Índice relativo de tasa de detección (RDI)":

        z = df["nivel_rdi"]
        hover = df["hover_rdi"]

        titulo = "Índice relativo de tasa de detección (RDI)"

        colorscale = COLORS_RR

        # Tres niveles: 1, 2 y 3
        zmin = 0.5
        zmax = 3.5
        zmid = None

        tickvals = [1, 2, 3]

        ticktext = [
            "Below national rate",
            "Similar to national rate",
            "Above national rate"
        ]


    # ========================================================
    # 3. CAMBIO PORCENTUAL RESPECTO A 2000
    # ========================================================

    elif indicador == "Cambio porcentual respecto a 2000":

        z = df["cambio_pct_2000"]
        hover = df["hover_cambio"]

        titulo = "Cambio porcentual de la CDR respecto a 2000"

        colorscale = COLORS_CAMBIO

        # Escala simétrica alrededor de cero
        limite = max(
            abs(df["cambio_pct_2000"].min()),
            abs(df["cambio_pct_2000"].max())
        )

        if pd.isna(limite) or limite == 0:
            limite = 1

        zmin = -limite
        zmax = limite
        zmid = 0

        tickvals = None
        ticktext = None


    # ========================================================
    # INDICADOR NO RECONOCIDO
    # ========================================================

    else:

        raise ValueError(
            f"Indicador no reconocido: {indicador}"
        )


    # ========================================================
    # CREAR FIGURA
    # ========================================================

    fig = go.Figure()


    # ========================================================
    # MAPA COROPLÉTICO
    # ========================================================

    fig.add_trace(

        go.Choropleth(

            geojson=geojson,

            featureidkey="properties.name",

            locations=df["entidad_geo"],

            z=z,

            zmin=zmin,

            zmax=zmax,

            zmid=zmid,

            colorscale=colorscale,

            marker_line_color="white",

            marker_line_width=0.8,

            customdata=hover,

            hovertemplate="%{customdata}<extra></extra>",

            colorbar=dict(

                title=titulo,

                tickvals=tickvals,

                ticktext=ticktext,

                thickness=18,

                len=0.70,

                outlinewidth=0
            )
        )
    )


    # ========================================================
    # CÍRCULOS DE POBLACIÓN AFILIADA AL IMSS
    # ========================================================

    fig.add_trace(

        go.Scattergeo(

            lon=df["lon"],

            lat=df["lat"],

            mode="markers",

            marker=dict(

                size=df["tamano"],

                color="royalblue",

                opacity=0.55
            ),

            customdata=hover,

            hovertemplate="%{customdata}<extra></extra>",

            showlegend=False
        )
    )


    # ========================================================
    # CONFIGURACIÓN GEOGRÁFICA
    # ========================================================

    fig.update_geos(

        fitbounds="locations",

        visible=False,

        projection_type="mercator"
    )


    # ========================================================
    # DISEÑO
    # ========================================================

    fig.update_layout(

        height=700,

        margin=dict(
            l=0,
            r=0,
            t=70,
            b=0
        ),

        title=dict(
            text=titulo,
            x=0.5,
            xanchor="center"
        )
    )


    return fig
