"""
MI ICFES — app.py
Sprint 1 - HU-01: App base con navegacion y session state
"""
import streamlit as st
import joblib, json, os
import streamlit.components.v1 as components

st.set_page_config(
    page_title="MI ICFES",
    page_icon="\U0001F393",
    layout="centered",
    initial_sidebar_state="collapsed",
)

def activar_pwa():
    components.html("""
    <link rel="manifest" href="/app/static/manifest.json">
    <script>
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/app/static/sw.js')
                .then(() => console.log('SW registrado'))
                .catch(e => console.log('SW error:', e));
        }
    </script>
    """, height=0)

activar_pwa()

 
# CSS: tema azul, movil-first, ocultar menu de Streamlit
st.markdown("""
<style>
  .block-container { max-width:430px; padding-top:1.5rem; }
  [data-testid="stSidebar"] { background-color:#003087; }
  [data-testid="stSidebar"] .stMarkdown, 
  [data-testid="stSidebar"] .stRadio label { color:#FFFFFF !important; }
  .stButton > button { border-radius:12px; font-weight:600; }
  .stButton > button[kind="primary"] { background:#003087; }
  .metric-container { border-radius:10px; padding:8px; }
  #MainMenu, footer, header { visibility:hidden; }
</style>
""", unsafe_allow_html=True)
 
# ── Cargar modelo una sola vez ──────────────────────────
@st.cache_resource
def cargar_modelo():
    pkl  = "models/modelo_icfes_prototipo.pkl"
    meta = "models/modelo_metadata.json"
    if not os.path.exists(pkl):
        st.error("No se encontro el .pkl en models/")
        st.stop()
    pipeline = joblib.load(pkl)
    with open(meta, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return pipeline, metadata
 
pipeline, metadata = cargar_modelo()
st.session_state["pipeline"] = pipeline
st.session_state["metadata"] = metadata
 
# ── Pagina de inicio ────────────────────────────────────
st.markdown("## \U0001F393 MI ICFES")
st.markdown("**Tu asesor inteligente para el Saber 11**")
st.markdown("---")
 
c1,c2,c3 = st.columns(3)
c1.metric("Estudiantes/ano", "600K", "Colombia")
c2.metric("Promedio nacional", "259", "pts")
c3.metric("Error del modelo", "+/-20", "pts")
 
st.markdown("---")
st.info("Responde 9 preguntas en menos de 2 minutos y descubre tu puntaje estimado Saber 11 con inteligencia artificial.", icon="\U0001F4A1")
 
col_a, col_b = st.columns(2)
with col_a:
    if st.button("\U0001F4DD Hacer simulacion", type="primary", use_container_width=True):
        st.switch_page("pages/01_simulador.py")
with col_b:
    if st.button("\U0001F4CA Ver Observatorio", use_container_width=True):
        st.switch_page("pages/03_observatorio.py")
 
st.markdown("---")
st.caption(f"Modelo: {type(pipeline).__name__} | v0.1 prototipo")
