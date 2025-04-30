# agentes/views_arquitecto.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from django.utils import timezone
import json
import traceback

from .models import Objetivo, Roadmap, Tarea
from core.agentes.arquitecto import generar_plan_estructurado
from .chroma_manager import guardar_checkin, guardar_tarea, eliminar_objetivo_vectores
from .ollama_client import verificar_config
from core.agentes.arquitecto_checkin import checkin_arquitecto



@csrf_exempt
def crear_objetivo(request):
    verificar_config()

    if request.method != "POST":
        return JsonResponse({"error": "Sólo se permiten solicitudes POST."}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
        titulo = data.get("objetivo", "").strip()
        descripcion = data.get("contexto", "").strip()
        prioridad = int(data.get("prioridad", 3))

        if not titulo:
            return JsonResponse({"error": "Se requiere un 'objetivo'."}, status=400)

        print(f"📩 Recibido: objetivo='{titulo}', descripcion='{descripcion}'")

        # Paso 1: Realizar Check-In
        resultado_checkin = checkin_arquitecto(titulo)
        print(f"🔍 Resultado Check-In: {json.dumps(resultado_checkin, indent=2, ensure_ascii=False)}")
        print(f"🛡️ Confirmación recibida: '{resultado_checkin.get('confirmacion_final', '')}'")

        if resultado_checkin.get("confirmacion_final", "").strip().lower() not in ("sí", "si", "yes"):
            print("❌ El Check-In determinó que el objetivo no es válido o está incompleto.")
            return JsonResponse({"error": "El Check-In determinó que el objetivo no es válido o está incompleto."}, status=400)

        # Paso 2: Crear Objetivo
        objetivo = Objetivo.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            prioridad=prioridad,
            fecha_creacion=timezone.now(),
            checkin_data=resultado_checkin
        )

        # Paso 3: Guardar Check-In en Chroma
        guardar_checkin(objetivo_id=str(objetivo.id), contenido_checkin=resultado_checkin)

        # Paso 4: Generar Roadmap
        plan = generar_plan_estructurado(titulo, descripcion)
        tareas_llm = plan.get("tareas", [])

        roadmap = Roadmap.objects.create(
            objetivo=objetivo,
            generado_por="arquitecto"
        )

        tareas_guardadas = []
        for tarea_data in tareas_llm:
            if not isinstance(tarea_data, dict):
                continue

            depende_de = tarea_data.get("depende_de", [])
            if not isinstance(depende_de, list):
                depende_de = []

            tarea_obj = Tarea.objects.create(
                roadmap=roadmap,
                tarea=tarea_data.get("tarea", ""),
                tipo=tarea_data.get("tipo", "sin_tipo"),
                prioridad=tarea_data.get("prioridad", 3),
                depende_de=depende_de,
                actor=tarea_data.get("actor", "asistente")
            )

            guardar_tarea(
                objetivo_id=str(objetivo.id),
                tarea_data=tarea_data,
                tarea_id=str(tarea_obj.id)
            )

            tareas_guardadas.append(tarea_obj.id)

        return JsonResponse({
            "mensaje": "Objetivo creado exitosamente con Check-In y Roadmap.",
            "objetivo_id": objetivo.id,
            "roadmap_id": roadmap.id,
            "tareas_guardadas": tareas_guardadas,
            "checkin": resultado_checkin,
            "plan": plan
        })

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({
            "error": "Error interno al crear el objetivo.",
            "detalle": str(e)
        }, status=500)

@require_http_methods(["GET"])
def obtener_objetivo(request, objetivo_id):
    try:
        objetivo = Objetivo.objects.get(id=objetivo_id)
        primer_roadmap = objetivo.roadmaps.first()

        data = {
            "id": objetivo.id,
            "titulo": objetivo.titulo,
            "descripcion": objetivo.descripcion,
            "prioridad": objetivo.prioridad,
            "fecha_creacion": objetivo.fecha_creacion.isoformat() if objetivo.fecha_creacion else None,
            "checkin": objetivo.checkin_data,
            "roadmap_id": primer_roadmap.id if primer_roadmap else None
        }
        return JsonResponse(data)

    except Objetivo.DoesNotExist:
        return JsonResponse({"error": "Objetivo no encontrado."}, status=404)

@csrf_exempt
def eliminar_objetivo(request, objetivo_id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Sólo se permiten solicitudes DELETE."}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8")) if request.body else {}
        confirmar = data.get("confirmar", False)

        objetivo = Objetivo.objects.get(id=objetivo_id)
        cantidad_roadmaps = objetivo.roadmaps.count()
        cantidad_tareas = Tarea.objects.filter(roadmap__objetivo=objetivo).count()

        if (cantidad_roadmaps > 0 or cantidad_tareas > 0) and not confirmar:
            return JsonResponse({
                "advertencia": f"El objetivo tiene {cantidad_roadmaps} roadmaps y {cantidad_tareas} tareas asociadas activas.",
                "mensaje": "¿Seguro que quieres eliminarlo? Esta acción NO se puede deshacer.",
                "requerido": "Envía el mismo DELETE agregando {\"confirmar\": true} en el body para confirmar."
            }, status=400)

        # 🔥 Borrar del vectorial (Chroma)
        eliminar_objetivo_vectores(str(objetivo.id))

        # 🔥 Borrar tareas asociadas
        Tarea.objects.filter(roadmap__objetivo=objetivo).delete()

        # 🔥 Borrar roadmaps asociados
        objetivo.roadmaps.all().delete()

        # 🔥 Finalmente borrar objetivo
        objetivo.delete()

        return JsonResponse({"mensaje": f"Objetivo {objetivo_id} y todos sus datos fueron eliminados correctamente."})

    except Objetivo.DoesNotExist:
        return JsonResponse({"error": "Objetivo no encontrado."}, status=404)

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({
            "error": "Error interno al eliminar el objetivo.",
            "detalle": str(e)
        }, status=500)

@csrf_exempt
def obtener_checkin(request, objetivo_id):
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido."}, status=405)

    try:
        objetivo = Objetivo.objects.get(id=objetivo_id)
        if objetivo.checkin_data:
            return JsonResponse({
                "objetivo_id": objetivo.id,
                "checkin_contenido": objetivo.checkin_data
            })
        else:
            return JsonResponse({"error": "No hay Check-In disponible."}, status=404)

    except Objetivo.DoesNotExist:
        return JsonResponse({"error": "Objetivo no encontrado."}, status=404)

@csrf_exempt
def obtener_tareas_roadmap(request, roadmap_id):
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido."}, status=405)

    try:
        roadmap = Roadmap.objects.get(id=roadmap_id)
        tareas = roadmap.tareas.all().values('id', 'tarea', 'tipo', 'prioridad', 'depende_de', 'actor')

        return JsonResponse(list(tareas), safe=False)

    except Roadmap.DoesNotExist:
        return JsonResponse({"error": "Roadmap no encontrado."}, status=404)
