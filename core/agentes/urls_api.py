# backend/agentes/urls_api.py

from django.urls import path
from .views import (
    simular_interaccion,
    consultar_memoria,
    historial_compilado,
    interactuar,
    medir_tiempo_llm,
    generar_respuesta_llm,
    arquitecto_view,
)
from .views_arquitecto import (
    crear_objetivo,
    obtener_objetivo,
    eliminar_objetivo,
    obtener_checkin,
    obtener_tareas_roadmap,
)
from .views_asistente import (
    ejecutar_tareas,
)
from tools.views_tools import (
    limpiar_base,
)

urlpatterns = [
    path("simular/", simular_interaccion, name="simular_interaccion"),
    path("memoria/", consultar_memoria, name="consultar_memoria"),
    path("historial/", historial_compilado, name="historial_compilado"),
    path("interactuar/", interactuar, name="interactuar_llm"),
    path("tiempo/", medir_tiempo_llm, name="medir_tiempo_llm"),
    path("generar/", generar_respuesta_llm, name="generar_respuesta"),
    path("arquitecto/", arquitecto_view, name="arquitecto_view"),

    # 🔥 Nuevo flujo para arquitecto
    path("arquitecto/crear_objetivo/", crear_objetivo, name="crear_objetivo"),
    path("arquitecto/obtener_objetivo/<int:objetivo_id>/", obtener_objetivo, name="obtener_objetivo"),
    path("objetivos/<int:objetivo_id>/", obtener_objetivo, name="alias_objetivo"),
    path("arquitecto/eliminar_objetivo/<int:objetivo_id>/", eliminar_objetivo, name="eliminar_objetivo"),
    path("arquitecto/obtener_checkin/<int:objetivo_id>/", obtener_checkin, name="obtener_checkin"),
    path("roadmaps/<int:roadmap_id>/tareas/", obtener_tareas_roadmap, name="obtener_tareas_roadmap"),







    # Asistente
    path("asistente/ejecutar/", ejecutar_tareas, name="ejecutar_tareas_asistente"),

    # Tools
    path("tools/limpiar_base/", limpiar_base, name="limpiar_base"),
]
