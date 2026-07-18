import plotly.graph_objects as go

def crear_mapa(df,geojson,indicador):
    
    if indicador=="Tasa de detección":

        z=df["nivel_tasa"]

        hover=df["hover_tasa"]

        titulo="Tasa de detección"
        
        colorscale = colors_tasa

        colors_tasa=[

            [0.0,"#ffffcc"],
    
            [0.25,"#ffeda0"],

            [0.50,"#feb24c"],

            [0.75,"#f03b20"],

            [1.0,"#bd0026"]

        ]

        ticktext = [
            "Muy bajo",
            "Bajo",
            "Medio",
            "Alto",
            "Muy alto"
        ]

    else:

        z=df["nivel_rr"]

        hover=df["hover_rr"]

        titulo="Riesgo relativo"
        
        colorscale = colors_rr

        colors_rr=[

            [0.0,"#006837"],

            [0.25,"#66bd63"],

            [0.50,"#ffffbf"],

            [0.75,"#fdae61"],

            [1.0,"#d73027"]

        ]

        ticktext = [
            "Muy bajo",
            "Bajo",
            "Promedio",
            "Alto",
            "Muy alto"
        ]
    
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

            zmin=1,

            zmax=5,

            colorscale=colorscale,

            marker_line_color="white",

            marker_line_width=0.8,

            customdata=hover,

            hovertemplate="%{customdata}<extra></extra>"
            
            colorbar=dict(

                title=titulo,

                tickvals=[1,2,3,4,5],

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
