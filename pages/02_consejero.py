"""
MI ICFES — pages/02_consejero.py
Sprint 1 - HU-01: Layout del chat (sin LangChain aun)
"""
import streamlit as st
 
st.markdown("## \U0001F916 Consejero IA")
st.markdown("Preguntame sobre los datos ICFES de tu departamento o sobre tu resultado.")
st.markdown("---")
 
# Inicializar historial del chat en session_state
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant",
         "content": "Hola! Soy el Consejero MI ICFES. Puedo ayudarte a entender tu puntaje o a consultar datos del ICFES de tu departamento. En que te puedo ayudar?"}
    ]
 
# Mostrar historial de mensajes
for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
 
# Caja de entrada del usuario
user_input = st.chat_input("Escribe tu pregunta aqui...")
 
if user_input:
    # Guardar mensaje del usuario
    st.session_state.chat_messages.append({"role":"user","content":user_input})
    with st.chat_message("user"):
        st.write(user_input)
 
    # Respuesta placeholder (Sprint 3: reemplazar con LangChain)
    with st.chat_message("assistant"):
        with st.spinner("El Consejero IA esta pensando..."):
            import time; time.sleep(1)
            respuesta = f"Entendido. En el Sprint 3 conectare esta respuesta a los datos reales del ICFES usando LangChain. Tu pregunta fue: \"{user_input}\""
            st.write(respuesta)
    st.session_state.chat_messages.append({"role":"assistant","content":respuesta})
 
st.markdown("---")
if st.button("\U0001F3E0 Volver al inicio"):
    st.switch_page("app.py")
