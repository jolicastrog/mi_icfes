"""
MI ICFES — pages/04_mi_plan.py
Sprint 1 - HU-01: Estructura del Plan (placeholder)
"""
import streamlit as st
 
st.markdown("## \U0001F4CB Mi Plan de Accion")
st.markdown("Tu plan personalizado de 8 semanas para mejorar tu puntaje ICFES.")
st.markdown("---")
 
# Verificar si hay un resultado del simulador
score = st.session_state.get("score_predicho", None)
 
if score is None:
    st.warning("Primero haz la simulacion para generar tu plan personalizado.", icon="\u26A0\uFE0F")
    if st.button("Ir al Simulador", type="primary"):
        st.switch_page("pages/01_simulador.py")
else:
    st.success(f"Plan basado en tu puntaje estimado: {score:.0f} pts", icon="\U0001F4AF")
 
# Plan de ejemplo con estructura de 8 semanas
semanas = [
    ("Semana 1-2", "Diagnostico y base matematica",
     ["Resuelve 2 pruebas ICFES anteriores (Khan Academy)", "Identifica tus 3 areas mas debiles", "15 min de matematicas en Duolingo Math diario"]),
    ("Semana 3-4", "Refuerzo en Lectura Critica",
     ["Lee 1 articulo de opinion al dia y resume los argumentos", "Practica comprension lectora en ICFES Interactivo (gratis)", "Escribe 1 parrafo de opinion semanal"]),
    ("Semana 5-6", "Ciencias Naturales y Sociales",
     ["Revisa conceptos clave de biologia y quimica en YouTube (Unicoos)", "Practica preguntas de ciencias sociales ICFES Interactivo", "Forma un grupo de estudio de 2-3 personas"]),
    ("Semana 7-8", "Simulacros y ajuste final",
     ["Haz 2 simulacros completos en tiempo real (3 horas)", "Revisa errores con calma, no memorices respuestas", "Duerme 8 horas los dias previos al examen"]),
]
 
for semana, titulo, actividades in semanas:
    with st.expander(f"\U0001F4C5 {semana}: {titulo}"):
        for actividad in actividades:
            completada = st.checkbox(actividad, key=f"{semana}_{actividad[:20]}")
 
st.markdown("---")
col_g, col_v = st.columns(2)
with col_g:
    if st.button("\U0001F4BE Guardar plan offline", use_container_width=True):
        st.info("Sprint 4: aqui se guardara el plan en LocalStorage.", icon="\U0001F4BE")
with col_v:
    if st.button("\U0001F3E0 Volver al inicio", use_container_width=True):
        st.switch_page("app.py")
