import plotly.graph_objects as go
from config import COLORS_TASA, COLORS_RR

def crear_mapa(df,geojson,indicador):
    
    if indicador=="Tasa de detección":

        z=df["nivel_tasa"]

        hover=df["hover_tasa"]

        titulo="Tasa de detección"
        
        colorscale = COLORS_TASA

        ticktext = [
            "Muy bajo",
            "Bajo",
            "Medio",
            "Alto",
            "Muy alto"
        ]

    else:

        z=df["nivel_rdi"]

        hover=df["hover_rdi"]

        #titulo="Riesgo relativo"

        titulo="IRD"
        
        colorscale = COLORS_RR

        zmin = 0.5
        zmax = 3.5
        tickvals = [1, 2, 3]
        ticktext = [
            "Below national rate",
            "Similar to national rate",
            "Above national rate"
        ]

        #ticktext = [
         #   "Muy bajo",
         #   "Bajo",
         #   "Promedio",
         #   "Alto",
         #   "Muy alto"
        #]
    
     # =====================================
    # Crear figura
    # =====================================      

    fig=go.Figure()

     # =====================================
    # Choropleth
    # =====================================
    
    fig.add_trace(

        go.Choropleth(

            geojson=geojson,

            featureidkey="properties.name",

            locations=df["entidad"],

            z=z,
            zmin=zmin,
            zmax=zmax,
            
            #zmin=1,

            #zmax=5,

            colorscale=colorscale,

            marker_line_color="white",

            marker_line_width=0.8,

            customdata=hover,

            hovertemplate="%{customdata}<extra></extra>",
            
            colorbar=dict(

                title=titulo,
                tickvals=tickvals,
                #tickvals=[1,2,3,4,5],

                ticktext=ticktext
            )

        )

    )

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

    fig.update_geos(

        fitbounds="locations",

        visible=False

    )

    fig.update_layout(

        height=700,

        margin=dict(

            l=0,

            r=0,

            t=60,

            b=0

        ),

        title=dict(

            text=titulo,

            x=0.5

        )

    )

    return fig
