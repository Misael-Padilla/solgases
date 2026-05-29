from django import forms
from apps.insumos.models import Insumo
from apps.usuarios.models import Proveedor


class InsumoForm(forms.ModelForm):

    class Meta:
        model = Insumo
        fields = [
            'codigo', 'nombre', 'subcategoria', 'unidad_medida',
            'precio_compra',
            'stock', 'stock_minimo', 'stock_maximo',
            'proveedor',
            'estado', 'imagen', 'observaciones',
        ]
        labels = {
            'subcategoria':  'Subcategoría',
            'unidad_medida': 'Unidad de medida',
            'precio_compra': 'Precio de compra',
            'stock':         'Stock inicial',
            'stock_minimo':  'Stock mínimo',
            'stock_maximo':  'Stock máximo',
            'imagen':        'Imagen del insumo',
        }

    def __init__(self, *args, **kwargs):
        es_edicion = kwargs.pop('es_edicion', False)
        super().__init__(*args, **kwargs)
        # Solo proveedores activos en el desplegable
        self.fields['proveedor'].queryset = Proveedor.objects.filter(
            estado='ACTIVO'
        ).order_by('razon_social', 'nombres')
        if es_edicion:
            # En edición el stock se gestiona exclusivamente via modificar_stock_insumo
            self.fields.pop('stock')

    def clean(self):
        """
        Validaciones cruzadas:
        - stock_minimo debe ser menor que stock_maximo (DA-002).
        - precio_compra debe ser mayor que cero.
        """
        cleaned_data  = super().clean()
        stock_minimo  = cleaned_data.get('stock_minimo')
        stock_maximo  = cleaned_data.get('stock_maximo')
        precio_compra = cleaned_data.get('precio_compra')

        if stock_minimo is not None and stock_maximo is not None:
            if stock_minimo >= stock_maximo:
                raise forms.ValidationError(
                    'El stock mínimo debe ser menor que el stock máximo.'
                )

        if precio_compra is not None and precio_compra <= 0:
            self.add_error('precio_compra', 'El precio de compra debe ser mayor que cero.')

        return cleaned_data


class StockInsumoForm(forms.Form):

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
            'rows': 3,
        }),
    )
