from django.contrib import admin
from .models import Objetivo, Roadmap, Tarea

@admin.register(Objetivo)
class ObjetivoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'prioridad', 'fecha_creacion')
    search_fields = ('titulo',)

@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ('id', 'objetivo', 'generado_por', 'fecha_generacion')
    search_fields = ('objetivo__titulo',)

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('id', 'tarea', 'tipo', 'prioridad', 'actor')
    search_fields = ('tarea',)
