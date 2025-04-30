import json
from datetime import datetime

contador = {"valor": 0}

def modelo_a(prompt):
    return f"[A responde a]: {prompt[::-1]}"  # Inversión para test

def modelo_b(prompt):
    return f"[B responde a]: {prompt.upper()}"  # Mayúsculas para test



def respuesta_simulada(tipo="codigo", prompt="...", agente="arquitecto"):
    contador["valor"] += 1

    if tipo == "codigo":
        return f"# Simulación de código Python\n\ndef ejemplo():\n    return 'Hola mundo {contador['valor']}'"

    if tipo == "evaluacion":
        return f"La respuesta fue evaluada correctamente en base al criterio solicitado. Simulación {contador['valor']}."

    if tipo == "arquitecto":
        return json.dumps([
            {
                "tarea": "Analizar requerimientos del sistema",
                "tipo": "investigación",
                "prioridad": 1,
                "depende_de": [],
                "actor": "usuario"
            },
            {
                "tarea": "Diseñar arquitectura básica",
                "tipo": "programación",
                "prioridad": 2,
                "depende_de": ["Analizar requerimientos del sistema"],
                "actor": "asistente"
            },
            {
                "tarea": "Configurar entorno de desarrollo",
                "tipo": "infraestructura",
                "prioridad": 3,
                "depende_de": [],
                "actor": "asistente"
            },
            {
                "tarea": "Presentar cronograma tentativo al usuario",
                "tipo": "comunicación",
                "prioridad": 4,
                "depende_de": ["Diseñar arquitectura básica"],
                "actor": "usuario"
            }
        ], indent=2)

    if tipo == "asistente":
        return f"Asistente generando contenido simulado según el plan entregado. Iteración: {contador['valor']}"

    # fallback genérico
    return f"[{agente.upper()}] Respuesta simulada #{contador['valor']} - Tipo: {tipo} - Prompt: {prompt[:50]}..."
