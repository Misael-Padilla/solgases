from django.contrib import admin
from apps.insumos.models import Insumo, HistorialStockInsumo


@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):

    list_display  = ('codigo', 'nombre', 'subcategoria', 'unidad_medida', 'stock', 'nivel_stock', 'proveedor', 'estado')
    list_filter   = ('subcategoria', 'unidad_medida', 'estado')
    search_fields = ('codigo', 'nombre')
    ordering      = ('codigo',)
    readonly_fields = ('fecha_creacion', 'creado_por', 'modificado_por', 'modificado_en')

    fieldsets = (
        ('Identificación', {'fields': ('codigo', 'nombre', 'subcategoria', 'unidad_medida')}),
        ('Precio',         {'fields': ('precio_compra',)}),
        ('Inventario',     {'fields': ('stock', 'stock_minimo', 'stock_maximo')}),
        ('Proveedor',      {'fields': ('proveedor',)}),
        ('Estado',         {'fields': ('estado', 'imagen', 'observaciones')}),
        ('Auditoría',      {'fields': ('fecha_creacion', 'creado_por', 'modificado_por', 'modificado_en')}),
    )


@admin.register(HistorialStockInsumo)
class HistorialStockInsumoAdmin(admin.ModelAdmin):

    list_display  = ('insumo', 'tipo', 'stock_anterior', 'stock_nuevo', 'realizado_por', 'fecha')
    list_filter   = ('tipo',)
    search_fields = ('insumo__codigo', 'insumo__nombre', 'motivo')
    ordering      = ('-fecha',)
    readonly_fields = ('insumo', 'tipo', 'stock_anterior', 'stock_nuevo', 'motivo', 'realizado_por', 'fecha')
