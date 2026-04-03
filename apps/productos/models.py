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
    codigo          = models.CharField(max_length=20, unique=True)
    nombre          = models.CharField(max_length=200)
    categoria       = models.CharField(max_length=15, choices=CATEGORIA_CHOICES)
    genero          = models.CharField(max_length=10, choices=GENERO_CHOICES)
    talla           = models.CharField(max_length=200, null=True, blank=True)

    # Precios — se usa Decimal para valores monetarios, nunca float
    precio_compra   = models.DecimalField(max_digits=12, decimal_places=2)
    precio_venta    = models.DecimalField(max_digits=12, decimal_places=2)

    # Control de inventario con dos umbrales (DA-002)
    stock           = models.IntegerField(default=0)
    stock_minimo    = models.IntegerField()
    stock_maximo    = models.IntegerField()

    # Estado y metadatos
    estado          = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='ACTIVO')
    imagen          = models.ImageField(upload_to='productos/', null=True, blank=True)
    observaciones   = models.TextField(null=True, blank=True)
    fecha_creacion  = models.DateTimeField(auto_now_add=True)

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