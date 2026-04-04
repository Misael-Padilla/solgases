from django.urls import path
from django.shortcuts import render

# Namespace del módulo ventas
app_name = 'ventas'

# Vista temporal placeholder — se reemplaza en el desarrollo completo del módulo
def placeholder(request):
    return render(request, 'base.html')

urlpatterns = [
    path('', placeholder, name='lista_ventas'),
]