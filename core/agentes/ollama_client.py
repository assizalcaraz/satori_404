import os
import requests
from . import prompts
from .mock_llm import respuesta_simulada


OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://ollama:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
USAR_MOCKS = os.getenv("USAR_MOCKS", "False").lower() in ("true", "1", "yes")


def verificar_config():
    print("🔍 Verificando configuración de entorno:")
    print(f"   OLLAMA_API_URL: {OLLAMA_API_URL}")
    print(f"   OLLAMA_MODEL: {OLLAMA_MODEL}")
    print(f"   USAR_MOCKS (interpreted): {USAR_MOCKS}")
    print(f"   USAR_MOCKS (raw): {os.getenv('USAR_MOCKS')}")


def generar_respuesta(prompt, temperatura=0.2, modelo=None, tipo="codigo", agente="arquitecto"):
    modelo = modelo or OLLAMA_MODEL

    if USAR_MOCKS:
        return respuesta_simulada(tipo=tipo, prompt=prompt, agente=agente)

    url = f"{OLLAMA_API_URL}/api/generate"

    payload = prompt if isinstance(prompt, dict) else {
        "model": modelo,
        "prompt": prompt,
        "temperature": temperatura,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload, timeout=90)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "Error: no se recibió respuesta del modelo.")
    except requests.exceptions.HTTPError as http_err:
        return f"Error HTTP: {http_err} - Payload enviado: {payload}"
    except Exception as e:
        return f"Error inesperado: {e} - Payload enviado: {payload}"


def generar_respuesta_desde_template(tipo, **kwargs):
    if tipo == "codigo":
        payload = prompts.prompt_codigo(**kwargs)
    elif tipo == "constructor":
        payload = prompts.prompt_constructor(**kwargs)
    elif tipo == "evaluacion":
        payload = prompts.prompt_evaluacion(**kwargs)
    else:
        raise ValueError("Tipo de prompt no reconocido")

    return enviar_a_ollama(payload)


def enviar_a_ollama(payload, tipo="codigo", agente="arquitecto"):
    if USAR_MOCKS:
        print("⚙️ Modo MOCK activado: respuesta simulada.")
        return respuesta_simulada(tipo=tipo, prompt=payload.get("prompt", ""), agente=agente)

    url = f"{OLLAMA_API_URL}/api/generate"
    try:
        response = requests.post(url, json=payload, timeout=200)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "Error: no se recibió respuesta del modelo.")
    except requests.exceptions.HTTPError as http_err:
        return f"Error HTTP: {http_err} - Payload: {payload}"
    except Exception as e:
        return f"Error inesperado: {e} - Payload: {payload}"
