"""
MI ICFES — pages/03_observatorio.py
Sprint 3 - HU-07: Observatorio Regional ICFES Cali
Datos basados en estadisticas reales ICFES Colombia 2019-2023
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

# ================================================================
# CONFIGURACION Y CARGA DE DATOS
# ================================================================

PROMEDIO_CALI   = 261.3
PROMEDIO_NACION = 259.0

st.markdown("## 🔭 Observatorio ICFES — Cali")
st.markdown("Conoce como esta tu ciudad, tu tipo de colegio y tu estrato en el Saber 11.")
st.markdown("---")

@st.cache_data
def cargar_colegios() -> pd.DataFrame:
    ruta = "data/datos_resumen_colegios_cali.csv"
    if not os.path.exists(ruta):
        return pd.DataFrame()
    return pd.read_csv(ruta)

@st.cache_data
def cargar_estrato() -> pd.DataFrame:
    ruta = "data/datos_resumen_estrato_cali.csv"
    if not os.path.exists(ruta):
        return pd.DataFrame()
    return pd.read_csv(ruta)

@st.cache_data
def cargar_areas() -> pd.DataFrame:
    ruta = "data/datos_areas_cali.csv"
    if not os.path.exists(ruta):
        return pd.DataFrame()
    return pd.read_csv(ruta)

df_col = cargar_colegios()
df_est = cargar_estrato()
df_are = cargar_areas()

if df_col.empty or df_est.empty or df_are.empty:
    st.error(
        "Archivos de datos no encontrados. "
        "Verificar que existen en la carpeta data/: "
        "datos_resumen_colegios_cali.csv, "
        "datos_resumen_estrato_cali.csv, "
        "datos_areas_cali.csv"
    )
    st.stop()

PERIODOS_DISP = sorted(df_col["PERIODO"].unique(), reverse=True)
PERIODO_LABELS = {p: f"{str(p)[:4]}-{str(p)[4:]}" for p in PERIODOS_DISP}

# ================================================================
# FILTROS GLOBALES
# ================================================================
col_f1, col_f2 = st.columns(2)
with col_f1:
    periodo_sel = st.selectbox(
        "📅 Periodo",
        options=PERIODOS_DISP,
        format_func=lambda p: PERIODO_LABELS[p],
    )
with col_f2:
    tipo_sel = st.selectbox(
        "🏫 Tipo de colegio",
        options=["Todos", "Oficial", "No Oficial"],
    )

# ================================================================
# METRICAS RAPIDAS — fila de KPIs
# ================================================================
st.markdown("---")

df_periodo = df_col[df_col["PERIODO"] == periodo_sel].copy()
if tipo_sel != "Todos":
    df_periodo = df_periodo[df_periodo["COLE_NATURALEZA"] == tipo_sel]

prom_periodo  = df_periodo["PROMEDIO_GLOBAL"].mean()
prom_oficial  = df_col[(df_col["PERIODO"]==periodo_sel) & (df_col["COLE_NATURALEZA"]=="Oficial")]["PROMEDIO_GLOBAL"].mean()
prom_privado  = df_col[(df_col["PERIODO"]==periodo_sel) & (df_col["COLE_NATURALEZA"]=="No Oficial")]["PROMEDIO_GLOBAL"].mean()
brecha_tipo   = prom_privado - prom_oficial

k1, k2, k3, k4 = st.columns(4)
with k1:
    delta_nac = prom_periodo - PROMEDIO_NACION
    st.metric(
        "Promedio Cali",
        f"{prom_periodo:.0f} pts",
        delta=f"{delta_nac:+.0f} vs nacion",
    )
with k2:
    st.metric("Colegios Oficiales", f"{prom_oficial:.0f} pts")
with k3:
    st.metric("Colegios Privados", f"{prom_privado:.0f} pts")
with k4:
    st.metric(
        "Brecha Oficial vs Privado",
        f"{brecha_tipo:.0f} pts",
        delta=f"{'Privado supera' if brecha_tipo>0 else 'Oficial supera'}",
        delta_color="off",
    )

st.markdown("---")

# ================================================================
# SECCION 1 — RANKING DE COLEGIOS
# ================================================================
st.markdown("### 🏆 Ranking de colegios — ¿Cómo está tu colegio?")
st.caption(
    "Puedes buscar tu colegio en la tabla o verlo en la gráfica. "
    "Azul oscuro = sobre el promedio de Cali."
)

df_rank = df_periodo.copy()
df_rank = df_rank.sort_values("PROMEDIO_GLOBAL", ascending=False).reset_index(drop=True)
df_rank["POSICION"] = df_rank.index + 1

# Top 20 para la grafica
df_top20 = df_rank.head(20).sort_values("PROMEDIO_GLOBAL", ascending=True)
colores_rank = [
    "#003087" if v >= PROMEDIO_CALI else "#94A3B8"
    for v in df_top20["PROMEDIO_GLOBAL"]
]

fig_rank = go.Figure(go.Bar(
    x=df_top20["PROMEDIO_GLOBAL"],
    y=df_top20["COLE_NOMBRE_ESTABLECIMIENTO"],
    orientation="h",
    marker_color=colores_rank,
    text=df_top20["PROMEDIO_GLOBAL"].round(0).astype(int),
    textposition="outside",
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Puntaje: %{x:.0f} pts<br>"
        "<extra></extra>"
    ),
))
fig_rank.add_vline(
    x=PROMEDIO_CALI,
    line_dash="dot",
    line_color="#F5C518",
    line_width=2,
    annotation_text=f"Promedio Cali: {PROMEDIO_CALI}",
    annotation_position="top right",
    annotation_font_color="#D97706",
)
fig_rank.update_layout(
    title=f"Top 20 colegios — Periodo {PERIODO_LABELS[periodo_sel]}",
    height=520,
    margin=dict(t=50, b=20, l=10, r=70),
    paper_bgcolor="#FAFAFA",
    plot_bgcolor="#FAFAFA",
    xaxis=dict(range=[200, df_top20["PROMEDIO_GLOBAL"].max() + 30]),
)
st.plotly_chart(fig_rank, use_container_width=True)

# Tabla completa buscable
with st.expander("📋 Ver tabla completa de colegios"):
    df_tabla = df_rank[["POSICION","COLE_NOMBRE_ESTABLECIMIENTO",
                         "COLE_NATURALEZA","COLE_JORNADA",
                         "PROMEDIO_GLOBAL","PROMEDIO_MATEMATICAS",
                         "PROMEDIO_LECTURA","PROMEDIO_INGLES",
                         "NUM_ESTUDIANTES"]].copy()
    df_tabla.columns = ["#","Colegio","Tipo","Jornada",
                         "Global","Matematicas","Lectura","Ingles","Estudiantes"]
    st.dataframe(df_tabla, use_container_width=True, hide_index=True)

# Comparacion con score del usuario
if "score_predicho" in st.session_state:
    score_u = st.session_state["score_predicho"]
    colegios_superados = (df_rank["PROMEDIO_GLOBAL"] < score_u).sum()
    total_col = len(df_rank)
    percentil = colegios_superados / total_col * 100
    categoria_u = st.session_state.get("categoria", "")
    st.success(
        f"🎯 Tu puntaje estimado **{score_u:.0f} pts** supera al promedio de "
        f"**{colegios_superados} de {total_col} colegios** ({percentil:.0f}%) "
        f"en este periodo. Nivel: **{categoria_u}**",
        icon="🏅"
    )

st.markdown("---")

# ================================================================
# SECCION 2 — BRECHA SOCIOECONOMICA POR ESTRATO
# ================================================================
st.markdown("### 📊 Brecha socioeconómica — El estrato sí importa")
st.caption(
    "Esta grafica muestra cuanto impacta el estrato en el puntaje ICFES en Cali. "
    "La linea amarilla es el promedio de la ciudad (261 pts)."
)

df_est_per = df_est[df_est["PERIODO"] == periodo_sel].copy()

# Orden logico de estratos
orden_estratos = ["Sin Estrato","Estrato 1","Estrato 2",
                  "Estrato 3","Estrato 4","Estrato 5","Estrato 6"]
df_est_per["ORDEN"] = df_est_per["FAMI_ESTRATOVIVIENDA"].map(
    {e: i for i, e in enumerate(orden_estratos)}
).fillna(99)
df_est_per = df_est_per.sort_values("ORDEN")

col_b1, col_b2 = st.columns([3, 2])

with col_b1:
    colores_est = [
        "#003087" if v >= PROMEDIO_CALI else "#94A3B8"
        for v in df_est_per["PROMEDIO_GLOBAL"]
    ]
    fig_est = go.Figure(go.Bar(
        x=df_est_per["FAMI_ESTRATOVIVIENDA"],
        y=df_est_per["PROMEDIO_GLOBAL"],
        marker_color=colores_est,
        text=df_est_per["PROMEDIO_GLOBAL"].round(0).astype(int),
        textposition="outside",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Puntaje promedio: %{y:.0f} pts<br>"
            "<extra></extra>"
        ),
    ))
    fig_est.add_hline(
        y=PROMEDIO_CALI,
        line_dash="dot",
        line_color="#F5C518",
        line_width=2,
        annotation_text=f"Promedio Cali: {PROMEDIO_CALI}",
        annotation_position="top right",
        annotation_font_color="#D97706",
    )
    fig_est.update_layout(
        title="Puntaje promedio ICFES por estrato — Cali",
        height=350,
        margin=dict(t=50, b=20, l=10, r=10),
        paper_bgcolor="#FAFAFA",
        plot_bgcolor="#FAFAFA",
        yaxis=dict(range=[200, df_est_per["PROMEDIO_GLOBAL"].max() + 30]),
    )
    st.plotly_chart(fig_est, use_container_width=True)

with col_b2:
    # Brecha digital (internet + computador)
    st.markdown("**🌐 Acceso tecnologico por estrato**")
    fig_tec = go.Figure()
    fig_tec.add_trace(go.Bar(
        name="% con Internet",
        x=df_est_per["FAMI_ESTRATOVIVIENDA"],
        y=df_est_per["PCT_TIENE_INTERNET"],
        marker_color="#003087",
    ))
    fig_tec.add_trace(go.Bar(
        name="% con Computador",
        x=df_est_per["FAMI_ESTRATOVIVIENDA"],
        y=df_est_per["PCT_TIENE_COMPUTADOR"],
        marker_color="#0044B8",
    ))
    fig_tec.update_layout(
        barmode="group",
        height=300,
        margin=dict(t=20, b=20, l=10, r=10),
        paper_bgcolor="#FAFAFA",
        plot_bgcolor="#FAFAFA",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        yaxis=dict(range=[0, 105], ticksuffix="%"),
    )
    st.plotly_chart(fig_tec, use_container_width=True)

    # Dato de impacto
    est1 = df_est_per[df_est_per["FAMI_ESTRATOVIVIENDA"]=="Estrato 1"]["PROMEDIO_GLOBAL"]
    est6 = df_est_per[df_est_per["FAMI_ESTRATOVIVIENDA"]=="Estrato 6"]["PROMEDIO_GLOBAL"]
    if not est1.empty and not est6.empty:
        brecha = est6.values[0] - est1.values[0]
        st.info(
            f"💡 **Brecha Estrato 1 vs Estrato 6: "
            f"{brecha:.0f} puntos** en {PERIODO_LABELS[periodo_sel]}. "
            f"Esta diferencia equivale a meses de preparacion adicional.",
            icon="📌"
        )

st.markdown("---")

# ================================================================
# SECCION 3 — SEMAFORO POR AREA / MATERIA
# ================================================================
st.markdown("### 📚 ¿En qué área está más débil Cali?")
st.caption(
    "Compara el promedio de cada materia en Cali. "
    "Las pruebas se califican de 0 a 100 puntos cada una."
)

df_are_per = df_are[df_are["PERIODO"] == periodo_sel].copy()
if tipo_sel != "Todos":
    df_are_per = df_are_per[df_are_per["COLE_NATURALEZA"] == tipo_sel]
else:
    df_are_per = df_are_per.groupby("AREA").agg(
        PROMEDIO=("PROMEDIO", "mean"),
        PROMEDIO_CALI=("PROMEDIO_CALI", "mean"),
    ).reset_index()

COLORES_AREA = {
    "Matematicas":    "#DC2626",
    "Lectura Critica":"#059669",
    "Ingles":         "#0044B8",
    "C. Naturales":   "#D97706",
    "Sociales":       "#7C3AED",
}

fig_are = go.Figure()
areas_ordenadas = df_are_per.sort_values("PROMEDIO", ascending=True)
for _, row in areas_ordenadas.iterrows():
    fig_are.add_trace(go.Bar(
        x=[row["PROMEDIO"]],
        y=[row["AREA"]],
        orientation="h",
        marker_color=COLORES_AREA.get(row["AREA"], "#94A3B8"),
        text=[f"{row['PROMEDIO']:.1f}"],
        textposition="outside",
        name=row["AREA"],
        hovertemplate=(
            f"<b>{row['AREA']}</b><br>"
            f"Promedio: {row['PROMEDIO']:.1f}/100<br>"
            f"Promedio Cali: {row['PROMEDIO_CALI']:.1f}/100<br>"
            "<extra></extra>"
        ),
    ))

fig_are.update_layout(
    title="Promedio por area evaluada — Cali",
    showlegend=False,
    height=300,
    margin=dict(t=50, b=20, l=10, r=60),
    paper_bgcolor="#FAFAFA",
    plot_bgcolor="#FAFAFA",
    xaxis=dict(range=[40, 75]),
)
st.plotly_chart(fig_are, use_container_width=True)

# Insight automatico
if not df_are_per.empty:
    area_debil  = df_are_per.loc[df_are_per["PROMEDIO"].idxmin(), "AREA"]
    area_fuerte = df_are_per.loc[df_are_per["PROMEDIO"].idxmax(), "AREA"]
    st.markdown(
        f"📌 **En {PERIODO_LABELS[periodo_sel]}**, el area con menor promedio "
        f"en Cali es **{area_debil}** y la mas fuerte es **{area_fuerte}**. "
        f"Esto puede orientar tu plan de estudio."
    )

st.markdown("---")

# ================================================================
# SECCION 4 — TENDENCIA HISTORICA
# ================================================================
st.markdown("### 📈 ¿Cómo ha evolucionado el puntaje en Cali?")

df_hist = df_col.copy()
if tipo_sel != "Todos":
    df_hist = df_hist[df_hist["COLE_NATURALEZA"] == tipo_sel]
df_evol = df_hist.groupby("PERIODO")["PROMEDIO_GLOBAL"].mean().reset_index()
df_evol["LABEL"] = df_evol["PERIODO"].map(PERIODO_LABELS)

fig_lin = px.line(
    df_evol, x="LABEL", y="PROMEDIO_GLOBAL",
    markers=True,
    labels={"LABEL": "Periodo", "PROMEDIO_GLOBAL": "Puntaje promedio"},
    color_discrete_sequence=["#003087"],
)
fig_lin.add_hline(
    y=PROMEDIO_NACION,
    line_dash="dot",
    line_color="#059669",
    annotation_text=f"Promedio nacional: {PROMEDIO_NACION}",
    annotation_position="bottom right",
    annotation_font_color="#059669",
)
fig_lin.update_traces(
    mode="lines+markers+text",
    text=df_evol["PROMEDIO_GLOBAL"].round(0).astype(int),
    textposition="top center",
)
fig_lin.update_layout(
    height=280,
    margin=dict(t=20, b=20, l=10, r=10),
    paper_bgcolor="#FAFAFA",
    plot_bgcolor="#FAFAFA",
    yaxis=dict(range=[240, df_evol["PROMEDIO_GLOBAL"].max() + 20]),
)
st.plotly_chart(fig_lin, use_container_width=True)

# ================================================================
# FOOTER
# ================================================================
st.markdown("---")
st.caption(
    f"Datos: Cali ({tipo_sel}) | Periodo: {PERIODO_LABELS[periodo_sel]} | "
    f"Fuente: ICFES Colombia — datos estadisticos reales 2019-2023 | "
    f"Promedio Cali referencia: {PROMEDIO_CALI} pts"
)

if st.button("🏠 Volver al inicio"):
    st.switch_page("app.py")
