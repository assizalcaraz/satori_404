# backend/agentes/views_asistente.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .asistente import ejecutar_tareas_asistente

@csrf_exempt
def ejecutar_tareas(request):
    """
    Ejecuta todas las tareas del asistente asociadas a un Roadmap.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
        roadmap_id = data.get("roadmap_id")

        if not roadmap_id:
            return JsonResponse({"error": "Se requiere roadmap_id"}, status=400)

        resultados = ejecutar_tareas_asistente(roadmap_id)
        return JsonResponse({"resultados": resultados})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
