import plotly.graph_objects as go

from config import COLORS_TASA, COLORS_RR


# ============================================================
# FUNCIÓN PARA CREAR MAPA
# ============================================================

def crear_mapa(df, geojson, indicador):

    # ========================================================
    # CONFIGURACIÓN SEGÚN INDICADOR
    # ========================================================

    if indicador == "Tasa de detección":

        z = df["nivel_tasa"]

        hover = df["hover_tasa"]

        titulo = (
            "Tasa de detección de diabetes"
        )

        colorscale = COLORS_TASA

        ticktext = [
            "Muy bajo",
            "Bajo",
            "Medio",
            "Alto",
            "Muy alto"
        ]


    elif indicador == "Índice relativo de tasa de detección (RDI)":

        z = df["nivel_rdi"]

        hover = df["hover_rdi"]

        titulo = (
            "Índice relativo de tasa de detección (RDI)"
        )

        colorscale = COLORS_RR

        ticktext = [
            "Muy por debajo",
            "Por debajo",
            "Similar",
            "Por encima",
            "Muy por encima"
        ]


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

            zmin=1,

            zmax=5,

            colorscale=colorscale,

            marker_line_color="white",

            marker_line_width=0.8,

            customdata=hover,

            hovertemplate=(
                "%{customdata}"
                "<extra></extra>"
            ),

            colorbar=dict(

                title=titulo,

                tickvals=[
                    1,
                    2,
                    3,
                    4,
                    5
                ],

                ticktext=ticktext,

                thickness=18,

                len=0.70,

                outlinewidth=0
            )
        )
    )


    # ========================================================
    # CÍRCULOS DE AFILIADOS
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

            hovertemplate=(
                "%{customdata}"
                "<extra></extra>"
            ),

            name="Afiliados al IMSS",

            showlegend=True
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
