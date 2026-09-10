import plotly.graph_objects as go

from config import COLORS_TASA, COLORS_RR


def crear_mapa(df, geojson, indicador):

    # ========================================================
    # TASA DE DETECCIÓN
    # ========================================================

    if indicador == "tasa":

        z = df["nivel_tasa"]
        hover = df["hover_tasa"]

        titulo = "Tasa de detección de diabetes"

        colorscale = COLORS_TASA

        zmin = 1
        zmax = 5

        tickvals = [1, 2, 3, 4, 5]

        ticktext = [
            "Muy bajo",
            "Bajo",
            "Medio",
            "Alto",
            "Muy alto"
        ]


    # ========================================================
    # ÍNDICE RELATIVO DE TASA DE DETECCIÓN
    # ========================================================

    elif indicador == "rdi":

        z = df["nivel_rdi"]
        hover = df["hover_rdi"]

        titulo = "Índice relativo de tasa de detección (IRD)"

        colorscale = COLORS_RR

        zmin = 0.5
        zmax = 3.5

        tickvals = [1, 2, 3]

        ticktext = [
            "Por debajo de la tasa nacional",
            "Similar a la tasa nacional",
            "Por encima de la tasa nacional"
        ]


    # ========================================================
    # INDICADOR NO RECONOCIDO
    # ========================================================

    else:

        raise ValueError(
            f"Indicador no reconocido: {repr(indicador)}"
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
    # CÍRCULOS DE AFILIADOS AL IMSS
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
