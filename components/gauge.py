"""
MI ICFES — components/gauge.py
Sprint 2 - T2.4: Velocimetro Plotly para puntaje ICFES 0-500
"""
import plotly.graph_objects as go
 
 
def crear_gauge(score: float) -> go.Figure:
    """
    Crea un velocimetro circular de 0 a 500 para el puntaje ICFES.
 
    Zonas de color:
    - Rojo    [0   - 175): Insuficiente
    - Amarillo[175 - 250): Minimo
    - Azul    [250 - 350): Satisfactorio
    - Verde   [350 - 500]: Avanzado
 
    La linea amarilla marca el promedio nacional: 259 puntos.
    El delta muestra la diferencia vs promedio nacional.
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=round(score, 1),
        domain={"x": [0, 1], "y": [0, 1]},
        title={
            "text": "Puntaje Estimado Saber 11",
            "font": {"size": 18, "color": "#003087"}
        },
        delta={
            "reference": 259,
            "increasing": {"color": "#059669"},
            "decreasing": {"color": "#DC2626"},
            "valueformat": "+.0f",
            "suffix": " vs promedio",
        },
        gauge={
            "axis": {
                "range": [0, 500],
                "tickwidth": 1,
                "tickcolor": "#6B7280",
                "tickvals": [0, 100, 175, 250, 350, 500],
                "ticktext": ["0", "100", "175", "250", "350", "500"],
            },
            "bar": {"color": "#003087", "thickness": 0.25},
            "bgcolor": "white",
            "borderwidth": 2,
            "bordercolor": "#D1D5DB",
            "steps": [
                {"range": [0,   175], "color": "#FFE4E4"},  # Insuficiente
                {"range": [175, 250], "color": "#FFF3CC"},  # Minimo
                {"range": [250, 350], "color": "#D4E8FF"},  # Satisfactorio
                {"range": [350, 500], "color": "#D4F0E8"},  # Avanzado
            ],
            "threshold": {
                "line": {"color": "#F5C518", "width": 4},
                "thickness": 0.75,
                "value": 259,  # Promedio nacional ICFES
            },
        },
    ))
 
    fig.update_layout(
        height=300,
        margin=dict(t=50, b=10, l=20, r=20),
        paper_bgcolor="#FAFAFA",
        font={"family": "Arial", "color": "#111827"},
    )
    return fig
 
 
def obtener_categoria(score: float) -> tuple[str, str]:
    """
    Retorna (nombre_categoria, color_hex) segun el puntaje.
    Categorias oficiales del ICFES Colombia.
    """
    if score < 175:
        return "Insuficiente", "#DC2626"
    elif score < 250:
        return "Minimo", "#D97706"
    elif score < 350:
        return "Satisfactorio", "#0044B8"
    else:
        return "Avanzado", "#059669"
