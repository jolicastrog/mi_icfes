"""
MI ICFES — ai/pandas_agent.py
Sprint 4 - HU-07: Pandas DataFrame Agent para chat conversacional
sobre datos ICFES de Cali.
"""
import streamlit as st
import pandas as pd
import os
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
 
 
# Prefijo del sistema para el agente — define su personalidad y restricciones
SYSTEM_PREFIX = """Eres el Consejero de Datos MI ICFES, un experto en analizar
los resultados del examen Saber 11 en la ciudad de Cali, Colombia.
 
Tienes acceso a tres tablas de datos reales de Cali:
- df_colegios: promedios por colegio, jornada, naturaleza (Oficial/No Oficial)
- df_estrato: promedios por estrato socioeconomico (1-6) con acceso tecnologico
- df_areas: promedios por area evaluada (Matematicas, Lectura, Ingles, etc.)
 
Reglas importantes:
1. Responde SIEMPRE en espanol colombiano claro y sencillo.
2. Si la pregunta no puede responderse con los datos disponibles, dilo claramente.
3. Cuando des numeros de puntaje, incluye la unidad "pts".
4. Si el usuario pregunta por un colegio especifico, busca el nombre mas parecido.
5. Maximo 150 palabras por respuesta — se conciso y directo.
6. No ejecutes operaciones destructivas sobre los datos.
"""
 
 
@st.cache_resource
def crear_agente():
    """
    Crea el Pandas DataFrame Agent con los 3 CSVs de datos ICFES Cali.
    Se cachea con @st.cache_resource para no recrearlo en cada mensaje.
 
    Returns:
        agent: AgentExecutor listo para responder preguntas
        None: si hay error de configuracion
    """
    # Verificar API key
    try:
        api_key = st.secrets["openai"]["api_key"]
    except Exception:
        st.error("No se encontro la API key de OpenAI en secrets.toml")
        return None
 
    # Verificar que los CSVs existen
    rutas = {
        "colegios": "data/datos_resumen_colegios_cali.csv",
        "estrato":  "data/datos_resumen_estrato_cali.csv",
        "areas":    "data/datos_areas_cali.csv",
    }
    for nombre, ruta in rutas.items():
        if not os.path.exists(ruta):
            st.error(f"CSV no encontrado: {ruta}. Verificar carpeta data/")
            return None
 
    # Cargar los DataFrames
    df_colegios = pd.read_csv(rutas["colegios"])
    df_estrato  = pd.read_csv(rutas["estrato"])
    df_areas    = pd.read_csv(rutas["areas"])
 
    # Configurar el LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.0,  # 0 para respuestas mas consistentes y precisas
        api_key=api_key,
        max_tokens=400,
    )
 
    # Crear el agente con los 3 DataFrames
    # Se pasan como lista — el agente puede consultar cualquiera de los tres
    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=[df_colegios, df_estrato, df_areas],
        agent_type=AgentType.OPENAI_FUNCTIONS,
        verbose=False,          # True en desarrollo para ver el razonamiento
        allow_dangerous_code=True,  # Requerido en langchain-experimental 0.0.65+
        prefix=SYSTEM_PREFIX,
        handle_parsing_errors=True, # Evita pantalla blanca si el agente falla
        max_iterations=5,       # Limita el numero de pasos del agente
    )
    return agent
 
 
def preguntar_al_agente(agente, pregunta: str) -> str:
    """
    Envia una pregunta al agente y retorna la respuesta como string.
    Maneja errores para que el chat nunca muestre pantalla blanca.
 
    Args:
        agente: AgentExecutor creado con crear_agente()
        pregunta: texto libre del usuario
 
    Returns:
        str: respuesta del agente o mensaje de error amigable
    """
    if agente is None:
        return ("Lo siento, el Consejero de Datos no esta disponible. "
                "Verificar la configuracion de la API key.")
    try:
        resultado = agente.invoke({"input": pregunta})
        # El agente retorna un dict con clave "output"
        respuesta = resultado.get("output", str(resultado))
        return respuesta
    except Exception as e:
        error_msg = str(e)[:100]  # Limitar longitud del error
        # Mensajes de error amigables segun el tipo
        if "RateLimitError" in error_msg or "quota" in error_msg.lower():
            return "Se agoto el credito de OpenAI. Agregar credito en platform.openai.com"
        elif "AuthenticationError" in error_msg:
            return "Error de autenticacion. Verificar la API key en secrets.toml"
        elif "timeout" in error_msg.lower():
            return "La consulta tardo demasiado. Intenta con una pregunta mas simple."
        else:
            return f"No pude responder esa pregunta con los datos disponibles. Intenta reformularla."
