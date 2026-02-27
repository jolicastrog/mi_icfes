"""
MI ICFES — pages/01_simulador.py
Sprint 1 - HU-01: Esqueleto del formulario (sin prediccion aun)
"""
import streamlit as st
import pandas as pd
from components.gauge    import crear_gauge, obtener_categoria
from components.semaforo import obtener_top_features, mostrar_semaforo
from ai.langchain_advisor import generar_consejo

# ================================================================
# LISTA DE FEATURES — debe coincidir exactamente con el .pkl
# ================================================================
FEATURES = [
    "FAMI_ESTRATOVIVIENDA", "FAMI_TIENEINTERNET", "FAMI_TIENECOMPUTADOR",
    "FAMI_EDUCACIONPADRE",  "FAMI_EDUCACIONMADRE", "ESTU_HORASSEMANATRABAJA",
    "COLE_NATURALEZA", "COLE_AREA_UBICACION", "ESTU_GENERO",
    "FAMI_CUARTOSHOGAR", "FAMI_NUMLIBROS", "COLE_DEPTO_UBICACION",
]

 
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
    # --- 1. Construir el dict con los 12 keys del .pkl ---
    # Los valores deben coincidir exactamente con los usados en entrenamiento.
    # Mapeo: valor del formulario -> valor del CSV ICFES
    form_data = {
        "FAMI_ESTRATOVIVIENDA":    estrato,
        "FAMI_TIENEINTERNET":      internet,
        "FAMI_TIENECOMPUTADOR":    computador,
        "FAMI_EDUCACIONPADRE":     edu_padre,
        "FAMI_EDUCACIONMADRE":     edu_madre,
        "ESTU_HORASSEMANATRABAJA": trabaja,
        "COLE_NATURALEZA":         naturaleza,
        "COLE_AREA_UBICACION":     zona,
        "ESTU_GENERO":             "M",   # simplificado en prototipo
        "FAMI_CUARTOSHOGAR":       3,     # valor por defecto prototipo
        "FAMI_NUMLIBROS":          libros,
        "COLE_DEPTO_UBICACION":    "VALLE DEL CAUCA",  # default prototipo
    }
 
    # --- 2. Spinner durante el calculo ---
    with st.spinner("Analizando tu perfil... esto tarda menos de 10 segundos"):
 
        # --- 3. Crear DataFrame de 1 fila x 12 columnas ---
        df_entrada = pd.DataFrame([form_data])
 
        # --- 4. Prediccion con el pipeline del .pkl ---
        pipeline = st.session_state["pipeline"]
        score = float(pipeline.predict(df_entrada)[0])
        score = max(0.0, min(500.0, score))  # Clamp al rango valido
 
        # --- 5. Categoria del resultado ---
        categoria, color_cat = obtener_categoria(score)
 
        # --- 6. Top-3 variables de mayor impacto ---
        top_features = obtener_top_features(pipeline, FEATURES, n=3)
 
        # --- 7. Perfil resumido para LangChain ---
        perfil_legible = {
            "estrato":   str(estrato),
            "internet":  internet,
            "computador": computador,
            "naturaleza": naturaleza,
            "zona":      zona,
            "horas":     horas,
            "trabaja":   trabaja,
            "edu_padre": edu_padre,
            "edu_madre": edu_madre,
            "libros":    libros,
        }
 
        # --- 8. Llamar a LangChain (GPT-4o-mini) ---
        consejo = generar_consejo(score, perfil_legible, top_features)
 
    # --- 9. Guardar en session_state (disponible en Mi Plan) ---
    st.session_state["score_predicho"] = score
    st.session_state["categoria"]      = categoria
    st.session_state["consejo_ia"]     = consejo
    st.session_state["top_features"]   = top_features
    st.session_state["perfil"]         = perfil_legible

# Boton para volver al inicio
st.markdown("---")
if st.button("\U0001F3E0 Volver al inicio"):
    st.switch_page("app.py")

# Se muestra solo cuando ya hay una prediccion guardada
# ================================================================
if "score_predicho" in st.session_state:
    score     = st.session_state["score_predicho"]
    categoria = st.session_state.get("categoria", "")
    consejo   = st.session_state.get("consejo_ia", "")
    top_feat  = st.session_state.get("top_features", [])

    st.markdown("---")
    st.markdown("## 🎯 Tus Resultados")

    # --- Badge de nivel con color ---
    cat_colores = {
        "Insuficiente": "#FEE2E2",
        "Minimo":       "#FEF3C7",
        "Satisfactorio":"#D4E8FF",
        "Avanzado":     "#D1FAE5",
    }
    bg = cat_colores.get(categoria, "#EEF3FF")
    st.markdown(
        f'<div style="background:{bg};border-radius:10px;padding:12px;'
        f'text-align:center;font-size:22px;font-weight:bold;">'
        f'Nivel: {categoria}  |  {score:.0f} / 500 pts</div>',
        unsafe_allow_html=True
    )
    st.markdown("")

    # --- Gauge chart ---
    fig_gauge = crear_gauge(score)
    st.plotly_chart(fig_gauge, use_container_width=True)

    # --- Rango probable ---
    st.info(
        f"Rango probable: {score-20:.0f} — {score+20:.0f} pts  "
        f"(margen de error del modelo: +/-20 pts)",
        icon="📊"
    )

    # --- Semaforo variables de impacto ---
    if top_feat:
        st.markdown("#### Variables que mas influyen en tu resultado")
        mostrar_semaforo(top_feat)

    # --- Recomendaciones LangChain ---
    if consejo:
        st.markdown("---")
        st.markdown("#### 🤖 Tu Consejero IA dice:")
        st.markdown(
            f'<div style="background:#F0F9F0;border-left:4px solid #059669;'
            f'border-radius:0 8px 8px 0;padding:16px;font-size:15px;">'
            f'{consejo}</div>',
            unsafe_allow_html=True
        )

    # --- Botones de navegacion ---
    st.markdown("---")
    col_p, col_o = st.columns(2)
    with col_p:
        if st.button("📋 Ver mi plan de accion", type="primary",
                     use_container_width=True):
            st.switch_page("pages/04_mi_plan.py")
    with col_o:
        if st.button("📊 Ver Observatorio",
                     use_container_width=True):
            st.switch_page("pages/03_observatorio.py")