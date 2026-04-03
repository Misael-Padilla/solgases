from django.contrib import admin
from apps.ventas.models import FacturaVenta, DetalleVenta


class DetalleVentaInline(admin.TabularInline):
    # Permite registrar los detalles directamente desde la factura
    model = DetalleVenta
    extra = 1
    readonly_fields = ('subtotal',)


@admin.register(FacturaVenta)
class FacturaVentaAdmin(admin.ModelAdmin):

    # Detalle inline — los ítems se registran dentro de la factura
    inlines = [DetalleVentaInline]

    # Columnas visibles en el listado de facturas
    list_display = ('numero_factura', 'cliente', 'registrado_por', 'fecha_factura', 'metodo_pago', 'total', 'estado')

    # Filtros laterales
    list_filter = ('estado', 'metodo_pago')

    # Campos de búsqueda
    search_fields = ('numero_factura',)

    # Orden por defecto — más recientes primero
    ordering = ('-fecha_registro',)

    # Campos de solo lectura
    readonly_fields = ('fecha_registro',)

    # Organización de campos en secciones al editar
    fieldsets = (
        ('Identificación', {'fields': ('numero_factura', 'cliente', 'registrado_por', 'recibido_por')}),
        ('Fechas', {'fields': ('fecha_factura', 'fecha_registro')}),
        ('Pago', {'fields': ('metodo_pago',)}),
        ('Valores', {'fields': ('subtotal', 'iva', 'total')}),
        ('Estado y metadatos', {'fields': ('estado', 'observaciones')}),
    )