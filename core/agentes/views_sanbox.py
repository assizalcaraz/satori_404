import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .ollama_client import generar_respuesta_desde_template

@csrf_exempt
@require_http_methods(["POST"])
def procesar_consulta_llm(request):
    """
    Endpoint sandbox para pruebas rápidas con LLM sin usar arquitectura de agentes.
    """
    try:
        data = json.loads(request.body.decode("utf-8"))
        tipo = data.get("tipo", "codigo")
        prompt = data.get("prompt", "Escribí una función en Python que devuelva Fibonacci")
        temperatura = float(data.get("temperatura", 0.2))
        modelo = data.get("modelo", "codellama:7b-instruct")

        kwargs = {
            "prompt_usuario": prompt,
            "temperatura": temperatura,
            "modelo": modelo
        }

        if tipo == "arquitecto":
            objetivo = data.get("prompt")
            contexto = data.get("contexto", "")
            kwargs = {"objetivo": objetivo, "contexto": contexto, "temperatura": temperatura, "modelo": modelo}

        elif tipo == "evaluacion":
            texto = data.get("prompt")
            criterio = data.get("criterio", "calidad técnica")
            kwargs = {"texto": texto, "criterio": criterio, "temperatura": temperatura, "modelo": modelo}

        respuesta = generar_respuesta_desde_template(tipo, **kwargs)
        return JsonResponse({"respuesta": respuesta})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
