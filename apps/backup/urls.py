from django.urls import path
from apps.backup import views

# Namespace del módulo backup
app_name = 'backup'

urlpatterns = [

    # Listado de backups — solo ADMIN
    path('', views.lista_backups, name='lista_backups'),

    # Generar backup manual — solo ADMIN
    path('generar/', views.generar_backup, name='generar_backup'),
    
    # Restaurar backup — solo ADMIN
    path('<int:id>/restaurar/', views.restaurar_backup, name='restaurar_backup'),
]