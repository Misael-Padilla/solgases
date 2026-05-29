from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from apps.productos.models import Producto
from apps.productos.forms import ProductoForm, StockForm
from apps.usuarios.decoradores import login_requerido, admin_requerido
from apps.usuarios.models import HistorialCambio


@login_requerido
def lista_productos(request):
    """Lista todos los productos del sistema — accesible para ADMIN y EMP."""
    productos = Producto.objects.all().order_by('codigo')
    return render(request, 'productos/lista_productos.html', {'productos': productos})


@login_requerido
def detalle_producto(request, id):
    """Muestra el detalle de un producto específico."""
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'productos/detalle_producto.html', {'producto': producto})


@login_requerido
def crear_producto(request):
    """Crea un nuevo producto — accesible para ADMIN y EMP."""
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado correctamente.')
            return redirect('productos:lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'productos/form_producto.html', {'form': form, 'titulo': 'Crear producto'})


@login_requerido
def editar_producto(request, id):
    """Edita un producto existente — accesible para ADMIN y EMP."""
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('productos:detalle_producto', id=producto.id)
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/form_producto.html', {'form': form, 'titulo': 'Editar producto'})


@admin_requerido
@require_POST
def cambiar_estado_producto(request, id):
    """Activa o desactiva un producto — solo ADMIN. Requiere observación."""
    producto = get_object_or_404(Producto, id=id)
    observacion = request.POST.get('observacion', '').strip()
    if not observacion:
        messages.error(request, 'La observación es obligatoria para cambiar el estado.')
        return redirect('productos:lista_productos')
    if producto.estado == 'ACTIVO':
        producto.estado = 'INACTIVO'
        accion = 'DESACTIVAR'
        messages.success(request, f'Producto {producto.nombre} desactivado.')
    else:
        producto.estado = 'ACTIVO'
        accion = 'ACTIVAR'
        messages.success(request, f'Producto {producto.nombre} activado.')
    producto.modificado_por = request.user
    producto.save()
    HistorialCambio.objects.create(
        modelo='PRODUCTO',
        objeto_id=producto.id,
        objeto_nombre=producto.nombre,
        accion=accion,
        observacion=observacion,
        realizado_por=request.user,
    )
    return redirect('productos:lista_productos')


@admin_requerido
def modificar_stock(request, id):
    """
    Modifica el stock de un producto manualmente.
    Solo ADMIN — correcciones excepcionales con motivo obligatorio.
    """
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            producto.stock = form.cleaned_data['stock']
            motivo = form.cleaned_data['motivo']
            registro = f"\n[{timezone.now().strftime('%d/%m/%Y %H:%M')}] Stock modificado a {producto.stock} — Motivo: {motivo}"
            producto.observaciones = (producto.observaciones or '') + registro
            producto.save()
            messages.success(request, f'Stock de {producto.nombre} actualizado a {producto.stock}.')
            return redirect('productos:detalle_producto', id=producto.id)
    else:
        form = StockForm(initial={'stock': producto.stock})
    return render(request, 'productos/form_stock.html', {'form': form, 'producto': producto})