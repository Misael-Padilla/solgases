# === Imports de Django ===
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.db.models import F
from django.views.decorators.http import require_POST

# === Imports locales ===
from apps.usuarios.decoradores import login_requerido



@login_requerido
def inicio(request):
    """Vista principal del dashboard — muestra métricas y alertas de stock."""
    from apps.productos.models import Producto
    from apps.insumos.models import Insumo
    from apps.usuarios.models import Cliente
    from apps.ventas.models import FacturaVenta
    from apps.compras.models import FacturaCompra
    from django.utils import timezone

    # Métricas generales
    total_productos = Producto.objects.filter(estado='ACTIVO').count()
    total_insumos   = Insumo.objects.filter(estado='ACTIVO').count()
    total_clientes  = Cliente.objects.filter(estado='ACTIVO').count()

    # Ventas del mes actual
    hoy = timezone.now()
    ventas_mes = FacturaVenta.objects.filter(
        fecha_factura__year=hoy.year,
        fecha_factura__month=hoy.month,
        estado='ACTIVO'
    ).count()

    # Alertas de stock bajo — productos e insumos bajo su umbral mínimo (DA-002)
    productos_bajo = Producto.objects.filter(estado='ACTIVO').filter(
        stock__lte=F('stock_minimo')
    )
    insumos_bajo = Insumo.objects.filter(estado='ACTIVO').filter(
        stock__lte=F('stock_minimo')
    )
    alertas_stock_bajo = list(productos_bajo) + list(insumos_bajo)

    # Alertas de sobrestock — productos e insumos sobre su umbral máximo (DA-002)
    productos_alto = Producto.objects.filter(estado='ACTIVO').filter(
        stock__gte=F('stock_maximo')
    )
    insumos_alto = Insumo.objects.filter(estado='ACTIVO').filter(
        stock__gte=F('stock_maximo')
    )
    alertas_sobrestock = list(productos_alto) + list(insumos_alto)

    # Últimas 5 ventas registradas
    ultimas_ventas = FacturaVenta.objects.filter(
        estado='ACTIVO'
    ).order_by('-fecha_registro')[:5]

    # Últimas 5 compras registradas
    ultimas_compras = FacturaCompra.objects.filter(
        estado='ACTIVO'
    ).order_by('-fecha_registro')[:5]

    context = {
        'breadcrumbs': [
            {'nombre': 'Inicio', 'url': None},
        ],
        'total_productos':    total_productos,
        'total_insumos':      total_insumos,
        'total_clientes':     total_clientes,
        'ventas_mes':         ventas_mes,
        'alertas_stock_bajo': alertas_stock_bajo,
        'alertas_sobrestock': alertas_sobrestock,
        'ultimas_ventas':     ultimas_ventas,
        'ultimas_compras':    ultimas_compras,
    }

    return render(request, 'core/inicio.html', context)


@login_requerido
def manual(request):
    """Vista del manual de usuario — requiere autenticación."""
    context = {
        'breadcrumbs': [
            {'nombre': 'Inicio', 'url': '/'},
            {'nombre': 'Manual de usuario', 'url': None},
        ],
    }
    return render(request, 'core/manual.html', context)


@require_POST
def cerrar_sesion(request):
    """Cierra la sesión del usuario y redirige al login.

    Solo acepta método POST para prevenir ataques CSRF
    que podrían cerrar la sesión mediante un enlace GET.
    """
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('core:login')


def login_view(request):
    """Vista del login — procesa credenciales y redirige al dashboard.

    Verifica cuatro condiciones antes de permitir el acceso:
    1. Que el correo exista en la base de datos.
    2. Que la cuenta no esté bloqueada por intentos fallidos (django-axes).
    3. Que la contraseña sea correcta (authenticate).
    4. Que el usuario no esté inactivo (estado != 'INACTIVO').
    """
    # Si ya está autenticado, redirige al dashboard directamente
    if request.user.is_authenticated:
        return redirect('core:inicio')

    if request.method == 'POST':
        correo = request.POST.get('username')
        password = request.POST.get('password')

        # 1. Verificar si el correo existe en la base de datos
        User = get_user_model()
        if not User.objects.filter(**{User.USERNAME_FIELD: correo}).exists():
            messages.error(
                request,
                'El correo ingresado no está registrado.'
            )
            return render(request, 'core/login.html')

        # 2. Intentar autenticación
        user = authenticate(request, username=correo, password=password)

        if user is not None:
            # 3. Verificar si el usuario está inactivo
            if user.estado == 'INACTIVO':
                messages.error(
                    request,
                    'Esta cuenta está inactiva. Contacte al administrador.'
                )
                return render(request, 'core/login.html')

            # Credenciales correctas y usuario activo — inicia sesión
            login(request, user)
            return redirect('core:inicio')
        else:
            # 4. Correo existe pero contraseña incorrecta
            messages.error(
                request,
                'La contraseña es incorrecta.'
            )
            return render(request, 'core/login.html')

    # Método GET — muestra el formulario vacío
    return render(request, 'core/login.html')