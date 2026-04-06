from django.urls import path
from apps.productos import views

# Namespace del módulo productos
app_name = 'productos'

urlpatterns = [

    # Listado y detalle
    path('', views.lista_productos, name='lista_productos'),
    path('<int:id>/', views.detalle_producto, name='detalle_producto'),

    # Crear y editar
    path('crear/', views.crear_producto, name='crear_producto'),
    path('<int:id>/editar/', views.editar_producto, name='editar_producto'),

    # Cambiar estado — solo ADMIN
    path('<int:id>/estado/', views.cambiar_estado_producto, name='cambiar_estado_producto'),

    # Modificar stock manualmente — solo ADMIN
    path('<int:id>/stock/', views.modificar_stock, name='modificar_stock'),

]