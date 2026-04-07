from django.urls import path
from apps.insumos import views

# Namespace del módulo insumos
app_name = 'insumos'

urlpatterns = [

    # Listado y detalle
    path('', views.lista_insumos, name='lista_insumos'),
    path('<int:id>/', views.detalle_insumo, name='detalle_insumo'),

    # Crear y editar
    path('crear/', views.crear_insumo, name='crear_insumo'),
    path('<int:id>/editar/', views.editar_insumo, name='editar_insumo'),

    # Cambiar estado — solo ADMIN
    path('<int:id>/estado/', views.cambiar_estado_insumo, name='cambiar_estado_insumo'),

    # Modificar stock manualmente — solo ADMIN
    path('<int:id>/stock/', views.modificar_stock_insumo, name='modificar_stock_insumo'),

]