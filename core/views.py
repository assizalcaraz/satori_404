import json
import random
from django.shortcuts import render
from django.conf import settings
import os

def manifesto_view(request):
    try:
        data_path = os.path.join(settings.BASE_DIR, 'core', 'data_koan.json')
        with open(data_path, encoding='utf-8') as f:
            koans = json.load(f)
        koan = random.choice(koans)
    except Exception as e:
        koan = f"⚠️ Error cargando el manifiesto: {e}"
    return render(request, 'core/manifesto.html', {'koan': koan})

def index_view(request):
    return render(request, 'core/index.html')

def ascii_view(request):
    return render(request, 'core/ascii.html')
