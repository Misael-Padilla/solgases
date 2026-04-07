from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from apps.ventas.models import FacturaVenta
from apps.ventas.forms import FacturaVentaForm, DetalleVentaFormSet
from apps.usuarios.decoradores import login_requerido, admin_requerido


@login_requerido
def lista_ventas(request):
    """Lista todas las facturas de venta — accesible para ADMIN y EMP."""
    ventas = FacturaVenta.objects.all().order_by('-fecha_registro')
    return render(request, 'ventas/lista_ventas.html', {'ventas': ventas})


@login_requerido
def detalle_venta(request, id):
    """Muestra el detalle de una factura de venta específica."""
    venta = get_object_or_404(FacturaVenta, id=id)
    return render(request, 'ventas/detalle_venta.html', {'venta': venta})


@login_requerido
def crear_venta(request):
    """
    Registra una nueva factura de venta con sus detalles.
    Usa formset para manejar múltiples ítems en el mismo formulario.
    Todo se ejecuta dentro de transaction.atomic() (DA-003).
    """
    if request.method == 'POST':
        form    = FacturaVentaForm(request.POST)
        formset = DetalleVentaFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    # Guarda la cabecera asignando el usuario logueado
                    venta = form.save(commit=False)
                    venta.registrado_por = request.user
                    venta.save()

                    # Asocia el formset a la factura cabecera y guarda los detalles
                    formset.instance = venta
                    formset.save()

                    messages.success(request, f'Factura {venta.numero_factura} registrada correctamente.')
                    return redirect('ventas:detalle_venta', id=venta.id)

            except ValueError as e:
                # Error de stock insuficiente o código no encontrado
                messages.error(request, str(e))

    else:
        form    = FacturaVentaForm()
        formset = DetalleVentaFormSet()

    return render(request, 'ventas/form_venta.html', {
        'form':    form,
        'formset': formset,
        'titulo':  'Registrar factura de venta',
    })


@admin_requerido
def cambiar_estado_venta(request, id):
    """Desactiva una factura de venta — solo ADMIN. Sin eliminación física."""
    venta = get_object_or_404(FacturaVenta, id=id)
    if venta.estado == 'ACTIVO':
        venta.estado = 'INACTIVO'
        messages.success(request, f'Factura {venta.numero_factura} desactivada.')
    else:
        venta.estado = 'ACTIVO'
        messages.success(request, f'Factura {venta.numero_factura} activada.')
    venta.save()
    return redirect('ventas:lista_ventas')