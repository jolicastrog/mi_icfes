"""
MI ICFES — ai/langchain_advisor.py
Sprint 2 - Consejero IA con LangChain 0.2.16 + GPT-4o-mini
"""
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def generar_consejo(score: float, perfil: dict, top_features: list) -> str:
    """
    Genera 3 recomendaciones personalizadas usando LangChain + GPT-4o-mini.
    Usa la nueva sintaxis LCEL (LangChain Expression Language) de 0.2.x
    que reemplaza el LLMChain deprecado.
    """
    try:
        api_key = st.secrets["openai"]["api_key"]
    except Exception:
        return "No se pudo acceder a la API key. Verificar .streamlit/secrets.toml"

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.4,
        api_key=api_key,
        max_tokens=600,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """Eres un experto en educacion colombiana con 15 anos de
experiencia en el sistema Saber 11. Respondes siempre en espanol colombiano
coloquial, de forma empatica, sin tecnicismos, como si hablaras con un
adolescente de 17 anos. Siempre das recursos GRATUITOS disponibles en Colombia."""),

        ("human", """El modelo predijo {score}/500 para un estudiante con este perfil:
- Estrato: {estrato} | Internet: {internet} | Computador: {computador}
- Colegio: {naturaleza} | Zona: {zona}
- Educacion padre: {edu_padre} | Educacion madre: {edu_madre}
- Horas estudio extra: {horas}/semana | Trabaja: {trabaja} horas
- Libros en casa: {libros}
- Variable que MAS impacta su puntaje: {top1}

Genera EXACTAMENTE 3 recomendaciones numeradas (1. 2. 3.).
Maximo 70 palabras por recomendacion.
Cada una DEBE incluir un recurso gratuito concreto disponible en Colombia
(Khan Academy, ICFES Interactivo, YouTube Unicoos, Mintic Aprender Digital, etc).
Habla directamente al estudiante usando 'tu'."""),
    ])

    # Nueva sintaxis LCEL: prompt | llm | parser (reemplaza LLMChain)
    chain = prompt | llm | StrOutputParser()

    nombres_top = [f.get("legible", f.get("tecnico", "habitos de estudio"))
                   for f in (top_features[:3] if top_features else [])]
    while len(nombres_top) < 3:
        nombres_top.append("habitos de estudio")

    return chain.invoke({
        "score":      round(score),
        "estrato":    perfil.get("estrato", "No especificado"),
        "internet":   perfil.get("internet", "No especificado"),
        "computador": perfil.get("computador", "No especificado"),
        "naturaleza": perfil.get("naturaleza", "No especificado"),
        "zona":       perfil.get("zona", "No especificado"),
        "horas":      perfil.get("horas", 0),
        "trabaja":    perfil.get("trabaja", 0),
        "edu_padre":  perfil.get("edu_padre", "No especificado"),
        "edu_madre":  perfil.get("edu_madre", "No especificado"),
        "libros":     perfil.get("libros", "No especificado"),
        "top1":       nombres_top[0],
    })