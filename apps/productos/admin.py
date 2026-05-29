from django.contrib import admin
from apps.productos.models import Producto, HistorialStock


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):

    list_display  = ('codigo', 'nombre', 'categoria', 'genero', 'stock', 'nivel_stock', 'estado')
    list_filter   = ('categoria', 'genero', 'estado')
    search_fields = ('codigo', 'nombre')
    ordering      = ('codigo',)
    readonly_fields = ('fecha_creacion', 'creado_por', 'modificado_por', 'modificado_en')

    fieldsets = (
        ('Identificación', {'fields': ('codigo', 'nombre', 'categoria', 'genero', 'talla')}),
        ('Precios',        {'fields': ('precio_compra', 'precio_venta')}),
        ('Inventario',     {'fields': ('stock', 'stock_minimo', 'stock_maximo')}),
        ('Estado',         {'fields': ('estado', 'imagen', 'observaciones')}),
        ('Auditoría',      {'fields': ('fecha_creacion', 'creado_por', 'modificado_por', 'modificado_en')}),
    )


@admin.register(HistorialStock)
class HistorialStockAdmin(admin.ModelAdmin):

    list_display  = ('producto', 'tipo', 'stock_anterior', 'stock_nuevo', 'realizado_por', 'fecha')
    list_filter   = ('tipo',)
    search_fields = ('producto__codigo', 'producto__nombre', 'motivo')
    ordering      = ('-fecha',)
    readonly_fields = ('producto', 'tipo', 'stock_anterior', 'stock_nuevo', 'motivo', 'realizado_por', 'fecha')
