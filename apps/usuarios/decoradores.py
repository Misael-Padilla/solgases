from django.shortcuts import redirect
from functools import wraps


def admin_requerido(funcion):
    """
    Decorador que restringe el acceso exclusivamente al rol ADMIN.
    Si el usuario es EMP, redirige al dashboard con acceso denegado.
    """
    @wraps(funcion)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('core:login')
        if request.user.rol != 'ADMIN':
            return redirect('core:inicio')
        return funcion(request, *args, **kwargs)
    return wrapper


def login_requerido(funcion):
    """
    Decorador que verifica que el usuario esté autenticado y activo.
    Reemplaza al @login_required de Django para usar nuestra lógica de roles.
    """
    @wraps(funcion)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('core:login')
        if request.user.estado == 'INACTIVO':
            from django.contrib.auth import logout
            logout(request)
            return redirect('core:login')
        return funcion(request, *args, **kwargs)
    return wrapper