"""
=============================================================
DATA LOADER

Dashboard Epidemiológico
Diabetes en México

Lee el archivo CSV y prepara todos los datos
para Streamlit.

=============================================================
"""

import numpy as np
import pandas as pd
import requests

from shapely.geometry import shape

# =====================================================
# CONFIGURACIÓN
# =====================================================

CSV_FILE = "deteccion_diabetes_resumen.csv"

GEOJSON_URL = (
    "https://raw.githubusercontent.com/"
    "angelnmara/geojson/master/"
    "mexicoHigh.json"
)

ANIOS = [2000, 2010, 2020]

NIVEL_TASA={

    "Muy bajo":1,
    "Bajo":2,
    "Medio":3,
    "Alto":4,
    "Muy alto":5
}

NIVEL_RR={

    "Muy bajo":1,
    "Bajo":2,
    "Promedio":3,
    "Alto":4,
    "Muy alto":5
}

def clasificar_tasa(serie):
    """
    Clasifica una serie numérica en 5 niveles
    utilizando quintiles.
    """

    q20, q40, q60, q80 = serie.quantile(
        [0.20,0.40,0.60,0.80]
    )

    categorias = []

    for valor in serie:

        if valor <= q20:

            categorias.append("Muy bajo")

        elif valor <= q40:

            categorias.append("Bajo")

        elif valor <= q60:

            categorias.append("Medio")

        elif valor <= q80:

            categorias.append("Alto")

        else:

            categorias.append("Muy alto")

    return categorias


def clasificar_rr(rr):

    categorias=[]

    for x in rr:

        if x < 0.80:

            categorias.append("Muy bajo")

        elif x < 0.95:

            categorias.append("Bajo")

        elif x <= 1.05:

            categorias.append("Promedio")

        elif x <= 1.20:

            categorias.append("Alto")

        else:

            categorias.append("Muy alto")

    return categorias

def escalar_poblacion(poblacion):

    p = poblacion.fillna(0)

    maximo = p.max()

    return np.sqrt(p/maximo)*40+8


def cargar_datos():

    df = pd.read_csv(CSV_FILE)

    df = df.dropna(how="all")

    df = df.dropna(subset=["entidad"])

    df["entidad"] = (
        df["entidad"]
        .astype(str)
        .str.strip()
    )

    df = df.rename(columns={

        "Riesgo_Relativo_2010":
            "riesgo_relativo_2010",

        "Riesgo_Relativo_2020":
            "riesgo_relativo_2020"
    })

    columnas = [

        c for c in df.columns

        if (

            c.startswith("casos")

            or

            c.startswith("poblacion")

            or

            c.startswith("tasa")

            or

            c.startswith("riesgo_relativo")

        )

    ]

    for c in columnas:

        df[c] = (

            df[c]

            .astype(str)

            .str.replace(",", "", regex=False)

            .astype(float)

        )
    
    mx_geo = requests.get(GEOJSON_URL).json()

    centroides = {}

    for feature in mx_geo["features"]:

        nombre = feature["properties"]["name"]

        poligono = shape(feature["geometry"])

        centro = poligono.centroid

        centroides[nombre] = (
            centro.x,
            centro.y
        )

    df["lon"] = df["entidad"].map(
        lambda e: centroides[e][0]
    )

    df["lat"] = df["entidad"].map(
        lambda e: centroides[e][1]
    )

    datos={}

    for anio in ANIOS:

        temp=df.copy()

        casos=f"casos_{anio}"

        poblacion=f"poblacion_{anio}"

        tasa=f"tasa_{anio}"

        rr=f"riesgo_relativo_{anio}"
    
        temp["categoria_tasa"]=clasificar_tasa(

        temp[tasa]

        )

        temp["nivel_tasa"]=(

            temp["categoria_tasa"]

            .map(NIVEL_TASA)

        )

        temp["categoria_rr"]=clasificar_rr(

            temp[rr]

        )

        temp["nivel_rr"]=(

            temp["categoria_rr"]

            .map(NIVEL_RR)

        )

        temp["tamano"]=escalar_poblacion(

            temp[poblacion]

        )

        temp["hover_tasa"]=(

            "<b>"+temp["entidad"]+"</b>"

            +"<br><br>"

            +"Casos: "

            +temp[casos].map("{:,.0f}".format)

            +"<br>Población: "

            +temp[poblacion].map("{:,.0f}".format)

            +"<br>Tasa: "

            +temp[tasa].map("{:.2f}".format)

            +"<br><b>Nivel: "

            +temp["categoria_tasa"]

            +"</b>"

        )

        temp["hover_rr"]=(

            "<b>"+temp["entidad"]+"</b>"

            +"<br><br>"

            +"Casos: "

            +temp[casos].map("{:,.0f}".format)

            +"<br>Población: "

            +temp[poblacion].map("{:,.0f}".format)

            +"<br>RR: "

            +temp[rr].map("{:.3f}".format)

            +"<br><b>Nivel: "

            +temp["categoria_rr"]

            +"</b>"

        )

        temp.attrs["stats"]={

            "tasa":{

                "media":temp[tasa].mean(),

                "mediana":temp[tasa].median(),

                "min":temp[tasa].min(),

                "max":temp[tasa].max()

            },

            "rr":{

                "media":temp[rr].mean(),

                "mediana":temp[rr].median(),

                "min":temp[rr].min(),

                "max":temp[rr].max()

            }

        }

        datos[anio]=temp

return {
    "datos": datos,
    "geojson": mx_geo
}


