# backend/agentes/tests/test_arquitecto.py

import json
from django.test import TestCase, Client
from django.urls import reverse
import os

class PlanificacionArquitectoMockTest(TestCase):
    def setUp(self):
        # Forzamos el uso de mocks
        os.environ["USAR_MOCKS"] = "True"
        self.client = Client()
        self.url = reverse("planificar_objetivo")
        self.payload = {
            "objetivo": "Construir una app de recordatorios con IA",
            "contexto": "Usuario sin conocimientos técnicos, necesita ayuda para organizar su semana",
            "objetivo_id": "test_mock_arquitecto"
        }

    def test_planificacion_mock_activada(self):
        response = self.client.post(
            self.url,
            data=json.dumps(self.payload),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("plan", data)
        self.assertIn("tareas_guardadas", data)
        self.assertTrue(len(data["plan"]["tareas"]) > 0)

        for tarea in data["plan"]["tareas"]:
            self.assertIn("tarea", tarea)
            self.assertIn("prioridad", tarea)
            self.assertIn("actor", tarea)

        print("✅ Test de planificación con mocks pasado correctamente.")
