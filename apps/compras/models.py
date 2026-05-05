from django.db import models
from django.db import transaction
from apps.usuarios.models import Proveedor, Usuario
from apps.productos.models import Producto
from apps.insumos.models import Insumo


class FacturaCompra(models.Model):
    """Cabecera de factura de compra a un proveedor (DA-003)."""

    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]

    numero_factura  = models.CharField(max_length=30, unique=True)
    proveedor       = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='facturas_compra')
    registrado_por  = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='compras_registradas')

    # Fecha real de la compra vs fecha de registro en el sistema
    fecha_factura   = models.DateTimeField()
    fecha_registro  = models.DateTimeField(auto_now_add=True)

    # Valores monetarios — IVA se almacena como porcentaje y como monto para trazabilidad
    subtotal        = models.DecimalField(max_digits=12, decimal_places=2)
    iva_porcentaje  = models.DecimalField(max_digits=5, decimal_places=2, default=19.00)
    iva             = models.DecimalField(max_digits=12, decimal_places=2)
    total           = models.DecimalField(max_digits=12, decimal_places=2)

    estado          = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='ACTIVO')
    observaciones   = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'factura_compra'
        verbose_name = 'Factura de Compra'
        verbose_name_plural = 'Facturas de Compra'

    def __str__(self):
        return f'Compra {self.numero_factura} — {self.proveedor}'


class DetalleCompra(models.Model):
    """
    Línea/ítem de una factura de compra.
    Al guardar, actualiza automáticamente el stock del producto o insumo (DA-003).
    """

    TIPO_ITEM_CHOICES = [
        ('PRODUCTO', 'Producto'),
        ('INSUMO', 'Insumo'),
    ]

    factura_compra  = models.ForeignKey(FacturaCompra, on_delete=models.PROTECT, related_name='detalles')
    tipo_item       = models.CharField(max_length=10, choices=TIPO_ITEM_CHOICES)
    codigo_item     = models.CharField(max_length=20)
    descripcion     = models.CharField(max_length=200)  # Copia fija al momento de la compra
    cantidad        = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal        = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'detalle_compra'
        verbose_name = 'Detalle de Compra'
        verbose_name_plural = 'Detalles de Compra'

    def __str__(self):
        return f'{self.tipo_item} {self.codigo_item} x{self.cantidad}'

    def save(self, *args, **kwargs):
        """Suma stock y actualiza precio_compra. Si el ítem no existe, lo crea automáticamente."""
        with transaction.atomic():
            if self.tipo_item == 'PRODUCTO':
                try:
                    producto = Producto.objects.get(codigo=self.codigo_item)
                    producto.stock += self.cantidad
                    producto.precio_compra = self.precio_unitario
                    producto.save()
                except Producto.DoesNotExist:
                    Producto.objects.create(
                        codigo=self.codigo_item,
                        nombre=self.descripcion,
                        categoria='DOTACION',
                        genero='Unisex',
                        precio_compra=self.precio_unitario,
                        precio_venta=self.precio_unitario,
                        stock=self.cantidad,
                        stock_minimo=0,
                        stock_maximo=100,
                    )
            elif self.tipo_item == 'INSUMO':
                try:
                    insumo = Insumo.objects.get(codigo=self.codigo_item)
                    insumo.stock += self.cantidad
                    insumo.precio_compra = self.precio_unitario
                    insumo.save()
                except Insumo.DoesNotExist:
                    Insumo.objects.create(
                        codigo=self.codigo_item,
                        nombre=self.descripcion,
                        subcategoria='GAS',
                        unidad_medida='Unidades',
                        precio_compra=self.precio_unitario,
                        stock=self.cantidad,
                        stock_minimo=0,
                        stock_maximo=100,
                        proveedor=self.factura_compra.proveedor,
                    )
            super().save(*args, **kwargs)