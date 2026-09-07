import streamlit as st

from maps import crear_mapa
from data_loader import cargar_datos


# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Diabetes en México",
    page_icon="🩺",
    layout="wide"
)


# ============================================================
# TÍTULO
# ============================================================

st.title("🩺 Diabetes en México")

st.write("Dashboard epidemiológico")


# ============================================================
# CARGAR DATOS
# ============================================================

dataset = cargar_datos()

datos = dataset["datos"]
datos_por_anio = dataset["datos_por_anio"]
nacional = dataset["nacional"]
geojson = dataset["geojson"]
anios = dataset["anios"]


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("Filtros")


# ============================================================
# SELECTOR DE AÑO
# ============================================================

anio = st.sidebar.selectbox(
    "Seleccione el año",
    anios
)


# ============================================================
# SELECTOR DE INDICADOR
# ============================================================

indicador = st.sidebar.radio(
    "Indicador",
    [
        "Tasa de detección",
        "Índice relativo de tasa de detección (RDI)"
    ]
)


# ============================================================
# TEXTO INFORMATIVO
# ============================================================

st.sidebar.markdown(
    """
    **Descripción**

    Seleccione un año y un indicador para explorar
    la distribución geográfica de la detección de
    diabetes en México.
    """
)


st.sidebar.caption(
    "Los círculos representan el número de afiliados al IMSS."
)


# ============================================================
# DATOS DEL AÑO SELECCIONADO
# ============================================================

df = datos_por_anio[anio]


# ============================================================
# CREAR MAPA
# ============================================================

fig = crear_mapa(
    df,
    geojson,
    indicador
)


# ============================================================
# MOSTRAR MAPA
# ============================================================

st.plotly_chart(
    fig,
    use_container_width=True
)
