# ============================================================
# DATA LOADER
# Diabetes en México - IMSS
#
# Archivos de entrada:
#   detectados.csv
#   afiliados.csv
#
# Periodo utilizado:
#   2000 - 2020
#
# Indicadores:
#
#   Tasa bruta =
#       casos detectados / afiliados * 100000
#
#   RDI =
#       tasa estatal / tasa nacional
#
# ============================================================


# ============================================================
# LIBRERÍAS
# ============================================================

import numpy as np
import pandas as pd
import requests
import unicodedata

from shapely.geometry import shape


# ============================================================
# CONFIGURACIÓN
# ============================================================

CSV_CASOS = "detectados.csv"

CSV_AFILIADOS = "afiliados.csv"


GEOJSON_URL = (
    "https://raw.githubusercontent.com/"
    "angelnmara/geojson/master/mexicoHigh.json"
)


# Solo se utilizarán los años 2000 a 2020

ANIOS = list(range(2000, 2021))


# ============================================================
# NORMALIZAR TEXTO
# ============================================================

def normalizar_texto(texto):

    """
    Normaliza nombres de entidades para poder comparar
    los nombres de los CSV con los nombres del GeoJSON.
    """

    texto = str(texto).strip().lower()

    texto = unicodedata.normalize(
        "NFKD",
        texto
    )

    texto = "".join(
        caracter
        for caracter in texto
        if not unicodedata.combining(caracter)
    )

    texto = " ".join(
        texto.split()
    )

    return texto


# ============================================================
# CONVERTIR DATOS NUMÉRICOS
# ============================================================

def convertir_numerico(serie):

    """
    Convierte valores como:

    123456
    123,456
    "123456 "
    valores vacíos

    en números.
    """

    return pd.to_numeric(

        serie
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace(" ", "", regex=False)
        .replace(
            {
                "nan": np.nan,
                "": np.nan,
                "-": np.nan,
                "NA": np.nan,
                "N/A": np.nan
            }
        ),

        errors="coerce"
    )


# ============================================================
# CLASIFICACIÓN DEL RDI
# ============================================================

def clasificar_rdi_old(valor):

    if pd.isna(valor):

        return "Sin datos"

    if valor < 0.80:

        return "Muy por debajo del nacional"

    elif valor < 0.95:

        return "Por debajo del nacional"

    elif valor <= 1.05:

        return "Similar al nacional"

    elif valor <= 1.20:

        return "Por encima del nacional"

    else:

        return "Muy por encima del nacional"


def clasificar_rdi(valor):

    if pd.isna(valor):

        return "Sin datos"

    elif valor < 0.95:

        return "Por debajo del nacional"

    elif valor <= 1.05:

        return "Similar al nacional"

    else:

        return "Por encima del nacional"


# ============================================================
# CLASIFICAR TASA EN CINCO NIVELES
# ============================================================

def clasificar_tasa(serie):

    """
    Clasifica las tasas estatales utilizando quintiles.

    La clasificación se realiza independientemente
    para cada año.
    """

    q20, q40, q60, q80 = serie.quantile(
        [0.20, 0.40, 0.60, 0.80]
    )

    categorias = []

    for valor in serie:

        if pd.isna(valor):

            categorias.append("Sin datos")

        elif valor <= q20:

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


# ============================================================
# NIVELES NUMÉRICOS PARA LOS MAPAS
# ============================================================

NIVEL_TASA = {

    "Muy bajo": 1,

    "Bajo": 2,

    "Medio": 3,

    "Alto": 4,

    "Muy alto": 5
}


NIVEL_RDI_old = {

    "Muy por debajo del nacional": 1,

    "Por debajo del nacional": 2,

    "Similar al nacional": 3,

    "Por encima del nacional": 4,

    "Muy por encima del nacional": 5
}

NIVEL_RDI = {
    "Por debajo del nacional": 1,
    "Similar al nacional": 2,
    "Por encima del nacional": 3
}


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def cargar_datos():

    # ========================================================
    # CARGAR CSV
    # ========================================================

    df_casos = pd.read_csv(
        CSV_CASOS
    )

    df_afiliados = pd.read_csv(
        CSV_AFILIADOS
    )


    # ========================================================
    # LIMPIAR NOMBRES DE COLUMNAS
    # ========================================================

    df_casos.columns = (
        df_casos.columns
        .astype(str)
        .str.strip()
    )

    df_afiliados.columns = (
        df_afiliados.columns
        .astype(str)
        .str.strip()
    )


    # ========================================================
    # IDENTIFICAR COLUMNA DE ENTIDAD
    # ========================================================

    if "entidad" not in df_casos.columns:

        df_casos = df_casos.rename(
            columns={
                df_casos.columns[0]:
                "entidad"
            }
        )


    if "entidad" not in df_afiliados.columns:

        df_afiliados = df_afiliados.rename(
            columns={
                df_afiliados.columns[0]:
                "entidad"
            }
        )


    # ========================================================
    # ELIMINAR REGISTROS SIN ENTIDAD
    # ========================================================

    df_casos = df_casos.dropna(
        subset=["entidad"]
    )

    df_afiliados = df_afiliados.dropna(
        subset=["entidad"]
    )


    # ========================================================
    # LIMPIAR NOMBRES DE ENTIDAD
    # ========================================================

    df_casos["entidad"] = (
        df_casos["entidad"]
        .astype(str)
        .str.strip()
    )

    df_afiliados["entidad"] = (
        df_afiliados["entidad"]
        .astype(str)
        .str.strip()
    )


    # ========================================================
    # VALIDAR AÑOS
    # ========================================================

    for anio in ANIOS:

        columna = str(anio)

        if columna not in df_casos.columns:

            raise ValueError(
                f"No existe la columna {columna} "
                "en detectados.csv"
            )

        if columna not in df_afiliados.columns:

            raise ValueError(
                f"No existe la columna {columna} "
                "en afiliados.csv"
            )


        # Convertir valores numéricos

        df_casos[columna] = convertir_numerico(
            df_casos[columna]
        )

        df_afiliados[columna] = convertir_numerico(
            df_afiliados[columna]
        )


    # ========================================================
    # CREAR CLAVE NORMALIZADA
    # ========================================================

    df_casos["clave_entidad"] = (
        df_casos["entidad"]
        .apply(normalizar_texto)
    )

    df_afiliados["clave_entidad"] = (
        df_afiliados["entidad"]
        .apply(normalizar_texto)
    )


    # ========================================================
    # CONVERTIR CASOS A FORMATO LARGO
    # ========================================================

    casos_long = df_casos.melt(

        id_vars=[
            "entidad",
            "clave_entidad"
        ],

        value_vars=[
            str(anio)
            for anio in ANIOS
        ],

        var_name="anio",

        value_name="casos"
    )


    casos_long["anio"] = (
        casos_long["anio"]
        .astype(int)
    )


    # ========================================================
    # CONVERTIR AFILIADOS A FORMATO LARGO
    # ========================================================

    afiliados_long = df_afiliados.melt(

        id_vars=[
            "entidad",
            "clave_entidad"
        ],

        value_vars=[
            str(anio)
            for anio in ANIOS
        ],

        var_name="anio",

        value_name="afiliados"
    )


    afiliados_long["anio"] = (
        afiliados_long["anio"]
        .astype(int)
    )


    # ========================================================
    # UNIR CASOS Y AFILIADOS
    # ========================================================

    datos = pd.merge(

        casos_long[
            [
                "entidad",
                "clave_entidad",
                "anio",
                "casos"
            ]
        ],

        afiliados_long[
            [
                "clave_entidad",
                "anio",
                "afiliados"
            ]
        ],

        on=[
            "clave_entidad",
            "anio"
        ],

        how="inner"
    )


    # ========================================================
    # CALCULAR TASA BRUTA
    # ========================================================

    datos["tasa"] = np.where(

        datos["afiliados"] > 0,

        (
            datos["casos"]
            /
            datos["afiliados"]
        )
        * 100000,

        np.nan
    )


    # ========================================================
    # CALCULAR DATOS NACIONALES
    # ========================================================

    nacional = (

        datos

        .groupby(
            "anio",
            as_index=False
        )

        .agg(

            casos_nacional=(
                "casos",
                "sum"
            ),

            afiliados_nacional=(
                "afiliados",
                "sum"
            )
        )
    )


    # ========================================================
    # CALCULAR TASA NACIONAL
    # ========================================================

    nacional["tasa_nacional"] = np.where(

        nacional["afiliados_nacional"] > 0,

        (
            nacional["casos_nacional"]
            /
            nacional["afiliados_nacional"]
        )
        * 100000,

        np.nan
    )


    # ========================================================
    # AGREGAR DATOS NACIONALES
    # ========================================================

    datos = pd.merge(

        datos,

        nacional,

        on="anio",

        how="left"
    )


    # ========================================================
    # CALCULAR RDI
    # ========================================================

    datos["rdi"] = np.where(

        datos["tasa_nacional"] > 0,

        (
            datos["tasa"]
            /
            datos["tasa_nacional"]
        ),

        np.nan
    )


    # ========================================================
    # CLASIFICAR RDI
    # ========================================================

    datos["categoria_rdi"] = (
        datos["rdi"]
        .apply(clasificar_rdi)
    )


    datos["nivel_rdi"] = (
        datos["categoria_rdi"]
        .map(NIVEL_RDI)
    )


    # ========================================================
    # DESCARGAR GEOJSON
    # ========================================================

    respuesta = requests.get(
        GEOJSON_URL,
        timeout=30
    )

    respuesta.raise_for_status()

    mx_geo = respuesta.json()


    # ========================================================
    # NOMBRES DEL GEOJSON
    # ========================================================

    geo_nombres = {}

    for feature in mx_geo["features"]:

        nombre = (
            feature["properties"]["name"]
        )

        clave = normalizar_texto(
            nombre
        )

        geo_nombres[clave] = nombre


    # ========================================================
    # EQUIVALENCIAS
    # ========================================================

    equivalencias = {

        "ciudad de mexico":
            "distrito federal",

        "cdmx":
            "distrito federal",

        "estado de mexico":
            "mexico",

        "coahuila":
            "coahuila de zaragoza",

        "michoacan":
            "michoacan de ocampo",

        "veracruz":
            "veracruz de ignacio de la llave"
    }


    # ========================================================
    # BUSCAR NOMBRE DEL GEOJSON
    # ========================================================

    def obtener_nombre_geo(entidad):

        clave = normalizar_texto(
            entidad
        )

        # Coincidencia directa

        if clave in geo_nombres:

            return geo_nombres[clave]


        # Equivalencia

        if clave in equivalencias:

            clave_equivalente = (
                equivalencias[clave]
            )

            if clave_equivalente in geo_nombres:

                return geo_nombres[
                    clave_equivalente
                ]


        # Equivalencia inversa

        for origen, destino in equivalencias.items():

            if clave == destino:

                if origen in geo_nombres:

                    return geo_nombres[
                        origen
                    ]


        return np.nan


    # ========================================================
    # ASIGNAR NOMBRE GEOJSON
    # ========================================================

    datos["entidad_geo"] = (

        datos["entidad"]
        .apply(obtener_nombre_geo)
    )


    # ========================================================
    # VALIDAR ENTIDADES
    # ========================================================

    faltantes = (

        datos.loc[
            datos["entidad_geo"].isna(),
            "entidad"
        ]

        .drop_duplicates()

        .tolist()
    )


    if faltantes:

        print(
            "Entidades no encontradas en GeoJSON:"
        )

        for entidad in faltantes:

            print(
                "-",
                entidad
            )


    # Eliminar únicamente registros sin geometría

    datos = datos.dropna(
        subset=["entidad_geo"]
    )


    # ========================================================
    # CALCULAR CENTROIDES
    # ========================================================

    centroides = {}

    for feature in mx_geo["features"]:

        nombre = (
            feature["properties"]["name"]
        )

        geometria = shape(
            feature["geometry"]
        )

        punto = (
            geometria
            .representative_point()
        )

        centroides[nombre] = (
            punto.x,
            punto.y
        )


    # ========================================================
    # AGREGAR COORDENADAS
    # ========================================================

    datos["lon"] = (

        datos["entidad_geo"]
        .map(
            lambda x:
            centroides[x][0]
        )
    )


    datos["lat"] = (

        datos["entidad_geo"]
        .map(
            lambda x:
            centroides[x][1]
        )
    )


    # ========================================================
    # TAMAÑO GLOBAL DE LOS CÍRCULOS
    # ========================================================

    afiliados_max = (
        datos["afiliados"]
        .max()
    )


    if (
        pd.isna(afiliados_max)
        or afiliados_max <= 0
    ):

        datos["tamano"] = 8

    else:

        datos["tamano"] = (

            np.sqrt(
                datos["afiliados"]
                .fillna(0)
                /
                afiliados_max
            )

            * 40

            + 6
        )


    # ========================================================
    # CLASIFICAR TASA POR AÑO
    # ========================================================

    datos["categoria_tasa"] = None


    for anio in ANIOS:

        mascara = (
            datos["anio"] == anio
        )

        datos.loc[
            mascara,
            "categoria_tasa"
        ] = clasificar_tasa(

            datos.loc[
                mascara,
                "tasa"
            ]
        )


    datos["nivel_tasa"] = (

        datos["categoria_tasa"]
        .map(NIVEL_TASA)
    )


    # ========================================================
    # CREAR HOVER PARA TASA
    # ========================================================

    datos["hover_tasa"] = (

        "<b>"
        + datos["entidad"]
        + "</b>"

        + "<br>Año: "
        + datos["anio"].astype(str)

        + "<br><br>Casos detectados: "
        + datos["casos"].map(
            lambda x:
            f"{x:,.0f}"
            if pd.notna(x)
            else "Sin datos"
        )

        + "<br>Afiliados IMSS: "
        + datos["afiliados"].map(
            lambda x:
            f"{x:,.0f}"
            if pd.notna(x)
            else "Sin datos"
        )

        + "<br><b>Tasa bruta: </b>"
        + datos["tasa"].map(
            lambda x:
            f"{x:,.2f}"
            if pd.notna(x)
            else "Sin datos"
        )

        + " por 100,000 afiliados"

        + "<br>Nivel: "
        + datos["categoria_tasa"]
        .fillna("Sin datos")
    )


    # ========================================================
    # CREAR HOVER PARA RDI
    # ========================================================

    datos["hover_rdi"] = (

        "<b>"
        + datos["entidad"]
        + "</b>"

        + "<br>Año: "
        + datos["anio"].astype(str)

        + "<br><br>Casos detectados: "
        + datos["casos"].map(
            lambda x:
            f"{x:,.0f}"
            if pd.notna(x)
            else "Sin datos"
        )

        + "<br>Afiliados IMSS: "
        + datos["afiliados"].map(
            lambda x:
            f"{x:,.0f}"
            if pd.notna(x)
            else "Sin datos"
        )

        + "<br>Tasa estatal: "
        + datos["tasa"].map(
            lambda x:
            f"{x:,.2f}"
            if pd.notna(x)
            else "Sin datos"
        )

        + "<br>Tasa nacional: "
        + datos["tasa_nacional"].map(
            lambda x:
            f"{x:,.2f}"
            if pd.notna(x)
            else "Sin datos"
        )

        + "<br><b>IRD: </b>"
        + datos["rdi"].map(
            lambda x:
            f"{x:.3f}"
            if pd.notna(x)
            else "Sin datos"
        )

        + "<br>"
        + datos["categoria_rdi"]
        .fillna("Sin datos")
    )


    # ========================================================
    # CREAR DICCIONARIO POR AÑO
    # ========================================================

    datos_por_anio = {}


    for anio in ANIOS:

        datos_por_anio[anio] = (

            datos[
                datos["anio"] == anio
            ]

            .copy()

            .reset_index(drop=True)
        )


    # ========================================================
    # REGRESAR DATOS
    # ========================================================

    return {

        "datos":
            datos,

        "datos_por_anio":
            datos_por_anio,

        "nacional":
            nacional,

        "geojson":
            mx_geo,

        "anios":
            ANIOS
    }
