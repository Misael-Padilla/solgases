from django.db import models
from apps.usuarios.models import Proveedor


class Insumo(models.Model):

    # Opciones para el campo subcategoria
    SUBCATEGORIA_CHOICES = [
        ('GAS', 'Gas'),
        ('QUIMICO', 'Químico'),
    ]

    # Opciones para el campo unidad_medida
    UNIDAD_MEDIDA_CHOICES = [
        ('Litros', 'Litros'),
        ('Kilos', 'Kilos'),
        ('Unidades', 'Unidades'),
    ]

    # Opciones para el campo estado
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]

    # Identificación del insumo
    codigo          = models.CharField(max_length=20, unique=True)
    nombre          = models.CharField(max_length=200)
    subcategoria    = models.CharField(max_length=10, choices=SUBCATEGORIA_CHOICES)
    unidad_medida   = models.CharField(max_length=15, choices=UNIDAD_MEDIDA_CHOICES)

    # Precio — se usa Decimal para valores monetarios, nunca float
    precio_compra   = models.DecimalField(max_digits=12, decimal_places=2)

    # Control de inventario con dos umbrales (DA-002)
    stock           = models.IntegerField(default=0)
    stock_minimo    = models.IntegerField()
    stock_maximo    = models.IntegerField()

    # Proveedor principal — a quién llamar cuando el stock esté bajo
    proveedor       = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='insumos')

    # Estado y metadatos
    estado          = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='ACTIVO')
    imagen          = models.ImageField(upload_to='insumos/', null=True, blank=True)
    observaciones   = models.TextField(null=True, blank=True)
    fecha_creacion  = models.DateTimeField(auto_now_add=True)

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