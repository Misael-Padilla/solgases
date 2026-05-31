import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)


class BackupConfig(AppConfig):
    name = 'apps.backup'

    def ready(self):
        import os
        from django.conf import settings

        # Desarrollo: solo el proceso hijo (RUN_MAIN='true')
        # Producción (DEBUG=False): siempre iniciar
        if settings.DEBUG and os.environ.get('RUN_MAIN') != 'true':
            return

        try:
            from apscheduler.schedulers.background import BackgroundScheduler
            from apscheduler.triggers.cron import CronTrigger
            from django_apscheduler.jobstores import DjangoJobStore
            from apps.backup.models import ConfigBackup
            from apps.backup.scheduler import backup_automatico, set_scheduler

            config, _ = ConfigBackup.objects.get_or_create(
                pk=1,
                defaults={'hora_diaria': 2, 'minuto_diario': 0, 'activo': True}
            )

            scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
            scheduler.add_jobstore(DjangoJobStore(), 'default')

            if config.activo:
                scheduler.add_job(
                    backup_automatico,
                    trigger=CronTrigger(hour=config.hora_diaria, minute=config.minuto_diario),
                    id='backup_automatico_diario',
                    name=f'Backup automático — {config.hora_diaria:02d}:{config.minuto_diario:02d}',
                    replace_existing=True,
                    misfire_grace_time=3600,
                )

            scheduler.start()
            set_scheduler(scheduler)
            logger.info(
                'APScheduler iniciado — backup diario a las %02d:%02d.',
                config.hora_diaria, config.minuto_diario
            )

        except Exception as e:
            logger.error('No se pudo iniciar APScheduler: %s', str(e), exc_info=True)
