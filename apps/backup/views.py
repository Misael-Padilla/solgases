import os
import sys
import logging
import subprocess
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.decorators.http import require_POST
from apps.backup.models import Backup
from apps.usuarios.models import HistorialCambio
from apps.usuarios.decoradores import admin_requerido

logger = logging.getLogger(__name__)

_POR_PAGINA = 15


@admin_requerido
def lista_backups(request):
    """Lista todos los backups generados — solo ADMIN."""
    backups_qs  = Backup.objects.all()
    paginator   = Paginator(backups_qs, _POR_PAGINA)
    page_obj    = paginator.get_page(request.GET.get('page', 1))
    breadcrumbs = [
        {'nombre': 'Dashboard',           'url': reverse('core:inicio')},
        {'nombre': 'Copias de seguridad', 'url': None},
    ]
    return render(request, 'backup/lista_backups.html', {
        'backups':            page_obj,
        'page_obj':           page_obj,
        'page_range':         list(paginator.get_elided_page_range(page_obj.number, on_each_side=2, on_ends=1)),
        'paginator_ellipsis': paginator.ELLIPSIS,
        'breadcrumbs':        breadcrumbs,
    })


@admin_requerido
@require_POST
def generar_backup(request):
    """
    Genera un backup manual de la base de datos completa.
    Usa dumpdata de Django para exportar todos los datos en formato JSON.
    Registra el backup en la tabla backup con nombre, peso y ruta relativa (DA-005).
    """
    try:
        carpeta_backup = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(carpeta_backup, exist_ok=True)

        nombre_archivo = f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        ruta_relativa  = os.path.join('backups', nombre_archivo)
        ruta_absoluta  = os.path.join(settings.BASE_DIR, ruta_relativa)

        resultado = subprocess.run(
            [sys.executable, 'manage.py', 'dumpdata', '--indent', '2'],
            capture_output=True,
            text=True,
            cwd=settings.BASE_DIR,
        )

        if resultado.returncode != 0:
            raise Exception(resultado.stderr)

        with open(ruta_absoluta, 'w', encoding='utf-8') as archivo:
            archivo.write(resultado.stdout)

        peso_bytes = os.path.getsize(ruta_absoluta)
        if peso_bytes < 1024:
            peso = f'{peso_bytes} B'
        elif peso_bytes < 1024 * 1024:
            peso = f'{peso_bytes / 1024:.1f} KB'
        else:
            peso = f'{peso_bytes / (1024 * 1024):.1f} MB'

        Backup.objects.create(
            nombre_archivo = nombre_archivo,
            tipo           = 'MANUAL',
            peso_archivo   = peso,
            ruta_archivo   = ruta_relativa,
            generado_por   = request.user,
        )

        messages.success(request, f'Backup generado correctamente: {nombre_archivo}')

    except Exception as e:
        logger.error('Error al generar backup: %s', str(e), exc_info=True)
        messages.error(request, 'Error al generar el backup. Revise los logs del servidor.')

    return redirect('backup:lista_backups')


@admin_requerido
def restaurar_backup(request, id):
    """
    Restaura la base de datos desde un archivo de backup.
    Proceso: vacía las tablas y carga el JSON con loaddata.
    Solo accesible para ADMIN — operación crítica (DA-005).
    """
    backup = get_object_or_404(Backup, id=id)

    if request.method == 'POST':
        try:
            # Soporta rutas relativas (nuevas) y absolutas (registros heredados)
            if os.path.isabs(backup.ruta_archivo):
                ruta_absoluta = backup.ruta_archivo
            else:
                ruta_absoluta = os.path.join(settings.BASE_DIR, backup.ruta_archivo)

            if not os.path.exists(ruta_absoluta):
                raise Exception('El archivo de backup no existe en el servidor.')

            resultado = subprocess.run(
                [sys.executable, 'manage.py', 'loaddata', ruta_absoluta],
                capture_output=True,
                text=True,
                cwd=settings.BASE_DIR,
            )

            if resultado.returncode != 0:
                raise Exception(resultado.stderr)

            HistorialCambio.objects.create(
                modelo        = 'BACKUP',
                objeto_id     = backup.id,
                objeto_nombre = backup.nombre_archivo,
                accion        = 'RESTAURAR',
                observacion   = (
                    f'Base de datos restaurada desde {backup.nombre_archivo} '
                    f'(tipo: {backup.get_tipo_display()}, '
                    f'generado: {backup.fecha_creacion.strftime("%d/%m/%Y %H:%M")})'
                ),
                realizado_por = request.user,
            )

            messages.success(request, f'Base de datos restaurada correctamente desde {backup.nombre_archivo}.')

        except Exception as e:
            logger.error('Error al restaurar backup %s: %s', backup.nombre_archivo, str(e), exc_info=True)
            messages.error(request, 'Error al restaurar el backup. Revise los logs del servidor.')

        return redirect('backup:lista_backups')

    breadcrumbs = [
        {'nombre': 'Dashboard',           'url': reverse('core:inicio')},
        {'nombre': 'Copias de seguridad', 'url': reverse('backup:lista_backups')},
        {'nombre': 'Restaurar backup',    'url': None},
    ]
    return render(request, 'backup/confirmar_restauracion.html', {
        'backup':      backup,
        'breadcrumbs': breadcrumbs,
    })
