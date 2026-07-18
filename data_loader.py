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
