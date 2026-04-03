from django.contrib import admin
from apps.backup.models import Backup


@admin.register(Backup)
class BackupAdmin(admin.ModelAdmin):

    # Columnas visibles en el listado de backups
    list_display = ('nombre_archivo', 'tipo', 'peso_archivo', 'generado_por', 'fecha_creacion')

    # Filtros laterales
    list_filter = ('tipo',)

    # Campos de búsqueda
    search_fields = ('nombre_archivo',)

    # Campos de solo lectura — el historial no se modifica manualmente
    readonly_fields = ('nombre_archivo', 'tipo', 'peso_archivo', 'ruta_archivo', 'generado_por', 'fecha_creacion')

    # Organización de campos en secciones al editar
    fieldsets = (
        ('Archivo', {'fields': ('nombre_archivo', 'tipo', 'peso_archivo', 'ruta_archivo')}),
        ('Generado por', {'fields': ('generado_por',)}),
        ('Metadatos', {'fields': ('observaciones', 'fecha_creacion')}),
    )