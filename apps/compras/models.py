from django.db import models
from django.db import transaction
from apps.usuarios.models import Proveedor, Usuario
from apps.productos.models import Producto
from apps.insumos.models import Insumo


class FacturaCompra(models.Model):

    # Opciones para el campo estado
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]

    # Identificación de la factura
    numero_factura  = models.CharField(max_length=30, unique=True)

    # Relaciones — quién vendió y quién registró
    proveedor       = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='facturas_compra')
    registrado_por  = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='compras_registradas')

    # Fechas — fecha real de la compra vs fecha de registro en el sistema
    fecha_factura   = models.DateTimeField()
    fecha_registro  = models.DateTimeField(auto_now_add=True)

    # Valores monetarios — siempre Decimal, nunca float
    subtotal        = models.DecimalField(max_digits=12, decimal_places=2)
    iva             = models.DecimalField(max_digits=12, decimal_places=2)
    total           = models.DecimalField(max_digits=12, decimal_places=2)

    # Estado y metadatos
    estado          = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='ACTIVO')
    observaciones   = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'factura_compra'
        verbose_name = 'Factura de Compra'
        verbose_name_plural = 'Facturas de Compra'

    def __str__(self):
        return f'Compra {self.numero_factura} — {self.proveedor}'


class DetalleCompra(models.Model):

    # Opciones para el campo tipo_item
    TIPO_ITEM_CHOICES = [
        ('PRODUCTO', 'Producto'),
        ('INSUMO', 'Insumo'),
    ]

    # Relación con la factura cabecera
    factura_compra  = models.ForeignKey(FacturaCompra, on_delete=models.PROTECT, related_name='detalles')

    # Tipo e identificación del ítem comprado
    tipo_item       = models.CharField(max_length=10, choices=TIPO_ITEM_CHOICES)
    codigo_item     = models.CharField(max_length=20)

    # Descripción fija al momento de la compra — no cambia aunque el producto cambie de nombre
    descripcion     = models.CharField(max_length=200)

    # Cantidades y valores
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
        # Lógica de actualización automática de stock al registrar un detalle (DA-003)
        # Todo se ejecuta dentro de una transacción atómica para garantizar integridad
        with transaction.atomic():
            if self.tipo_item == 'PRODUCTO':
                try:
                    # Si el producto existe — suma stock y actualiza precio_compra
                    producto = Producto.objects.get(codigo=self.codigo_item)
                    producto.stock += self.cantidad
                    producto.precio_compra = self.precio_unitario
                    producto.save()
                except Producto.DoesNotExist:
                    # Si el producto no existe — lo crea automáticamente
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
                    # Si el insumo existe — suma stock y actualiza precio_compra
                    insumo = Insumo.objects.get(codigo=self.codigo_item)
                    insumo.stock += self.cantidad
                    insumo.precio_compra = self.precio_unitario
                    insumo.save()
                except Insumo.DoesNotExist:
                    # Si el insumo no existe — lo crea automáticamente
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
            # Guarda el detalle después de actualizar el stock
            super().save(*args, **kwargs)