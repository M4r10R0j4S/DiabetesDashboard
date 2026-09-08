import streamlit as st

from maps import crear_mapa
from data_loader import cargar_datos
import streamlit as st


# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Diabetes en México)",
    page_icon="🩺",
    layout="wide"
)


# ============================================================
# TÍTULO
# ============================================================

st.title("🩺 Evolución de la Diabetes en México (2000-2020)")

st.write("Dashboard epidemiológico basado en los datos anuales de detecciones del Instituto Mexicano del Seguro Social (IMSS) y su cantidad de afiliados.")


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
    "NOTAS:"
)

st.sidebar.caption(
    "*Los círculos representan el número de afiliados al IMSS."
)

st.sidebar.caption(
    "*La tasa detección (cruda) corresponde al número de detecciones de diabetes por cada 100,000 trabajadores afiliados al IMSS en cada entidad y año."
)

st.sidebar.caption(
    "*El índice relativo de tasa de detección (IRD) compara la tasa cruda de cada entidad con la tasa nacional, calculada a partir del total de detecciones y trabajadores afiliados de las 32 entidades."
)


st.sidebar.markdown(
    """
    <div style="
        text-align: center;
        font-size: 10px;
        color: gray;
    ">
        Desarrollado por el grupo de sistemas biofísicos, Posgrado en Ingeniería de Sistemas, ESIME-IPN, CDMX
    </div>
    """,
    unsafe_allow_html=True
)
st.sidebar.image(
    "IPN_Logo_PNG1.png",
    width=180
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

