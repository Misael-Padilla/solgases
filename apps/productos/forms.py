from django import forms
from apps.productos.models import Producto


class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = [
            'codigo', 'nombre', 'categoria', 'genero', 'talla',
            'precio_compra', 'precio_venta',
            'stock', 'stock_minimo', 'stock_maximo',
            'estado', 'imagen', 'observaciones',
        ]
        labels = {
            'codigo':        'Código',
            'categoria':     'Categoría',
            'genero':        'Género',
            'precio_compra': 'Precio de compra',
            'precio_venta':  'Precio de venta',
            'stock':         'Stock inicial',
            'stock_minimo':  'Stock mínimo',
            'stock_maximo':  'Stock máximo',
            'imagen':        'Imagen del producto',
        }

    def __init__(self, *args, **kwargs):
        es_edicion = kwargs.pop('es_edicion', False)
        super().__init__(*args, **kwargs)
        if es_edicion:
            # En edición el stock se gestiona exclusivamente via modificar_stock
            self.fields.pop('stock')

    def clean(self):
        """
        Validaciones cruzadas:
        - stock_minimo debe ser menor que stock_maximo.
        - precio_compra y precio_venta deben ser mayores que cero.
        - precio_venta no puede ser menor que precio_compra.
        """
        cleaned_data  = super().clean()
        stock_minimo  = cleaned_data.get('stock_minimo')
        stock_maximo  = cleaned_data.get('stock_maximo')
        precio_compra = cleaned_data.get('precio_compra')
        precio_venta  = cleaned_data.get('precio_venta')

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

        # Validación de regla de negocio: precio de venta >= precio de compra
        if precio_compra is not None and precio_venta is not None:
            if precio_venta < precio_compra:
                self.add_error(
                    'precio_venta',
                    'El precio de venta no puede ser menor que el precio de compra.'
                )

        return cleaned_data


class StockForm(forms.Form):

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
        widget=forms.Textarea(attrs={
            'placeholder': 'Explica por qué se modifica el stock...',
            'rows': 3,
        }),
    )
