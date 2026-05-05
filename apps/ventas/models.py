from django.db import models
from django.db import transaction
from apps.usuarios.models import Cliente, Usuario
from apps.productos.models import Producto
from apps.insumos.models import Insumo


class FacturaVenta(models.Model):
    """Cabecera de factura de venta a un cliente (DA-003)."""

    METODO_PAGO_CHOICES = [
        ('EFECTIVO', 'Efectivo'),
        ('TRANSFERENCIA', 'Transferencia Bancaria'),
    ]

    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]

    numero_factura  = models.CharField(max_length=30, unique=True)
    cliente         = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='facturas_venta')
    registrado_por  = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='ventas_registradas')
    recibido_por    = models.CharField(max_length=200, null=True, blank=True)

    # Fecha real de la venta vs fecha de registro en el sistema
    fecha_factura   = models.DateTimeField()
    fecha_registro  = models.DateTimeField(auto_now_add=True)

    metodo_pago     = models.CharField(max_length=15, choices=METODO_PAGO_CHOICES)

    # Valores monetarios — IVA se almacena como porcentaje y como monto para trazabilidad
    subtotal        = models.DecimalField(max_digits=12, decimal_places=2)
    iva_porcentaje  = models.DecimalField(max_digits=5, decimal_places=2, default=19.00)
    iva             = models.DecimalField(max_digits=12, decimal_places=2)
    total           = models.DecimalField(max_digits=12, decimal_places=2)

    estado          = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='ACTIVO')
    observaciones   = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'factura_venta'
        verbose_name = 'Factura de Venta'
        verbose_name_plural = 'Facturas de Venta'

    def __str__(self):
        return f'Venta {self.numero_factura} — {self.cliente}'


class DetalleVenta(models.Model):
    """
    Línea/ítem de una factura de venta.
    Al guardar, descuenta automáticamente el stock del producto o insumo (DA-003).
    """

    TIPO_ITEM_CHOICES = [
        ('PRODUCTO', 'Producto'),
        ('INSUMO', 'Insumo'),
    ]

    factura_venta   = models.ForeignKey(FacturaVenta, on_delete=models.PROTECT, related_name='detalles')
    tipo_item       = models.CharField(max_length=10, choices=TIPO_ITEM_CHOICES)
    codigo_item     = models.CharField(max_length=20)
    descripcion     = models.CharField(max_length=200)  # Copia fija al momento de la venta
    cantidad        = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal        = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'detalle_venta'
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Venta'

    def __str__(self):
        return f'{self.tipo_item} {self.codigo_item} x{self.cantidad}'

    def save(self, *args, **kwargs):
        """Descuenta stock validando disponibilidad. Lanza ValueError si no hay suficiente."""
        with transaction.atomic():
            if self.tipo_item == 'PRODUCTO':
                try:
                    producto = Producto.objects.get(codigo=self.codigo_item)
                    if producto.stock < self.cantidad:
                        raise ValueError(f'Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}')
                    producto.stock -= self.cantidad
                    producto.save()
                except Producto.DoesNotExist:
                    raise ValueError(f'No existe un producto con código {self.codigo_item}')

            elif self.tipo_item == 'INSUMO':
                try:
                    insumo = Insumo.objects.get(codigo=self.codigo_item)
                    if insumo.stock < self.cantidad:
                        raise ValueError(f'Stock insuficiente para {insumo.nombre}. Disponible: {insumo.stock}')
                    insumo.stock -= self.cantidad
                    insumo.save()
                except Insumo.DoesNotExist:
                    raise ValueError(f'No existe un insumo con código {self.codigo_item}')

            super().save(*args, **kwargs)