from django.contrib import admin
from apps.compras.models import FacturaCompra, DetalleCompra


class DetalleCompraInline(admin.TabularInline):
    # Permite registrar los detalles directamente desde la factura
    model = DetalleCompra
    extra = 1
    readonly_fields = ('subtotal',)


@admin.register(FacturaCompra)
class FacturaCompraAdmin(admin.ModelAdmin):

    # Detalle inline — los ítems se registran dentro de la factura
    inlines = [DetalleCompraInline]

    # Columnas visibles en el listado de facturas
    list_display = ('numero_factura', 'proveedor', 'registrado_por', 'fecha_factura', 'total', 'estado')

    # Filtros laterales
    list_filter = ('estado', 'proveedor')

    # Campos de búsqueda
    search_fields = ('numero_factura',)

    # Orden por defecto — más recientes primero
    ordering = ('-fecha_registro',)

    # Campos de solo lectura
    readonly_fields = ('fecha_registro',)

    # Organización de campos en secciones al editar
    fieldsets = (
        ('Identificación', {'fields': ('numero_factura', 'proveedor', 'registrado_por')}),
        ('Fechas', {'fields': ('fecha_factura', 'fecha_registro')}),
        ('Valores', {'fields': ('subtotal', 'iva', 'total')}),
        ('Estado y metadatos', {'fields': ('estado', 'observaciones')}),
    )