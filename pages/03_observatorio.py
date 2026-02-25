"""
MI ICFES — pages/03_observatorio.py
Sprint 1 - HU-01: Layout del Observatorio (datos de ejemplo)
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
 
st.markdown("## \U0001F4CA Observatorio ICFES")
st.markdown("Compara los puntajes de tu departamento con el resto del pais.")
st.markdown("---")
 
# Filtro de tipo de colegio
tipo = st.selectbox(
    "Tipo de colegio:",
    ["Todos", "Oficial", "No Oficial"],
    help="Filtra los datos por naturaleza del colegio"
)
 
# Datos de ejemplo (Sprint 4: reemplazar con datos_resumen_icfes.csv real)
datos_ejemplo = {
    "Departamento": ["Valle del Cauca", "Antioquia", "Bogota", "Cundinamarca",
                     "Santander", "Atlantico", "Bolivar", "Narino"],
    "Promedio": [275, 285, 310, 265, 280, 255, 245, 240]
}
df = pd.DataFrame(datos_ejemplo)
 
# Grafica de barras horizontales
df_sorted = df.sort_values("Promedio")
colores = ["#003087" if p >= 259 else "#94A3B8" for p in df_sorted["Promedio"]]
 
fig = go.Figure(go.Bar(
    x=df_sorted["Promedio"],
    y=df_sorted["Departamento"],
    orientation="h",
    marker_color=colores,
    text=df_sorted["Promedio"],
    textposition="outside"
))
fig.add_vline(x=259, line_dash="dash", line_color="#D97706",
              annotation_text="Promedio nacional: 259", annotation_position="top")
fig.update_layout(
    title="Puntaje Promedio ICFES por Departamento",
    xaxis_title="Puntaje promedio",
    yaxis_title="",
    height=350,
    margin=dict(l=0,r=60,t=60,b=20),
    plot_bgcolor="#FAFAFA",
    paper_bgcolor="#FAFAFA"
)
st.plotly_chart(fig, use_container_width=True)
 
st.caption("Datos de ejemplo — Sprint 4 conectara el CSV real del ICFES")
st.markdown("---")
if st.button("\U0001F3E0 Volver al inicio"):
    st.switch_page("app.py")
