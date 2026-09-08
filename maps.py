import plotly.graph_objects as go

from config import COLORS_TASA, COLORS_RR


# ============================================================
# CREAR MAPA
# ============================================================

def crear_mapa(df, geojson, indicador):


    # ========================================================
    # TASA DE DETECCIÓN
    # ========================================================

    if indicador == "Tasa de detección":

        z = df["nivel_tasa"]

        hover = df["hover_tasa"]

        titulo = "Tasa de detección"

        colorscale = COLORS_TASA

        zmin = 1

        zmax = 5

        zmid = None

        tickvals = [
            1,
            2,
            3,
            4,
            5
        ]

        ticktext = [
            "Muy bajo",
            "Bajo",
            "Medio",
            "Alto",
            "Muy alto"
        ]

        colorbar_title = "Nivel"


    # ========================================================
    # RDI
    # ========================================================

    elif indicador == "Índice relativo de tasa de detección (RDI)":

        z = df["nivel_rdi"]

        hover = df["hover_rdi"]

        titulo = (
            "Índice relativo de tasa de detección (RDI)"
        )

        colorscale = COLORS_RR

        zmin = 1

        zmax = 5

        zmid = None

        tickvals = [
            1,
            2,
            3,
            4,
            5
        ]

        ticktext = [
            "Muy por debajo",
            "Por debajo",
            "Similar",
            "Por encima",
            "Muy por encima"
        ]

        colorbar_title = "RDI"


    # ========================================================
    # CAMBIO PORCENTUAL 2000 - 2020
    # ========================================================

    elif indicador == "Cambio porcentual 2000-2020":

        z = df["cambio_pct"]

        hover = df["hover_cambio"]

        titulo = (
            "Cambio porcentual de la tasa de detección "
            "entre 2000 y 2020"
        )

        # Azul = disminución
        # Blanco = cercano a 0
        # Rojo = incremento

        colorscale = "RdBu_r"

        max_abs = max(
            abs(df["cambio_pct"].min()),
            abs(df["cambio_pct"].max())
        )

        zmin = -max_abs

        zmax = max_abs

        zmid = 0

        tickvals = None

        ticktext = None

        colorbar_title = "Cambio (%)"


    else:

        raise ValueError(
            f"Indicador no reconocido: {indicador}"
        )


    # ========================================================
    # FIGURA
    # ========================================================

    fig = go.Figure()


    # ========================================================
    # PARÁMETROS DEL CHOROPLETH
    # ========================================================

    parametros = dict(

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

        hovertemplate=(
            "%{customdata}"
            "<extra></extra>"
        ),

        colorbar=dict(

            title=colorbar_title,

            thickness=18,

            len=0.70,

            outlinewidth=0
        )
    )


    # ========================================================
    # CENTRO DE ESCALA
    # ========================================================

    if zmid is not None:

        parametros["zmid"] = zmid


    # ========================================================
    # ETIQUETAS COLORBAR PARA MAPAS CATEGÓRICOS
    # ========================================================

    if tickvals is not None:

        parametros["colorbar"]["tickvals"] = tickvals

        parametros["colorbar"]["ticktext"] = ticktext


    # ========================================================
    # COROPLÉTICO
    # ========================================================

    fig.add_trace(

        go.Choropleth(
            **parametros
        )
    )


    # ========================================================
    # CÍRCULOS DE AFILIADOS
    # ========================================================

    if "tamano" in df.columns:

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
    # LAYOUT
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
