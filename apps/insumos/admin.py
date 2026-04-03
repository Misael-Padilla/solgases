from django.contrib import admin
from apps.insumos.models import Insumo


@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):

    # Columnas visibles en el listado de insumos
    list_display = ('codigo', 'nombre', 'subcategoria', 'unidad_medida', 'stock', 'nivel_stock', 'proveedor', 'estado')

    # Filtros laterales
    list_filter = ('subcategoria', 'unidad_medida', 'estado')

    # Campos de búsqueda
    search_fields = ('codigo', 'nombre')

    # Orden por defecto
    ordering = ('codigo',)

    # Campos de solo lectura — no se modifican manualmente
    readonly_fields = ('fecha_creacion',)

    # Organización de campos en secciones al editar
    fieldsets = (
        ('Identificación', {'fields': ('codigo', 'nombre', 'subcategoria', 'unidad_medida')}),
        ('Precio', {'fields': ('precio_compra',)}),
        ('Inventario', {'fields': ('stock', 'stock_minimo', 'stock_maximo')}),
        ('Proveedor', {'fields': ('proveedor',)}),
        ('Estado y metadatos', {'fields': ('estado', 'imagen', 'observaciones', 'fecha_creacion')}),
    )