import json
import datetime
from .ollama_client import generar_respuesta, enviar_a_ollama, verificar_config
from .prompts import prompt_arquitecto

def generar_plan_estructurado(objetivo: str, contexto: str = "") -> dict:
    verificar_config()
    payload = prompt_arquitecto(objetivo=objetivo, contexto=contexto)

    respuesta = enviar_a_ollama(payload, tipo="arquitecto", agente="arquitecto")

    print("📦 Respuesta cruda del modelo:\n", respuesta)

    try:
        tareas = json.loads(respuesta)
    except json.JSONDecodeError:
        tareas = [{
            "tarea": "Error de interpretación",
            "tipo": "error",
            "prioridad": 1,
            "depende_de": [],
            "error": "No se pudo interpretar la respuesta del modelo",
            "respuesta_cruda": respuesta
        }]

    return {
        "objetivo": objetivo,
        "contexto": contexto,
        "tareas": tareas,
        "agente": "arquitecto",
        "fase": "planificacion",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }