from .ollama_client import generar_respuesta
from .models import Tarea
from .context_manager import guardar_interaccion
import json

def ejecutar_tareas_asistente(roadmap_id):
    tareas = Tarea.objects.filter(roadmap_id=roadmap_id, actor="asistente")
    resultados = []

    for tarea in tareas:
        prompt = f"Realizá la siguiente tarea: {tarea.tarea}"
        respuesta = generar_respuesta(prompt, tipo="codigo", agente="asistente")

        respuesta_json = {
            "tipo": "respuesta",
            "contenido": respuesta
        }

        doc_id = guardar_interaccion(
            texto=json.dumps(respuesta_json, ensure_ascii=False),
            agente="asistente",
            objetivo_id=str(tarea.roadmap.objetivo.id),
            fase="ejecucion"
        )

        resultados.append({
            "tarea_id": tarea.id,
            "respuesta": respuesta_json,
            "documento_id": doc_id
        })

    return resultados
