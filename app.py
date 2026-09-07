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
        "Índice relativo de tasa de detección (IRD)"
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

st.sidebar.caption(
    "La tasa cruda de detección se obtiene dividiendo el número de detecciones de diabetes registradas por el IMSS en una entidad 
    y año determinados entre el número promedio anual de trabajadores afiliados al IMSS de esa misma entidad y año, multiplicado por 100,000."
)

st.sidebar.caption(
    "El índice relativo de tasa de detección compara la tasa cruda de cada entidad con la tasa cruda nacional: Un IRD igual a 1 indica una 
    tasa igual a la nacional; IRD mayor que 1, una tasa superior; y IRD menor que 1, una tasa inferior a la referencia nacional."
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
