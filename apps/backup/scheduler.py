import os
import io
import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.core.management import call_command
from django.utils import timezone

logger = logging.getLogger(__name__)

RETENTION_DAYS = getattr(settings, 'BACKUP_RETENTION_DAYS', 30)


def backup_automatico():
    """
    Genera un backup automático de la BD y aplica la política de retención.
    Registra el resultado en la tabla Backup con tipo='AUTOMATICO'.
    Se ejecuta diariamente a las 02:00 AM.
    """
    from apps.backup.models import Backup

    try:
        carpeta_backup = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(carpeta_backup, exist_ok=True)

        nombre_archivo = f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        ruta_relativa  = os.path.join('backups', nombre_archivo)
        ruta_absoluta  = os.path.join(settings.BASE_DIR, ruta_relativa)

        output = io.StringIO()
        call_command('dumpdata', indent=2, stdout=output, verbosity=0)
        datos = output.getvalue()

        if not datos.strip():
            raise Exception('dumpdata devolvió un resultado vacío.')

        with open(ruta_absoluta, 'w', encoding='utf-8') as archivo:
            archivo.write(datos)

        peso_bytes = os.path.getsize(ruta_absoluta)
        if peso_bytes < 1024:
            peso = f'{peso_bytes} B'
        elif peso_bytes < 1024 * 1024:
            peso = f'{peso_bytes / 1024:.1f} KB'
        else:
            peso = f'{peso_bytes / (1024 * 1024):.1f} MB'

        Backup.objects.create(
            nombre_archivo = nombre_archivo,
            tipo           = 'AUTOMATICO',
            peso_archivo   = peso,
            ruta_archivo   = ruta_relativa,
            generado_por   = None,
        )

        logger.info('Backup automático generado: %s (%s)', nombre_archivo, peso)
        _aplicar_retencion()

    except Exception as e:
        logger.error('Error en backup automático: %s', str(e), exc_info=True)


def _aplicar_retencion():
    """Elimina backups automáticos con más de RETENTION_DAYS días."""
    from apps.backup.models import Backup

    fecha_limite = timezone.now() - timedelta(days=RETENTION_DAYS)
    antiguos     = list(Backup.objects.filter(tipo='AUTOMATICO', fecha_creacion__lt=fecha_limite))

    eliminados = 0
    for backup in antiguos:
        ruta = (
            backup.ruta_archivo
            if os.path.isabs(backup.ruta_archivo)
            else os.path.join(settings.BASE_DIR, backup.ruta_archivo)
        )
        try:
            if os.path.exists(ruta):
                os.remove(ruta)
            backup.delete()
            eliminados += 1
        except Exception as e:
            logger.warning('No se pudo eliminar backup antiguo %s: %s', backup.nombre_archivo, str(e))

    if eliminados:
        logger.info('Retención aplicada: %d backup(s) automático(s) eliminado(s)', eliminados)
