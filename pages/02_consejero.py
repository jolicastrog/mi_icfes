"""
MI ICFES — pages/02_consejero.py
Sprint 4 - HU-07: Chat conversacional con Pandas DataFrame Agent
sobre datos ICFES reales de Cali.
"""
import streamlit as st
from ai.pandas_agent import crear_agente, preguntar_al_agente

# ================================================================
# CONFIGURACION
# ================================================================
MAX_MENSAJES = 20  # Limite de mensajes en el historial

EJEMPLOS_PREGUNTAS = [
    "Cual es el colegio con mayor puntaje global en 2023?",
    "Cual es la diferencia entre colegios oficiales y privados?",
    "Como esta el estrato 1 vs estrato 6 en puntaje?",
    "Cual es el promedio en matematicas en Cali?",
    "Cuantos colegios hay en los datos?",
    "Cual jornada tiene mejor puntaje: manana o tarde?",
]

# ================================================================
# INTERFAZ
# ================================================================
st.markdown("## Consejero IA — Datos ICFES Cali")
# FIX: un solo string, no dos argumentos separados por coma
st.markdown("Preguntame sobre los resultados del ICFES en Cali. Tengo datos de 30 colegios, por estrato y por area evaluada.")
st.markdown("---")

# Inicializar historial del chat
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": ("Hola! Soy el Consejero de Datos MI ICFES. "
                        "Tengo informacion sobre puntajes ICFES de colegios en Cali, "
                        "diferencias por estrato y rendimiento por area. "
                        "En que te puedo ayudar?"),
        }
    ]

# Mostrar ejemplos de preguntas (solo si el chat esta vacio)
if len(st.session_state.chat_messages) == 1:
    st.markdown("**Ejemplos de preguntas:**")
    cols = st.columns(2)
    for i, ejemplo in enumerate(EJEMPLOS_PREGUNTAS):
        with cols[i % 2]:
            if st.button(ejemplo, key=f"ej_{i}", use_container_width=True):
                st.session_state["pregunta_pendiente"] = ejemplo
                st.rerun()
    st.markdown("---")

# Mostrar historial de mensajes
for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Aviso si se acerca al limite
n_mensajes = len(st.session_state.chat_messages)
if n_mensajes >= MAX_MENSAJES - 4:
    # FIX: icon debe ser un emoji, no el string "warning"
    st.warning(
        f"El chat tiene {n_mensajes} mensajes. Se reiniciara automaticamente al llegar a {MAX_MENSAJES}.",
        icon="⚠️"
    )

# Limpiar chat si supera el limite
if n_mensajes >= MAX_MENSAJES:
    st.session_state.chat_messages = st.session_state.chat_messages[-4:]
    st.info("El historial fue reiniciado para liberar memoria.", icon="ℹ️")

# Procesar pregunta pendiente (de los botones de ejemplo)
pregunta_pendiente = st.session_state.pop("pregunta_pendiente", None)

# Caja de entrada del usuario
user_input = st.chat_input("Escribe tu pregunta sobre los datos ICFES de Cali...")

# Unificar: input manual o boton de ejemplo
pregunta_final = user_input or pregunta_pendiente

if pregunta_final:
    # Guardar mensaje del usuario en historial
    st.session_state.chat_messages.append({"role": "user", "content": pregunta_final})
    with st.chat_message("user"):
        st.write(pregunta_final)

    # Llamar al Pandas Agent
    with st.chat_message("assistant"):
        with st.spinner("El Consejero esta analizando los datos..."):
            agente = crear_agente()
            respuesta = preguntar_al_agente(agente, pregunta_final)
        st.write(respuesta)

    # Guardar respuesta en historial
    st.session_state.chat_messages.append({"role": "assistant", "content": respuesta})

# ================================================================
# PANEL INFORMATIVO (expandible)
# ================================================================
st.markdown("---")
with st.expander("Que datos tengo disponibles?"):
    st.markdown("""
    **Datos de colegios de Cali (2019-2023):**
    - 30 colegios: nombre, naturaleza (Oficial/No Oficial), jornada, area
    - Promedios por: matematicas, lectura critica, ingles, C. naturales, sociales
    - Numero de estudiantes por colegio y periodo

    **Datos por estrato socioeconomico:**
    - Estratos 1 al 6 + Sin estrato
    - Promedios globales y por materia
    - % con internet y computador en casa

    **Datos por area evaluada:**
    - 5 areas: Matematicas, Lectura Critica, Ingles, C. Naturales, Sociales
    - Promedio Cali y por tipo de colegio
    """)

if st.button("Volver al inicio"):
    st.switch_page("app.py")
