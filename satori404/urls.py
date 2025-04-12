from django.contrib import admin
from django.urls import path
from core.views import manifesto_view, neo_view, neo_talking_view, neo_real_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', manifesto_view, name='manifesto'),
    path('neo/', neo_view, name='neo'),
    path('neo_talking/', neo_talking_view, name='neo_talking'),
    path('neo_real/', neo_real_view, name='neo_real'),  # 👈 esta es la nueva


]
