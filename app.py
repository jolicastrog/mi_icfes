"""
MI ICFES — Plataforma PWA de Predicción Saber 11
app.py — Punto de entrada principal
Sprint 1 — HU-02: Estructura base Streamlit
"""

import streamlit as st
import joblib
import json
import os

# ── Configuración de página ─────────────────────────────────
st.set_page_config(
    page_title="MI ICFES",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "MI ICFES v0.1 — Simulador inteligente Saber 11 🇨🇴"
    }
)

# ── CSS personalizado para móvil ────────────────────────────
st.markdown("""
<style>
    .block-container { max-width: 430px; padding-top: 2rem; }
    .stButton > button { border-radius: 12px; font-weight: 600; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Carga del modelo (una sola vez, en caché) ───────────────
@st.cache_resource
def cargar_modelo():
    """Carga el pipeline .pkl y el metadata.json al iniciar."""
    pkl_path  = "models/modelo_icfes_prototipo.pkl"
    meta_path = "models/modelo_metadata.json"

    if not os.path.exists(pkl_path):
        st.error("❌ No se encontró el modelo. Verifica que modelo_icfes_prototipo.pkl esté en models/")
        st.stop()

    pipeline = joblib.load(pkl_path)

    with open(meta_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    return pipeline, metadata


pipeline, metadata = cargar_modelo()

# Disponible para todas las páginas vía session_state
st.session_state["pipeline"] = pipeline
st.session_state["metadata"] = metadata

# ── Pantalla de bienvenida ──────────────────────────────────
st.markdown("## 🎓 MI ICFES")
st.markdown("### Tu asesor inteligente para el Saber 11")
st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Estudiantes/año", "600K", "Colombia")
with col2:
    st.metric("Promedio nacional", "259", "pts")
with col3:
    st.metric("Error del modelo", "±20", "pts MAE")

st.markdown("---")
st.markdown("""
**¿Cómo funciona?**
1. 📝 Respondes 9 preguntas sobre tu contexto (menos de 2 min)
2. 🤖 La IA predice tu puntaje Saber 11
3. 📊 Ves tu posición frente a otros colegios de tu región
4. 💡 Recibes un plan de acción personalizado
""")

st.markdown("---")

if st.button("🚀 Iniciar simulador", type="primary", use_container_width=True):
    st.switch_page("pages/01_simulador.py")

st.markdown("---")
st.caption("⚠️ Modelo prototipo v0.1 — En espera del modelo definitivo del equipo ML")
st.caption(f"Pipeline cargado: {type(pipeline.named_steps.get('model', pipeline)).__name__}")