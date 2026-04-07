from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from apps.compras.models import FacturaCompra
from apps.compras.forms import FacturaCompraForm, DetalleCompraFormSet
from apps.usuarios.decoradores import login_requerido, admin_requerido


@login_requerido
def lista_compras(request):
    """Lista todas las facturas de compra — accesible para ADMIN y EMP."""
    compras = FacturaCompra.objects.all().order_by('-fecha_registro')
    return render(request, 'compras/lista_compras.html', {'compras': compras})


@login_requerido
def detalle_compra(request, id):
    """Muestra el detalle de una factura de compra específica."""
    compra = get_object_or_404(FacturaCompra, id=id)
    return render(request, 'compras/detalle_compra.html', {'compra': compra})


@login_requerido
def crear_compra(request):
    """
    Registra una nueva factura de compra con sus detalles.
    Usa formset para manejar múltiples ítems en el mismo formulario.
    Todo se ejecuta dentro de transaction.atomic() (DA-003).
    """
    if request.method == 'POST':
        form    = FacturaCompraForm(request.POST)
        formset = DetalleCompraFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    # Guarda la cabecera asignando el usuario logueado
                    compra = form.save(commit=False)
                    compra.registrado_por = request.user
                    compra.save()

                    # Asocia el formset a la factura cabecera y guarda los detalles
                    formset.instance = compra
                    formset.save()

                    messages.success(request, f'Factura {compra.numero_factura} registrada correctamente.')
                    return redirect('compras:detalle_compra', id=compra.id)

            except ValueError as e:
                # Error de stock insuficiente o código no encontrado
                messages.error(request, str(e))

    else:
        form    = FacturaCompraForm()
        formset = DetalleCompraFormSet()

    return render(request, 'compras/form_compra.html', {
        'form':    form,
        'formset': formset,
        'titulo':  'Registrar factura de compra',
    })


@admin_requerido
def cambiar_estado_compra(request, id):
    """Desactiva una factura de compra — solo ADMIN. Sin eliminación física."""
    compra = get_object_or_404(FacturaCompra, id=id)
    if compra.estado == 'ACTIVO':
        compra.estado = 'INACTIVO'
        messages.success(request, f'Factura {compra.numero_factura} desactivada.')
    else:
        compra.estado = 'ACTIVO'
        messages.success(request, f'Factura {compra.numero_factura} activada.')
    compra.save()
    return redirect('compras:lista_compras')