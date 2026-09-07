import streamlit as st

from maps import crear_mapa

from data_loader import cargar_datos

st.set_page_config(

    page_title="Diabetes en México",

    page_icon="🩺",

    layout="wide"

)

st.title("🩺 Diabetes en México")

st.write("Dashboard epidemiológico")

dataset = cargar_datos()

datos = dataset["datos"]
datos_por_anio = dataset["datos_por_anio"]
nacional = dataset["nacional"]
geojson = dataset["geojson"]
anios = dataset["anios"]

st.sidebar.header("Filtros")

anio = st.sidebar.selectbox(
    "Seleccione el año",
    anios
)

df = datos_por_anio[anio]

indicador = st.sidebar.radio(

    "Indicador",

    [

        #"Tasa de detección bruta por 100,000 afiliados al IMSS",

        #"Índice de tasa de detección relativa"

        "Tasa de detección",

        "Índice relativo de tasa de detección (RDI)"

    ]

)

st.sidebar.markdown(
    """
    **Descripción**

    Seleccione un año y un indicador para explorar
    la distribución geográfica de la detección de
    diabetes en México.
    """
)

st.sidebar.caption(
    "Los círculos representan el tamaño de la población."
)

# ============================================================
# DATOS DEL AÑO SELECCIONADO
# ============================================================

df = datos_por_anio[anio]

fig = crear_mapa(
    df,
    geojson,
    indicador
)

st.plotly_chart(
    fig,
    use_container_width=True
)
