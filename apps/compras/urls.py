from django.urls import path
from apps.compras import views

# Namespace del módulo compras
app_name = 'compras'

urlpatterns = [

    # Listado y detalle
    path('', views.lista_compras, name='lista_compras'),
    path('<int:id>/', views.detalle_compra, name='detalle_compra'),

    # Registrar factura
    path('crear/', views.crear_compra, name='crear_compra'),

    # Cambiar estado — solo ADMIN
    path('<int:id>/estado/', views.cambiar_estado_compra, name='cambiar_estado_compra'),

]