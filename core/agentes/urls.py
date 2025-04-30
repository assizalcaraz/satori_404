# backend/agentes/urls.py

from django.urls import path, include

urlpatterns = [
    path("", include("agentes.urls_api")),
]
