"""
MI ICFES — components/semaforo.py
Sprint 2 - T2.5: Visualizacion top-3 variables de impacto
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
 
 
# Traduccion de nombres tecnicos CSV -> preguntas del formulario
NOMBRES_LEGIBLES = {
    "FAMI_ESTRATOVIVIENDA":    "Estrato de tu vivienda",
    "FAMI_TIENEINTERNET":      "Internet en casa",
    "FAMI_TIENECOMPUTADOR":    "Computador o tablet",
    "FAMI_EDUCACIONPADRE":     "Nivel educativo del padre",
    "FAMI_EDUCACIONMADRE":     "Nivel educativo de la madre",
    "ESTU_HORASSEMANATRABAJA": "Horas de trabajo semanal",
    "COLE_NATURALEZA":         "Tipo de colegio (oficial/privado)",
    "COLE_AREA_UBICACION":     "Zona (urbana/rural)",
    "ESTU_GENERO":             "Genero del estudiante",
    "FAMI_CUARTOSHOGAR":       "Cuartos en el hogar",
    "FAMI_NUMLIBROS":          "Libros en el hogar",
    "COLE_DEPTO_UBICACION":    "Departamento del colegio",
}
 
 
def obtener_top_features(pipeline, features: list, n: int = 3) -> list[dict]:
    """
    Extrae las n variables de mayor importancia del pipeline.
    Retorna lista de dicts con: nombre_tecnico, nombre_legible, importancia.
    """
    try:
        model = pipeline.named_steps["model"]
        importancias = model.feature_importances_
    except (KeyError, AttributeError):
        # Fallback si el modelo no tiene feature_importances_ (ej. regresion lineal)
        return [{"tecnico": f, "legible": NOMBRES_LEGIBLES.get(f, f), "importancia": 0.0}
                for f in features[:n]]
 
    indices = np.argsort(importancias)[::-1][:n]
    return [
        {
            "tecnico": features[i],
            "legible": NOMBRES_LEGIBLES.get(features[i], features[i]),
            "importancia": float(importancias[i]),
        }
        for i in indices
    ]
 
 
def mostrar_semaforo(top_features: list[dict]) -> None:
    """
    Renderiza las 3 barras horizontales de impacto con Plotly.
    Colores: mayor importancia = azul oscuro, menor = gris claro.
    """
    if not top_features:
        st.caption("No se pudo calcular la importancia de variables.")
        return
 
    nombres   = [f["legible"]     for f in top_features]
    valores   = [f["importancia"] for f in top_features]
    colores   = ["#003087", "#0044B8", "#94A3B8"][:len(top_features)]
    max_val   = max(valores) if valores else 1
    porcentajes = [round(v / max_val * 100) for v in valores]
 
    fig = go.Figure(go.Bar(
        x=porcentajes,
        y=nombres,
        orientation="h",
        marker_color=colores,
        text=[f"{p}%" for p in porcentajes],
        textposition="outside",
        hovertemplate="%{y}: %{x}% de impacto relativo<extra></extra>",
    ))
    fig.update_layout(
        title={
            "text": "Variables que mas influyen en tu puntaje",
            "font": {"size": 14, "color": "#003087"},
        },
        xaxis=dict(range=[0, 130], showticklabels=False, showgrid=False),
        yaxis=dict(autorange="reversed"),
        height=200,
        margin=dict(t=40, b=10, l=5, r=20),
        paper_bgcolor="#FAFAFA",
        plot_bgcolor="#FAFAFA",
    )
    st.plotly_chart(fig, use_container_width=True)
