from django.contrib import admin
from django.urls import path
from core.views import index_view, manifesto_view, ascii_view

urlpatterns = [
    path('', index_view, name='index'),
    path('admin/', admin.site.urls),
    path('manifesto/', manifesto_view, name='manifesto'),
    path('ascii/', ascii_view, name='ascii'),
]
