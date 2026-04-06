from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from apps.productos.models import Producto
from apps.productos.forms import ProductoForm, StockForm
from apps.usuarios.decoradores import login_requerido, admin_requerido


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
def cambiar_estado_producto(request, id):
    """Activa o desactiva un producto — solo ADMIN. Sin eliminación física."""
    producto = get_object_or_404(Producto, id=id)
    if producto.estado == 'ACTIVO':
        producto.estado = 'INACTIVO'
        messages.success(request, f'Producto {producto.nombre} desactivado.')
    else:
        producto.estado = 'ACTIVO'
        messages.success(request, f'Producto {producto.nombre} activado.')
    producto.save()
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
            producto.save()
            messages.success(request, f'Stock de {producto.nombre} actualizado a {producto.stock}.')
            return redirect('productos:detalle_producto', id=producto.id)
    else:
        form = StockForm(initial={'stock': producto.stock})
    return render(request, 'productos/form_stock.html', {'form': form, 'producto': producto})