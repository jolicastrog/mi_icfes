"""
MI ICFES — pages/01_simulador.py
Sprint 1 - HU-01: Esqueleto del formulario (sin prediccion aun)
"""
import streamlit as st
 
st.markdown("## \U0001F4DD Simulador ICFES")
st.markdown("Responde las preguntas sobre tu contexto para predecir tu puntaje.")
st.markdown("---")
 
with st.form("formulario_icfes"):
    col1, col2 = st.columns(2)
 
    with col1:
        st.markdown("**Tu entorno familiar**")
        estrato = st.selectbox(
            "Estrato de tu vivienda",
            options=[1, 2, 3, 4, 5, 6],
            help="El estrato aparece en el recibo del servicio publico"
        )
        internet = st.radio(
            "Internet en casa",
            options=["Si siempre", "A veces", "No tengo"],
            horizontal=True
        )
        computador = st.radio(
            "Computador o tablet",
            options=["Si", "No"],
            horizontal=True
        )
        naturaleza = st.radio(
            "Tu colegio es:",
            options=["Oficial", "No Oficial"],
            horizontal=True
        )
        zona = st.radio(
            "Zona donde vives:",
            options=["Urbana", "Rural"],
            horizontal=True
        )
 
    with col2:
        st.markdown("**Tus habitos de estudio**")
        horas = st.slider(
            "Horas de estudio extra por semana",
            min_value=0, max_value=40, value=10,
            help="Horas fuera del horario del colegio"
        )
        trabaja = st.selectbox(
            "Horas de trabajo semanal",
            options=[0, 5, 15, 25],
            format_func=lambda x: "No trabajo" if x==0 else f"{x} horas/semana"
        )
        edu_padre = st.selectbox(
            "Nivel educativo del padre",
            ["Primaria", "Secundaria", "Tecnico", "Universidad", "Postgrado"]
        )
        edu_madre = st.selectbox(
            "Nivel educativo de la madre",
            ["Primaria", "Secundaria", "Tecnico", "Universidad", "Postgrado"]
        )
        libros = st.selectbox(
            "Libros en tu hogar",
            ["0 a 10", "11 a 25", "26 a 100", "Mas de 100"]
        )
 
    submitted = st.form_submit_button(
        "\U0001F680 Calcular mi puntaje",
        type="primary",
        use_container_width=True
    )
 
if submitted:
    st.info("Sprint 2 conectara este formulario al modelo ML. Aqui apareceran los resultados.", icon="\u23F3")
 
# Boton para volver al inicio
st.markdown("---")
if st.button("\U0001F3E0 Volver al inicio"):
    st.switch_page("app.py")
