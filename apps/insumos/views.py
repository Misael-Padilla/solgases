from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from apps.insumos.models import Insumo
from apps.insumos.forms import InsumoForm, StockInsumoForm
from apps.usuarios.decoradores import login_requerido, admin_requerido


@login_requerido
def lista_insumos(request):
    """Lista todos los insumos del sistema — accesible para ADMIN y EMP."""
    insumos = Insumo.objects.all().order_by('codigo')
    return render(request, 'insumos/lista_insumos.html', {'insumos': insumos})


@login_requerido
def detalle_insumo(request, id):
    """Muestra el detalle de un insumo específico."""
    insumo = get_object_or_404(Insumo, id=id)
    return render(request, 'insumos/detalle_insumo.html', {'insumo': insumo})


@login_requerido
def crear_insumo(request):
    """Crea un nuevo insumo — accesible para ADMIN y EMP."""
    if request.method == 'POST':
        form = InsumoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Insumo creado correctamente.')
            return redirect('insumos:lista_insumos')
    else:
        form = InsumoForm()
    return render(request, 'insumos/form_insumo.html', {'form': form, 'titulo': 'Crear insumo'})


@login_requerido
def editar_insumo(request, id):
    """Edita un insumo existente — accesible para ADMIN y EMP."""
    insumo = get_object_or_404(Insumo, id=id)
    if request.method == 'POST':
        form = InsumoForm(request.POST, request.FILES, instance=insumo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Insumo actualizado correctamente.')
            return redirect('insumos:detalle_insumo', id=insumo.id)
    else:
        form = InsumoForm(instance=insumo)
    return render(request, 'insumos/form_insumo.html', {'form': form, 'titulo': 'Editar insumo'})


@admin_requerido
def cambiar_estado_insumo(request, id):
    """Activa o desactiva un insumo — solo ADMIN. Sin eliminación física."""
    insumo = get_object_or_404(Insumo, id=id)
    if insumo.estado == 'ACTIVO':
        insumo.estado = 'INACTIVO'
        messages.success(request, f'Insumo {insumo.nombre} desactivado.')
    else:
        insumo.estado = 'ACTIVO'
        messages.success(request, f'Insumo {insumo.nombre} activado.')
    insumo.save()
    return redirect('insumos:lista_insumos')


@admin_requerido
def modificar_stock_insumo(request, id):
    """
    Modifica el stock de un insumo manualmente.
    Solo ADMIN — correcciones excepcionales con motivo obligatorio.
    """
    insumo = get_object_or_404(Insumo, id=id)
    if request.method == 'POST':
        form = StockInsumoForm(request.POST)
        if form.is_valid():
            insumo.stock = form.cleaned_data['stock']
            insumo.save()
            messages.success(request, f'Stock de {insumo.nombre} actualizado a {insumo.stock}.')
            return redirect('insumos:detalle_insumo', id=insumo.id)
    else:
        form = StockInsumoForm(initial={'stock': insumo.stock})
    return render(request, 'insumos/form_stock_insumo.html', {'form': form, 'insumo': insumo})