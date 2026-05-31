import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)


class BackupConfig(AppConfig):
    name = 'apps.backup'

    def ready(self):
        import os
        from django.conf import settings

        # Desarrollo (runserver crea 2 procesos):
        #   proceso padre (watcher): RUN_MAIN no existe → no iniciar
        #   proceso hijo (reloader): RUN_MAIN='true'   → iniciar
        # Producción (DEBUG=False, RUN_MAIN no existe) → iniciar siempre
        if settings.DEBUG and os.environ.get('RUN_MAIN') != 'true':
            return

        try:
            from apscheduler.schedulers.background import BackgroundScheduler
            from apscheduler.triggers.cron import CronTrigger
            from django_apscheduler.jobstores import DjangoJobStore
            from apps.backup.scheduler import backup_automatico

            scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
            scheduler.add_jobstore(DjangoJobStore(), 'default')

            scheduler.add_job(
                backup_automatico,
                trigger=CronTrigger(hour=2, minute=0),
                id='backup_automatico_diario',
                name='Backup automático diario — 02:00 AM',
                replace_existing=True,
                misfire_grace_time=3600,  # 1 hora de tolerancia si el servidor estaba apagado
            )

            scheduler.start()
            logger.info('APScheduler iniciado — backup automático programado a las 02:00 AM.')

        except Exception as e:
            logger.error('No se pudo iniciar APScheduler: %s', str(e), exc_info=True)
