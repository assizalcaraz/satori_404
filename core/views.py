
from django.http import JsonResponse
import json
import random
from django.shortcuts import render
from django.conf import settings
import os
from core.agentes.arquitecto_checkin import checkin_arquitecto
from core.agentes.mock_llm import modelo_a, modelo_b  # o el cliente real tipo OllamaClient



def manifesto_view(request):
    try:
        data_path = os.path.join(settings.BASE_DIR, 'core', 'data_koan.json')
        with open(data_path, encoding='utf-8') as f:
            koans = json.load(f)
        koan = random.choice(koans)
    except Exception as e:
        koan = f"⚠️ Error cargando el manifiesto: {e}"
    return render(request, 'core/manifesto.html', {'koan': koan})

def index_view(request):
    return render(request, 'core/index.html')

def ascii_view(request):
    return render(request, 'core/ascii.html')

from django.http import JsonResponse

from django.http import JsonResponse
from django.shortcuts import render
import uuid
from core.agentes.ollama_client import generar_respuesta
from core.agentes.chroma_manager import buscar_checkin, guardar_checkin

# Prompt base para cada modelo
def construir_prompt(totem, contexto):
    if totem == "A":
        return f"""
Contexto previo:
{contexto}

Respondé con tu estilo propio a esta pregunta:
¿Quién sos y por qué existís?
"""
    elif totem == "B":
        return f"""
Contexto previo:
{contexto}

Reaccioná al mensaje anterior con una opinión crítica. Repetí primero el mensaje citado y luego respondé:
"""
    return "Sin prompt definido"


# Vista principal de interacción real
conversacion_memoria = []  # estado persistente en RAM

def interaccion(request):
    try:
        id_interaccion = str(uuid.uuid4())[:8]
        contexto = ""
        for idx, turno in enumerate(conversacion_memoria):
            contexto += f"Turno {idx} - {turno['from']}: {turno['input']} => {turno['output']}\n"

        # Turno de tótem A
        prompt_a = construir_prompt("A", contexto)
        respuesta_a = generar_respuesta(prompt_a)
        conversacion_memoria.append({
            "from": "tótem A",
            "input": "¿Quién sos y por qué existís?",
            "output": respuesta_a.strip()
        })

        # Turno de tótem B
        contexto += f"Tótem A: ¿Quién sos y por qué existís? => {respuesta_a}\n"
        prompt_b = construir_prompt("B", contexto)
        respuesta_b = generar_respuesta(prompt_b)
        conversacion_memoria.append({
            "from": "tótem B",
            "input": f"Tótem A dijo: {respuesta_a.strip()}. ¿Qué opinás?",
            "output": respuesta_b.strip()
        })

        # Guardar en Chroma (opcional)
        guardar_checkin(id_interaccion, {"conversacion": conversacion_memoria})

        return JsonResponse({"status": "ok", "interaccion": {"ronda": conversacion_memoria}})

    except Exception as e:
        return JsonResponse({"status": "error", "mensaje": str(e)}, status=500)


def interaccion_ui(request):
    return render(request, "core/interaccion.html")
