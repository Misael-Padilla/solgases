from decimal import Decimal
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
            'subtotal', 'iva_porcentaje', 'iva', 'total',
            'estado', 'observaciones',
        ]
        widgets = {
            'fecha_factura': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            # Campos calculados por JavaScript — no editables por el usuario
            'iva':   forms.NumberInput(attrs={'readonly': True}),
            'total': forms.NumberInput(attrs={'readonly': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_factura'].input_formats = ['%Y-%m-%dT%H:%M']

        # Valor inicial del IVA (%) — solo para formularios nuevos
        if not self.instance.pk:
            self.fields['iva_porcentaje'].initial = Decimal('19.00')

    def clean(self):
        """
        Validación cruzada de valores monetarios.
        Verifica que iva y total sean consistentes con el porcentaje aplicado:
        - iva = subtotal × (iva_porcentaje / 100)
        - total = subtotal + iva
        """
        cleaned_data   = super().clean()
        subtotal       = cleaned_data.get('subtotal')
        iva_porcentaje = cleaned_data.get('iva_porcentaje')
        iva            = cleaned_data.get('iva')
        total          = cleaned_data.get('total')

        if all(v is not None for v in [subtotal, iva_porcentaje, iva, total]):
            iva_esperado   = (subtotal * iva_porcentaje / Decimal('100')).quantize(Decimal('0.01'))
            total_esperado = subtotal + iva_esperado

            if iva != iva_esperado:
                raise forms.ValidationError(
                    f'El IVA ({iva}) no coincide con el {iva_porcentaje}% del subtotal. Esperado: {iva_esperado}.'
                )
            if total != total_esperado:
                raise forms.ValidationError(
                    f'El total ({total}) debe ser {subtotal} + {iva_esperado} = {total_esperado}.'
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
        """Cantidad y precio unitario deben ser mayores que cero."""
        cleaned_data    = super().clean()
        cantidad        = cleaned_data.get('cantidad')
        precio_unitario = cleaned_data.get('precio_unitario')

        if cantidad is not None and cantidad <= 0:
            self.add_error('cantidad', 'La cantidad debe ser mayor que cero.')

        if precio_unitario is not None and precio_unitario <= 0:
            self.add_error('precio_unitario', 'El precio unitario debe ser mayor que cero.')

        return cleaned_data


# Formset de detalles — extra=0 porque las filas se agregan dinámicamente con JS
DetalleVentaFormSet = inlineformset_factory(
    FacturaVenta,
    DetalleVenta,
    form=DetalleVentaForm,
    extra=0,
    can_delete=True,
)