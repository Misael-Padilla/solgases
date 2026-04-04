from django.urls import path
from django.shortcuts import render

# Namespace del módulo usuarios
app_name = 'usuarios'

# Vista temporal placeholder — se reemplaza en el desarrollo completo del módulo
def placeholder(request):
    return render(request, 'base.html')

urlpatterns = [
    path('', placeholder, name='lista_usuarios'),
    path('clientes/', placeholder, name='lista_clientes'),
    path('proveedores/', placeholder, name='lista_proveedores'),
]