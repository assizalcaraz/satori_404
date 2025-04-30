import time
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods

from .ollama_client import generar_respuesta, generar_respuesta_desde_template
from .prompts import prompt_codigo
from .context_manager import guardar_interaccion, consultar_contexto

from .models import Objetivo
from django.core.serializers.json import DjangoJSONEncoder

@csrf_exempt
def historial_compilado(request):
    if request.method != "POST":
        return JsonResponse({"error": "Sólo se permiten solicitudes POST."}, status=405)

    try:
        objetivos = Objetivo.objects.all().order_by("-fecha_creacion")
        lista = []

        for obj in objetivos:
            roadmap = obj.roadmaps.order_by("-fecha_generacion").first()
            tareas = []
            if roadmap:
                tareas = list(roadmap.tareas.values(
                    "id", "tarea", "tipo", "prioridad", "depende_de", "actor"
                ))

            lista.append({
                "id": obj.id,
                "titulo": obj.titulo,
                "descripcion": obj.descripcion,
                "prioridad": obj.prioridad,
                "fecha_creacion": obj.fecha_creacion.isoformat(),
                "roadmap_id": roadmap.id if roadmap else None,
                "tareas": tareas
            })

        return JsonResponse({"objetivos": lista}, encoder=DjangoJSONEncoder, safe=False)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def simular_interaccion(request):
    try:
        print("📥 Ingresó al endpoint /agentes/simular")

        body = json.loads(request.body)
        print("🧾 Cuerpo recibido:", body)

        agente = body.get("agente", "arquitecto")
        tipo = body.get("tipo", "codigo")
        prompt = body.get("prompt", "simulación de tarea")
        objetivo_id = body.get("objetivo_id", "demo_001")
        fase = body.get("fase", "inicio")

        from .mock_llm import respuesta_simulada
        from .context_manager import guardar_interaccion

        respuesta = respuesta_simulada(tipo=tipo, prompt=prompt, agente=agente)
        print("✅ Respuesta generada:", respuesta)

        doc_id = guardar_interaccion(respuesta, agente, objetivo_id, fase)
        print("🧠 Documento almacenado en Chroma con ID:", doc_id)

        return JsonResponse({"respuesta": respuesta, "documento_id": doc_id})

    except Exception as e:
        print("❌ Ocurrió un error en /simular/")
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def consultar_memoria(request):
    try:
        body = json.loads(request.body)
        prompt = body.get("prompt", "consulta básica")
        objetivo_id = body.get("objetivo_id", None)

        documentos = consultar_contexto(prompt, objetivo_id)
        return JsonResponse({"resultados": documentos})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def procesar_consulta_llm(request):
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

@csrf_exempt
@require_POST
def interactuar(request):
    try:
        body = json.loads(request.body)

        tipo = body.get("tipo", "codigo")  # valores posibles: "codigo", "arquitecto", "evaluacion"
        prompt = body.get("prompt", "")
        modelo = body.get("modelo", "codellama:7b-instruct")
        temperatura = float(body.get("temperatura", 0.2))

        if tipo == "codigo":
            payload = {
                "prompt_usuario": prompt,
                "modelo": modelo,
                "temperatura": temperatura
            }
        elif tipo == "arquitecto":
            payload = {
                "objetivo": prompt,
                "modelo": modelo,
                "temperatura": temperatura,
                "contexto": body.get("contexto", "")
            }
        elif tipo == "evaluacion":
            payload = {
                "texto": prompt,
                "criterio": body.get("criterio", "claridad"),
                "modelo": modelo,
                "temperatura": temperatura
            }
        else:
            return JsonResponse({"error": f"Tipo de prompt no válido: {tipo}"}, status=400)

        respuesta = generar_respuesta_desde_template(tipo, **payload)
        return JsonResponse({"respuesta": respuesta})

    except Exception as e:
        return JsonResponse({"error": f"Error interno: {str(e)}"}, status=500)


@csrf_exempt
def medir_tiempo_llm(request):
    prompt_usuario = request.GET.get("prompt", "¿Cuál es la capital de Argentina?")
    temperatura = float(request.GET.get("temperatura", 0.2))
    modelo = request.GET.get("modelo", "codellama:7b-instruct")

    prompt_dict = prompt_codigo(prompt_usuario, temperatura, modelo)

    start = time.time()
    respuesta = generar_respuesta(prompt_dict)
    end = time.time()

    return JsonResponse({
        "respuesta": respuesta,
        "duracion_segundos": round(end - start, 2)
    })

def generar_respuesta_llm(request):
    prompt_usuario = request.GET.get("prompt", "Escribí una función en Python que devuelva Fibonacci")
    temperatura = float(request.GET.get("temperatura", 0.2))
    modelo = request.GET.get("modelo", "codellama:7b-instruct")

    prompt_dict = prompt_codigo(prompt_usuario, temperatura, modelo)
    respuesta = generar_respuesta(prompt_dict)

    return JsonResponse({"respuesta": respuesta})

def arquitecto_view(request):
    objetivo = request.GET.get("objetivo", "Crear una app de asistencia con reconocimiento facial")
    contexto = request.GET.get("contexto", "")
    resultado = desglosar_objetivo(objetivo, contexto)
    return JsonResponse(resultado, safe=False)
