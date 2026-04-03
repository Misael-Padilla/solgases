from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.usuarios.models import Usuario, Cliente, Proveedor


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    # Campos que se muestran en el listado de usuarios
    list_display = ('correo_electronico', 'nombres', 'apellidos', 'rol', 'estado')
    list_filter = ('rol', 'estado')
    search_fields = ('correo_electronico', 'nombres', 'apellidos', 'identificacion')
    ordering = ('correo_electronico',)

    # Campos que se muestran al editar un usuario existente
    fieldsets = (
        ('Credenciales', {'fields': ('correo_electronico', 'password')}),
        ('Información personal', {'fields': ('tipo_identificacion', 'identificacion', 'nombres', 'apellidos', 'telefono', 'direccion', 'ciudad', 'departamento')}),
        ('Sistema', {'fields': ('rol', 'estado', 'imagen', 'observaciones')}),
        ('Permisos', {'fields': ('is_staff', 'is_superuser')}),
    )

    # Campos que se muestran al crear un usuario nuevo desde el admin
    add_fieldsets = (
        ('Nuevo usuario', {
            'classes': ('wide',),
            'fields': ('correo_electronico', 'nombres', 'apellidos', 'identificacion', 'password1', 'password2', 'rol'),
        }),
    )

    # Campo de login personalizado
    USERNAME_FIELD = 'correo_electronico'


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    # Campos que se muestran en el listado de clientes
    list_display = ('identificacion', 'tipo_identificacion', 'telefono', 'ciudad', 'estado')
    list_filter = ('tipo_identificacion', 'estado')
    search_fields = ('identificacion', 'nombres', 'apellidos', 'razon_social')
    ordering = ('identificacion',)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    # Campos que se muestran en el listado de proveedores
    list_display = ('identificacion', 'tipo_identificacion', 'telefono', 'ciudad', 'estado')
    list_filter = ('tipo_identificacion', 'estado')
    search_fields = ('identificacion', 'nombres', 'apellidos', 'razon_social')
    ordering = ('identificacion',)