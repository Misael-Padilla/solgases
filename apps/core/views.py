from django.shortcuts import render
from apps.usuarios.decoradores import login_requerido
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db import models



@login_requerido
def inicio(request):
    """Vista principal del dashboard — muestra métricas y alertas de stock."""
    from apps.productos.models import Producto
    from apps.insumos.models import Insumo
    from apps.usuarios.models import Cliente
    from apps.ventas.models import FacturaVenta
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
        stock__lte=models.F('stock_minimo')
    )
    insumos_bajo = Insumo.objects.filter(estado='ACTIVO').filter(
        stock__lte=models.F('stock_minimo')
    )
    alertas_stock_bajo = list(productos_bajo) + list(insumos_bajo)

    # Alertas de sobrestock — productos e insumos sobre su umbral máximo (DA-002)
    productos_alto = Producto.objects.filter(estado='ACTIVO').filter(
        stock__gte=models.F('stock_maximo')
    )
    insumos_alto = Insumo.objects.filter(estado='ACTIVO').filter(
        stock__gte=models.F('stock_maximo')
    )
    alertas_sobrestock = list(productos_alto) + list(insumos_alto)

    # Últimas 5 ventas registradas
    ultimas_ventas = FacturaVenta.objects.filter(estado='ACTIVO').order_by('-fecha_registro')[:5]

    # Últimas 5 compras registradas
    from apps.compras.models import FacturaCompra
    ultimas_compras = FacturaCompra.objects.filter(estado='ACTIVO').order_by('-fecha_registro')[:5]

    context = {
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
    return render(request, 'core/manual.html')


def cerrar_sesion(request):
    """Cierra la sesión del usuario y redirige al login."""
    logout(request)
    return redirect('core:login')


def login_view(request):
    """Vista del login — procesa credenciales y redirige al dashboard."""
    # Si ya está autenticado, redirige al dashboard directamente
    if request.user.is_authenticated:
        return redirect('core:inicio')

    if request.method == 'POST':
        correo = request.POST.get('username')
        password = request.POST.get('password')

        # Verifica las credenciales contra la base de datos
        user = authenticate(request, username=correo, password=password)

        if user is not None:
            # Credenciales correctas — inicia sesión y redirige al dashboard
            user.estado == 'INACTIVO'
            login(request, user)
            return redirect('core:inicio')
        else:
            # Credenciales incorrectas — regresa al login con error
            from django.contrib.auth.forms import AuthenticationForm
            form = AuthenticationForm()
            form.errors['__all__'] = ['Credenciales incorrectas']
            return render(request, 'core/login.html', {'form': form})

    # Método GET — muestra el formulario vacío
    from django.contrib.auth.forms import AuthenticationForm
    form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})