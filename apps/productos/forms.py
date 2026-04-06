from django import forms
from apps.productos.models import Producto


class ProductoForm(forms.ModelForm):
    """
    Formulario para crear y editar productos.
    Incluye validación cruzada de umbrales de stock (DA-002).
    """

    class Meta:
        model = Producto
        fields = [
            'codigo', 'nombre', 'categoria', 'genero', 'talla',
            'precio_compra', 'precio_venta',
            'stock', 'stock_minimo', 'stock_maximo',
            'estado', 'imagen', 'observaciones',
        ]

    def clean(self):
        """
        Validación cruzada:
        - stock_minimo debe ser menor que stock_maximo.
        - precio_compra y precio_venta deben ser mayores que cero.
        """
        cleaned_data = super().clean()
        stock_minimo = cleaned_data.get('stock_minimo')
        stock_maximo = cleaned_data.get('stock_maximo')
        precio_compra = cleaned_data.get('precio_compra')
        precio_venta = cleaned_data.get('precio_venta')

        # Validación de umbrales de stock (DA-002)
        if stock_minimo is not None and stock_maximo is not None:
            if stock_minimo >= stock_maximo:
                raise forms.ValidationError(
                    'El stock mínimo debe ser menor que el stock máximo.'
                )

        # Validación de precios
        if precio_compra is not None and precio_compra <= 0:
            self.add_error('precio_compra', 'El precio de compra debe ser mayor que cero.')

        if precio_venta is not None and precio_venta <= 0:
            self.add_error('precio_venta', 'El precio de venta debe ser mayor que cero.')

        return cleaned_data


class StockForm(forms.Form):
    """
    Formulario para modificar el stock manualmente.
    Solo accesible para el rol ADMIN — correcciones excepcionales.
    """

    # Nuevo valor de stock — debe ser mayor o igual a cero
    stock = forms.IntegerField(
        label='Nuevo stock',
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': '0'}),
    )

    # Motivo de la modificación — para trazabilidad
    motivo = forms.CharField(
        label='Motivo de la modificación',
        max_length=200,
        widget=forms.Textarea(attrs={'placeholder': 'Explica por qué se modifica el stock...', 'rows': 3}),
    )