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

