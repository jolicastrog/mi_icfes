"""
MI ICFES — pages/04_mi_plan.py
Sprint 3 - HU-08: Plan de accion con LocalStorage offline
"""
import streamlit as st
import streamlit.components.v1 as components
import json
from datetime import datetime

# ================================================================
# FUNCIONES DE LOCALSTORAGE
# ================================================================

def guardar_plan_offline(score: float, consejo: str, fecha: str) -> None:
    """Guarda el plan en LocalStorage del navegador."""
    data = {
        "score": round(score),
        "consejo": consejo,
        "fecha": fecha,
        "version": "sprint3"
    }
    data_json = json.dumps(data, ensure_ascii=False)
    data_json_escaped = data_json.replace("\\", "\\\\").replace("`", "\\`")

    js_code = f"""
    <script>
        try {{
            localStorage.setItem("mi_icfes_plan", `{data_json_escaped}`);
        }} catch(e) {{
            console.error("Error LocalStorage:", e);
        }}
    </script>
    """
    components.html(js_code, height=0)  # height=0, sin UI en el iframe


def mostrar_plan_guardado_offline() -> None:
    """Muestra el plan guardado en LocalStorage si existe."""
    js_leer = """
    <script>
    const plan = localStorage.getItem("mi_icfes_plan");
    if (plan) {
        const data = JSON.parse(plan);
        document.getElementById("plan_offline").innerHTML =
            '<div style="background:#FEF3C7;border-left:4px solid #D97706;'
            + 'padding:12px;border-radius:0 8px 8px 0;">'
            + '<b>Plan guardado offline</b> — Puntaje: ' + data.score + '/500 pts'
            + '<br><small>Guardado el: ' + data.fecha + '</small></div>';
    } else {
        document.getElementById("plan_offline").innerHTML = "";
    }
    </script>
    <div id="plan_offline"></div>
    """
    components.html(js_leer, height=80)


# ================================================================
# CONTENIDO DE LA PAGINA
# ================================================================

st.markdown("## 📋 Mi Plan de Accion")
st.markdown("Tu plan personalizado de 8 semanas para mejorar tu puntaje ICFES.")

# Mostrar si hay un plan guardado offline
mostrar_plan_guardado_offline()

st.markdown("---")

# Verificar si hay score del simulador
score   = st.session_state.get("score_predicho", None)
consejo = st.session_state.get("consejo_ia", "")

if score is None:
    st.warning(
        "Primero haz la simulacion para ver tu plan personalizado.",
        icon="⚠️"
    )
    if st.button("Ir al Simulador", type="primary"):
        st.switch_page("pages/01_simulador.py")
else:
    st.success(f"Plan basado en tu puntaje estimado: {score:.0f} pts", icon="💯")

    # Plan de 8 semanas
    semanas = [
        ("Semana 1-2", "Diagnostico y base matematica", [
            "Resolver 2 pruebas ICFES anteriores disponibles en ICFES Interactivo",
            "Identificar las 3 areas con menor puntaje en las pruebas diagnostico",
            "15 minutos diarios de matematicas en Khan Academy en espanol",
        ]),
        ("Semana 3-4", "Refuerzo en Lectura Critica", [
            "Leer 1 articulo de opinion diario y resumir los argumentos principales",
            "Practicar comprension de lectura con preguntas tipo ICFES Interactivo",
            "Escribir 1 parrafo de opinion semanal sobre temas de actualidad colombiana",
        ]),
        ("Semana 5-6", "Ciencias Naturales y Sociales", [
            "Revisar conceptos de biologia y quimica en YouTube canal Unicoos",
            "Practicar preguntas de ciencias sociales en ICFES Interactivo",
            "Formar grupo de estudio de 2-3 personas para repasar en voz alta",
        ]),
        ("Semana 7-8", "Simulacros y ajuste final", [
            "Hacer 2 simulacros completos en tiempo real (3 horas cada uno)",
            "Revisar cada error con calma, entender el concepto, no solo memorizar",
            "Dormir 8 horas los dias previos al examen. El sueno consolida la memoria",
        ]),
    ]

    for semana, titulo, actividades in semanas:
        with st.expander(f"📅 {semana}: {titulo}"):
            for act in actividades:
                st.checkbox(act, key=f"{semana}_{act[:25]}")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Guardar plan offline", type="primary",
                 use_container_width=True):
            fecha_ahora = datetime.now().strftime("%d/%m/%Y %H:%M")
            guardar_plan_offline(score, consejo, fecha_ahora)
            # Confirmacion con Streamlit nativo (no depende del iframe JS)
            st.success(
                f"Plan guardado correctamente — {fecha_ahora}",
                icon="✅"
            )
    with col2:
        if st.button("🏠 Volver al inicio", use_container_width=True):
            st.switch_page("app.py")
