from django.contrib import admin
from apps.productos.models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):

    # Columnas visibles en el listado de productos
    list_display = ('codigo', 'nombre', 'categoria', 'genero', 'stock', 'nivel_stock', 'estado')

    # Filtros laterales
    list_filter = ('categoria', 'genero', 'estado')

    # Campos de búsqueda
    search_fields = ('codigo', 'nombre')

    # Orden por defecto
    ordering = ('codigo',)

    # Campos de solo lectura — no se modifican manualmente
    readonly_fields = ('fecha_creacion',)

    # Organización de campos en secciones al editar
    fieldsets = (
        ('Identificación', {'fields': ('codigo', 'nombre', 'categoria', 'genero', 'talla')}),
        ('Precios', {'fields': ('precio_compra', 'precio_venta')}),
        ('Inventario', {'fields': ('stock', 'stock_minimo', 'stock_maximo')}),
        ('Estado y metadatos', {'fields': ('estado', 'imagen', 'observaciones', 'fecha_creacion')}),
    )