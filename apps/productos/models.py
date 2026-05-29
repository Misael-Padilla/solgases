from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Producto(models.Model):

    # Opciones para el campo categoria
    CATEGORIA_CHOICES = [
        ('DOTACION', 'Dotación'),
        ('EPP', 'EPP'),
    ]

    # Opciones para el campo genero
    GENERO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
        ('Unisex', 'Unisex'),
    ]

    # Opciones para el campo estado
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]

    # Identificación del producto
    codigo    = models.CharField(max_length=20, unique=True)
    nombre    = models.CharField(max_length=200)
    categoria = models.CharField(max_length=15, choices=CATEGORIA_CHOICES)
    genero    = models.CharField(max_length=10, choices=GENERO_CHOICES)
    talla     = models.CharField(max_length=200, null=True, blank=True)

    # Precios — se usa Decimal para valores monetarios, nunca float
    precio_compra = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    precio_venta  = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    # Control de inventario con dos umbrales (DA-002)
    stock        = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    stock_minimo = models.IntegerField(validators=[MinValueValidator(0)])
    stock_maximo = models.IntegerField(validators=[MinValueValidator(1)])

    # Estado y metadatos
    estado       = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='ACTIVO')
    imagen       = models.ImageField(upload_to='productos/', null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # Auditoría — quién creó y quién modificó por última vez
    creado_por    = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='productos_creados'
    )
    modificado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='productos_modificados'
    )
    modificado_en  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return f'{self.codigo} — {self.nombre}'

    # Propiedad calculada para el nivel de stock (DA-002)
    # No se almacena en BD — se calcula en tiempo de ejecución
    @property
    def nivel_stock(self):
        if self.stock <= self.stock_minimo:
            return 'BAJO'
        elif self.stock >= self.stock_maximo:
            return 'ALTO'
        return 'NORMAL'


class HistorialStock(models.Model):

    TIPO_CHOICES = [
        ('MANUAL', 'Ajuste manual'),
        ('COMPRA', 'Entrada por compra'),
        ('VENTA',  'Salida por venta'),
    ]

    producto       = models.ForeignKey(
        'Producto', on_delete=models.CASCADE, related_name='historial_stock'
    )
    tipo           = models.CharField(max_length=10, choices=TIPO_CHOICES, default='MANUAL')
    stock_anterior = models.IntegerField()
    stock_nuevo    = models.IntegerField()
    motivo         = models.CharField(max_length=200)
    realizado_por  = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='historial_stock_realizado'
    )
    fecha          = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table            = 'historial_stock'
        ordering            = ['-fecha']
        verbose_name        = 'Historial de stock'
        verbose_name_plural = 'Historial de stock'

    def __str__(self):
        return f'{self.producto.codigo} — {self.stock_anterior} → {self.stock_nuevo} ({self.fecha:%d/%m/%Y})'
