from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from apps.usuarios.models import Proveedor


class Insumo(models.Model):

    SUBCATEGORIA_CHOICES = [
        ('GAS',     'Gas'),
        ('QUIMICO', 'Químico'),
    ]
    UNIDAD_MEDIDA_CHOICES = [
        ('Litros',   'Litros'),
        ('Kilos',    'Kilos'),
        ('Unidades', 'Unidades'),
    ]
    ESTADO_CHOICES = [
        ('ACTIVO',   'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]

    # Identificación del insumo
    codigo        = models.CharField(max_length=20, unique=True)
    nombre        = models.CharField(max_length=200)
    subcategoria  = models.CharField(max_length=10, choices=SUBCATEGORIA_CHOICES)
    unidad_medida = models.CharField(max_length=15, choices=UNIDAD_MEDIDA_CHOICES)

    # Precio — se usa Decimal para valores monetarios, nunca float
    precio_compra = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    # Control de inventario con dos umbrales (DA-002)
    stock        = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    stock_minimo = models.IntegerField(validators=[MinValueValidator(0)])
    stock_maximo = models.IntegerField(validators=[MinValueValidator(1)])

    # Proveedor principal — a quién llamar cuando el stock esté bajo
    proveedor     = models.ForeignKey(
        Proveedor, on_delete=models.PROTECT, related_name='insumos'
    )

    # Estado y metadatos
    estado        = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='ACTIVO')
    imagen        = models.ImageField(upload_to='insumos/', null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # Auditoría — quién creó y quién modificó por última vez
    creado_por    = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='insumos_creados'
    )
    modificado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='insumos_modificados'
    )
    modificado_en  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'insumo'
        verbose_name = 'Insumo'
        verbose_name_plural = 'Insumos'

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


class HistorialStockInsumo(models.Model):

    TIPO_CHOICES = [
        ('MANUAL', 'Ajuste manual'),
        ('COMPRA', 'Entrada por compra'),
    ]

    insumo         = models.ForeignKey(
        'Insumo', on_delete=models.CASCADE, related_name='historial_stock'
    )
    tipo           = models.CharField(max_length=10, choices=TIPO_CHOICES, default='MANUAL')
    stock_anterior = models.IntegerField()
    stock_nuevo    = models.IntegerField()
    motivo         = models.CharField(max_length=200)
    realizado_por  = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='historial_stock_insumo_realizado'
    )
    fecha          = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table            = 'historial_stock_insumo'
        ordering            = ['-fecha']
        verbose_name        = 'Historial de stock de insumo'
        verbose_name_plural = 'Historial de stock de insumos'

    def __str__(self):
        return f'{self.insumo.codigo} — {self.stock_anterior} → {self.stock_nuevo} ({self.fecha:%d/%m/%Y})'
