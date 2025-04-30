# models.py

from django.db import models
from django.utils import timezone

class Objetivo(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    prioridad = models.IntegerField(default=3)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    checkin_data = models.JSONField(null=True, blank=True)  # Guarda el checkin en el objetivo mismo

    def __str__(self):
        return self.titulo

class Roadmap(models.Model):
    objetivo = models.ForeignKey(Objetivo, on_delete=models.CASCADE, related_name='roadmaps')
    fecha_generacion = models.DateTimeField(default=timezone.now)
    generado_por = models.CharField(max_length=50, default="arquitecto")
    validado = models.BooleanField(default=False)

    def __str__(self):
        return f"Roadmap #{self.id} para {self.objetivo.titulo}"

class Tarea(models.Model):
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE, related_name='tareas')
    tarea = models.CharField(max_length=500)
    tipo = models.CharField(max_length=50)
    prioridad = models.IntegerField(default=3)
    depende_de = models.JSONField(default=list, blank=True)
    actor = models.CharField(max_length=50, default="asistente")

    def __str__(self):
        return self.tarea
