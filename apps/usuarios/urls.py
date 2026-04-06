from django.urls import path
from apps.usuarios import views

# Namespace del módulo usuarios
app_name = 'usuarios'

urlpatterns = [

    # ---- Usuarios ----
    path('', views.lista_usuarios, name='lista_usuarios'),
    path('<int:id>/', views.detalle_usuario, name='detalle_usuario'),
    path('crear/', views.crear_usuario, name='crear_usuario'),
    path('<int:id>/editar/', views.editar_usuario, name='editar_usuario'),
    path('<int:id>/estado/', views.cambiar_estado_usuario, name='cambiar_estado_usuario'),

    # ---- Clientes ----
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/<int:id>/', views.detalle_cliente, name='detalle_cliente'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/<int:id>/editar/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:id>/estado/', views.cambiar_estado_cliente, name='cambiar_estado_cliente'),

    # ---- Proveedores ----
    path('proveedores/', views.lista_proveedores, name='lista_proveedores'),
    path('proveedores/<int:id>/', views.detalle_proveedor, name='detalle_proveedor'),
    path('proveedores/crear/', views.crear_proveedor, name='crear_proveedor'),
    path('proveedores/<int:id>/editar/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/<int:id>/estado/', views.cambiar_estado_proveedor, name='cambiar_estado_proveedor'),

]