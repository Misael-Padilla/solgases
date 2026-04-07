from django import forms
from django.forms import inlineformset_factory
from apps.ventas.models import FacturaVenta, DetalleVenta


class FacturaVentaForm(forms.ModelForm):
    """
    Formulario para la cabecera de la factura de venta.
    El campo registrado_por se asigna automáticamente desde la vista.
    """

    class Meta:
        model = FacturaVenta
        fields = [
            'numero_factura', 'cliente', 'recibido_por',
            'fecha_factura', 'metodo_pago',
            'subtotal', 'iva', 'total',
            'estado', 'observaciones',
        ]
        widgets = {
            # Input de fecha con tipo datetime-local para mejor UX
            'fecha_factura': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Formato correcto para el widget datetime-local
        self.fields['fecha_factura'].input_formats = ['%Y-%m-%dT%H:%M']

    def clean(self):
        """
        Validación cruzada:
        - total debe ser igual a subtotal + iva.
        """
        cleaned_data = super().clean()
        subtotal = cleaned_data.get('subtotal')
        iva      = cleaned_data.get('iva')
        total    = cleaned_data.get('total')

        if subtotal is not None and iva is not None and total is not None:
            if total != subtotal + iva:
                raise forms.ValidationError(
                    f'El total ({total}) debe ser igual a subtotal ({subtotal}) + IVA ({iva}).'
                )
        return cleaned_data


class DetalleVentaForm(forms.ModelForm):
    """
    Formulario para cada ítem de la factura de venta.
    Se usa dentro de un formset para manejar múltiples ítems.
    """

    class Meta:
        model = DetalleVenta
        fields = [
            'tipo_item', 'codigo_item', 'descripcion',
            'cantidad', 'precio_unitario', 'subtotal',
        ]

    def clean(self):
        """Validación: cantidad y precio deben ser mayores que cero."""
        cleaned_data    = super().clean()
        cantidad        = cleaned_data.get('cantidad')
        precio_unitario = cleaned_data.get('precio_unitario')

        if cantidad is not None and cantidad <= 0:
            self.add_error('cantidad', 'La cantidad debe ser mayor que cero.')

        if precio_unitario is not None and precio_unitario <= 0:
            self.add_error('precio_unitario', 'El precio unitario debe ser mayor que cero.')

        return cleaned_data


# Formset — permite manejar múltiples DetalleVenta dentro de una misma vista
# extra=0 → sin filas vacías al cargar — se agregan dinámicamente con JS
# can_delete=True → permite eliminar filas del formset
DetalleVentaFormSet = inlineformset_factory(
    FacturaVenta,
    DetalleVenta,
    form=DetalleVentaForm,
    extra=0,
    can_delete=True,
)