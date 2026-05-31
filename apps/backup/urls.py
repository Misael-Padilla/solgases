from django.urls import path
from apps.backup import views

app_name = 'backup'

urlpatterns = [
    path('',                          views.lista_backups,        name='lista_backups'),
    path('generar/',                  views.generar_backup,       name='generar_backup'),
    path('<int:id>/restaurar/',       views.restaurar_backup,     name='restaurar_backup'),
    path('configuracion/',            views.configuracion_backup,   name='configuracion_backup'),
    path('configuracion/cancelar/',   views.cancelar_puntual,       name='cancelar_puntual'),
    path('exportar/',                 views.exportar_backups_excel, name='exportar_backups_excel'),
]
