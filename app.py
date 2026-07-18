import streamlit as st

from maps import crear_mapa

st.set_page_config(

    page_title="Diabetes en México",

    page_icon="🩺",

    layout="wide"

)

st.title("🩺 Diabetes en México")

st.write("Dashboard epidemiológico")

from data_loader import cargar_datos

datos = cargar_datos()



