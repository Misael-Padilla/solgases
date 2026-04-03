from django.db import models
from apps.usuarios.models import Usuario


class Backup(models.Model):

    # Opciones para el campo tipo
    TIPO_CHOICES = [
        ('AUTOMATICO', 'Automático'),
        ('MANUAL', 'Manual'),
    ]

    # Identificación del archivo de backup
    nombre_archivo  = models.CharField(max_length=200, unique=True)
    tipo            = models.CharField(max_length=15, choices=TIPO_CHOICES)
    peso_archivo    = models.CharField(max_length=20)
    ruta_archivo    = models.CharField(max_length=300)

    # Usuario que generó el backup — null si fue automático (DA-005)
    generado_por    = models.ForeignKey(
                        Usuario,
                        on_delete=models.SET_NULL,
                        null=True,
                        blank=True,
                        related_name='backups_generados'
                    )

    # Metadatos
    observaciones   = models.TextField(null=True, blank=True)
    fecha_creacion  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'backup'
        verbose_name = 'Backup'
        verbose_name_plural = 'Backups'
        # Orden por defecto — más recientes primero
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'{self.tipo} — {self.nombre_archivo} ({self.fecha_creacion})'