from django import forms
from apps.insumos.models import Insumo


class InsumoForm(forms.ModelForm):
    """
    Formulario para crear y editar insumos.
    Incluye validación cruzada de umbrales de stock (DA-002).
    """

    class Meta:
        model = Insumo
        fields = [
            'codigo', 'nombre', 'subcategoria', 'unidad_medida',
            'precio_compra',
            'stock', 'stock_minimo', 'stock_maximo',
            'proveedor',
            'estado', 'imagen', 'observaciones',
        ]

    def clean(self):
        """
        Validación cruzada:
        - stock_minimo debe ser menor que stock_maximo (DA-002).
        - precio_compra debe ser mayor que cero.
        """
        cleaned_data = super().clean()
        stock_minimo  = cleaned_data.get('stock_minimo')
        stock_maximo  = cleaned_data.get('stock_maximo')
        precio_compra = cleaned_data.get('precio_compra')

        # Validación de umbrales de stock (DA-002)
        if stock_minimo is not None and stock_maximo is not None:
            if stock_minimo >= stock_maximo:
                raise forms.ValidationError(
                    'El stock mínimo debe ser menor que el stock máximo.'
                )

        # Validación de precio
        if precio_compra is not None and precio_compra <= 0:
            self.add_error('precio_compra', 'El precio de compra debe ser mayor que cero.')

        return cleaned_data


class StockInsumoForm(forms.Form):
    """
    Formulario para modificar el stock de un insumo manualmente.
    Solo accesible para el rol ADMIN — correcciones excepcionales.
    """

    # Nuevo valor de stock — debe ser mayor o igual a cero
    stock = forms.IntegerField(
        label='Nuevo stock',
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': '0'}),
    )

    # Motivo obligatorio para trazabilidad
    motivo = forms.CharField(
        label='Motivo de la modificación',
        max_length=200,
        widget=forms.Textarea(attrs={
            'placeholder': 'Explica por qué se modifica el stock...',
            'rows': 3
        }),
    )