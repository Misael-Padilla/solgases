import os 
import json
import sys
import subprocess
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from apps.backup.models import Backup
from apps.usuarios.decoradores import admin_requerido



@admin_requerido
def lista_backups(request):
    """Lista todos los backups generados — solo ADMIN."""
    backups = Backup.objects.all().order_by('-fecha_creacion')
    return render(request, 'backup/lista_backups.html', {'backups': backups})


@admin_requerido
def generar_backup(request):
    """
    Genera un backup manual de la base de datos completa.
    Usa dumpdata de Django para exportar todos los datos en formato JSON.
    Registra el backup en la tabla backup con nombre, peso, ruta y usuario (DA-005).
    """
    if request.method == 'POST':
        try:
            # Carpeta donde se guardan los backups
            carpeta_backup = os.path.join(settings.BASE_DIR, 'backups')
            os.makedirs(carpeta_backup, exist_ok=True)

            # Nombre del archivo con fecha y hora
            nombre_archivo = f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            ruta_archivo   = os.path.join(carpeta_backup, nombre_archivo)

            # Ejecuta dumpdata de Django para exportar todos los datos
            resultado = subprocess.run(
                [sys.executable, 'manage.py', 'dumpdata', '--indent', '2'],
                capture_output=True,
                text=True,
                cwd=settings.BASE_DIR,
            )

            if resultado.returncode != 0:
                raise Exception(resultado.stderr)

            # Guarda el archivo JSON en disco
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(resultado.stdout)

            # Calcula el peso del archivo
            peso_bytes = os.path.getsize(ruta_archivo)
            if peso_bytes < 1024:
                peso = f'{peso_bytes} B'
            elif peso_bytes < 1024 * 1024:
                peso = f'{peso_bytes / 1024:.1f} KB'
            else:
                peso = f'{peso_bytes / (1024 * 1024):.1f} MB'

            # Registra el backup en la base de datos
            Backup.objects.create(
                nombre_archivo = nombre_archivo,
                tipo           = 'MANUAL',
                peso_archivo   = peso,
                ruta_archivo   = ruta_archivo,
                generado_por   = request.user,
            )

            messages.success(request, f'Backup generado correctamente: {nombre_archivo}')

        except Exception as e:
            messages.error(request, f'Error al generar el backup: {str(e)}')

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
            # Verifica que el archivo existe en disco
            if not os.path.exists(backup.ruta_archivo):
                raise Exception('El archivo de backup no existe en el servidor.')

            # Ejecuta loaddata con el Python del entorno virtual
            resultado = subprocess.run(
                [sys.executable, 'manage.py', 'loaddata', backup.ruta_archivo],
                capture_output=True,
                text=True,
                cwd=settings.BASE_DIR,
            )

            if resultado.returncode != 0:
                raise Exception(resultado.stderr)

            messages.success(request, f'Base de datos restaurada correctamente desde {backup.nombre_archivo}.')

        except Exception as e:
            messages.error(request, f'Error al restaurar el backup: {str(e)}')

        return redirect('backup:lista_backups')

    # GET — muestra pantalla de confirmación antes de restaurar
    return render(request, 'backup/confirmar_restauracion.html', {'backup': backup})