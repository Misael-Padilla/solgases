from django.urls import path
from apps.ventas import views

# Namespace del módulo ventas
app_name = 'ventas'

urlpatterns = [

    # Listado y detalle
    path('', views.lista_ventas, name='lista_ventas'),
    path('<int:id>/', views.detalle_venta, name='detalle_venta'),

    # Registrar factura
    path('crear/', views.crear_venta, name='crear_venta'),

    # Cambiar estado — solo ADMIN
    path('<int:id>/estado/', views.cambiar_estado_venta, name='cambiar_estado_venta'),

]