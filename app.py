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

geojson = dataset["geojson"]

st.sidebar.header("Filtros")

anio = st.sidebar.selectbox(

    "Seleccione el año",

    [2000,2010,2020]

)

indicador = st.sidebar.radio(

    "Indicador",

    [

        "Tasa de detección bruta por 100,000 afiliados al IMSS",

        "Índice de tasa de detección relativa"

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

df = datos[anio]

fig = crear_mapa(
    df,
    geojson,
    indicador
)

st.plotly_chart(
    fig,
    use_container_width=True
)
