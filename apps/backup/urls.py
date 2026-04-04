from django.urls import path
from django.shortcuts import render

# Namespace del módulo backup
app_name = 'backup'

# Vista temporal placeholder — se reemplaza en el desarrollo completo del módulo
def placeholder(request):
    return render(request, 'base.html')

urlpatterns = [
    path('', placeholder, name='lista_backups'),
]