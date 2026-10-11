from google import genai
from google.genai import errors
import os
from dotenv import load_dotenv
import json

load_dotenv()  
api_key = os.getenv("API_KEY")
client = genai.Client(api_key=api_key) 

def analizar_eficiencia_con_ia(datos_consultas: dict) -> str:
    
    if not datos_consultas:
        return "No hay suficientes datos registrados para generar un análisis."
        
    prompt = f"""
    Eres un experto en análisis de datos y gestión de recursos humanos educativos.
    A continuación, te presento el volumen de consultas atendidas por nuestro equipo agrupadas por fecha:
    {json.dumps(datos_consultas)}    
    Basado en los picos y caídas de esta demanda, redacta 3 sugerencias operativas breves y concretas para el administrador. 
    El objetivo es mejorar la eficiencia del equipo, anticipar días de alta carga y optimizar la asignación de horarios para los equipos de trabajo.
    """
    try: 
        respuesta = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt
        )
        return respuesta.text or "No pudo generarse un análisis con la información proporcionada en este momento."

    except errors.ServerError: 
        return "El motor de Inteligencia Artificial está experimentando alta demanda. Por favor, intenta de nuevo en unos minutos."