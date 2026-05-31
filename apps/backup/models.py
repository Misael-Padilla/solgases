from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
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


class ConfigBackup(models.Model):
    """
    Configuración del backup automático — registro único (singleton, pk=1).
    El scheduler lee esta config al iniciar y la vista la actualiza en tiempo real.
    """
    hora_diaria   = models.PositiveSmallIntegerField(
        default=2,
        validators=[MinValueValidator(0), MaxValueValidator(23)],
        verbose_name='Hora (0-23)'
    )
    minuto_diario = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(59)],
        verbose_name='Minuto'
    )
    activo        = models.BooleanField(default=True, verbose_name='Backup automático activo')
    modificado_por = models.ForeignKey(
        Usuario,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    modificado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'config_backup'
        verbose_name        = 'Configuración de backup'
        verbose_name_plural = 'Configuración de backup'

    def __str__(self):
        return f'Backup diario {self.hora_diaria:02d}:{self.minuto_diario:02d}'