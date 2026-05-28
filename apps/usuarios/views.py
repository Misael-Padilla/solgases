from io import BytesIO
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Q
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from apps.usuarios.models import Usuario, Cliente, Proveedor
from apps.usuarios.decoradores import login_requerido, admin_requerido


# =====================================================
# VISTAS DE USUARIOS (ADMIN / EMP)
# =====================================================

@login_requerido
def lista_usuarios(request):
    """Lista todos los usuarios del sistema — accesible para ADMIN y EMP."""
    q = request.GET.get('q', '').strip()
    usuarios = Usuario.objects.all().order_by('nombres')
    if q:
        usuarios = usuarios.filter(
            Q(identificacion__icontains=q) |
            Q(nombres__icontains=q) |
            Q(apellidos__icontains=q) |
            Q(correo_electronico__icontains=q)
        )
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios, 'q': q})


@login_requerido
def detalle_usuario(request, id):
    """Muestra el detalle de un usuario específico."""
    usuario = get_object_or_404(Usuario, id=id)
    return render(request, 'usuarios/detalle_usuario.html', {'usuario': usuario})


@admin_requerido
def crear_usuario(request):
    """Crea un nuevo usuario — solo ADMIN."""
    from apps.usuarios.forms import UsuarioForm
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.creado_por = request.user
            usuario.save()
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('usuarios:lista_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/form_usuario.html', {'form': form, 'titulo': 'Crear usuario'})


@admin_requerido
def editar_usuario(request, id):
    """Edita un usuario existente — solo ADMIN."""
    from apps.usuarios.forms import UsuarioEditarForm
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        form = UsuarioEditarForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            u = form.save(commit=False)
            u.modificado_por = request.user
            u.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('usuarios:detalle_usuario', id=usuario.id)
    else:
        form = UsuarioEditarForm(instance=usuario)
    return render(request, 'usuarios/form_usuario.html', {'form': form, 'titulo': 'Editar usuario'})


@admin_requerido
@require_POST
def cambiar_estado_usuario(request, id):
    """Activa o desactiva un usuario — solo ADMIN. Sin eliminación física."""
    usuario = get_object_or_404(Usuario, id=id)
    if usuario.estado == 'ACTIVO':
        usuario.estado = 'INACTIVO'
        messages.success(request, f'Usuario {usuario.nombres} desactivado.')
    else:
        usuario.estado = 'ACTIVO'
        messages.success(request, f'Usuario {usuario.nombres} activado.')
    usuario.save()
    return redirect('usuarios:lista_usuarios')


# =====================================================
# VISTAS DE CLIENTES
# =====================================================

@login_requerido
def lista_clientes(request):
    """Lista todos los clientes — accesible para ADMIN y EMP."""
    q = request.GET.get('q', '').strip()
    clientes = Cliente.objects.all().order_by('identificacion')
    if q:
        clientes = clientes.filter(
            Q(identificacion__icontains=q) |
            Q(nombres__icontains=q) |
            Q(apellidos__icontains=q) |
            Q(razon_social__icontains=q) |
            Q(ciudad__icontains=q) |
            Q(telefono__icontains=q)
        )
    return render(request, 'usuarios/lista_clientes.html', {'clientes': clientes, 'q': q})


@login_requerido
def detalle_cliente(request, id):
    """Muestra el detalle de un cliente específico."""
    cliente = get_object_or_404(Cliente, id=id)
    return render(request, 'usuarios/detalle_cliente.html', {'cliente': cliente})


@login_requerido
def crear_cliente(request):
    """Crea un nuevo cliente — accesible para ADMIN y EMP."""
    from apps.usuarios.forms import ClienteForm
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.creado_por = request.user
            cliente.save()
            messages.success(request, 'Cliente creado correctamente.')
            return redirect('usuarios:lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'usuarios/form_cliente.html', {'form': form, 'titulo': 'Crear cliente'})


@login_requerido
def editar_cliente(request, id):
    """Edita un cliente existente — accesible para ADMIN y EMP."""
    from apps.usuarios.forms import ClienteForm
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            c = form.save(commit=False)
            c.modificado_por = request.user
            c.save()
            messages.success(request, 'Cliente actualizado correctamente.')
            return redirect('usuarios:detalle_cliente', id=cliente.id)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'usuarios/form_cliente.html', {'form': form, 'titulo': 'Editar cliente'})


@admin_requerido
@require_POST
def cambiar_estado_cliente(request, id):
    """Activa o desactiva un cliente — solo ADMIN."""
    cliente = get_object_or_404(Cliente, id=id)
    if cliente.estado == 'ACTIVO':
        cliente.estado = 'INACTIVO'
        messages.success(request, f'Cliente desactivado.')
    else:
        cliente.estado = 'ACTIVO'
        messages.success(request, f'Cliente activado.')
    cliente.save()
    return redirect('usuarios:lista_clientes')


# =====================================================
# VISTAS DE PROVEEDORES
# =====================================================

@login_requerido
def lista_proveedores(request):
    """Lista todos los proveedores — accesible para ADMIN y EMP."""
    q = request.GET.get('q', '').strip()
    proveedores = Proveedor.objects.all().order_by('identificacion')
    if q:
        proveedores = proveedores.filter(
            Q(identificacion__icontains=q) |
            Q(nombres__icontains=q) |
            Q(apellidos__icontains=q) |
            Q(razon_social__icontains=q) |
            Q(ciudad__icontains=q) |
            Q(telefono__icontains=q)
        )
    return render(request, 'usuarios/lista_proveedores.html', {'proveedores': proveedores, 'q': q})


@login_requerido
def detalle_proveedor(request, id):
    """Muestra el detalle de un proveedor específico."""
    proveedor = get_object_or_404(Proveedor, id=id)
    return render(request, 'usuarios/detalle_proveedor.html', {'proveedor': proveedor})


@login_requerido
def crear_proveedor(request):
    """Crea un nuevo proveedor — accesible para ADMIN y EMP."""
    from apps.usuarios.forms import ProveedorForm
    if request.method == 'POST':
        form = ProveedorForm(request.POST, request.FILES)
        if form.is_valid():
            proveedor = form.save(commit=False)
            proveedor.creado_por = request.user
            proveedor.save()
            messages.success(request, 'Proveedor creado correctamente.')
            return redirect('usuarios:lista_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'usuarios/form_proveedor.html', {'form': form, 'titulo': 'Crear proveedor'})


@login_requerido
def editar_proveedor(request, id):
    """Edita un proveedor existente — accesible para ADMIN y EMP."""
    from apps.usuarios.forms import ProveedorForm
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, request.FILES, instance=proveedor)
        if form.is_valid():
            p = form.save(commit=False)
            p.modificado_por = request.user
            p.save()
            messages.success(request, 'Proveedor actualizado correctamente.')
            return redirect('usuarios:detalle_proveedor', id=proveedor.id)
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'usuarios/form_proveedor.html', {'form': form, 'titulo': 'Editar proveedor'})


@admin_requerido
@require_POST
def cambiar_estado_proveedor(request, id):
    """Activa o desactiva un proveedor — solo ADMIN."""
    proveedor = get_object_or_404(Proveedor, id=id)
    if proveedor.estado == 'ACTIVO':
        proveedor.estado = 'INACTIVO'
        messages.success(request, f'Proveedor desactivado.')
    else:
        proveedor.estado = 'ACTIVO'
        messages.success(request, f'Proveedor activado.')
    proveedor.save()
    return redirect('usuarios:lista_proveedores')


# =====================================================
# EXPORTACIÓN EXCEL — AUDITORÍA
# =====================================================

def _estilo_excel(wb):
    """Devuelve los estilos reutilizables para los reportes Excel."""
    color_cabecera = '1A1A1A'
    color_acento   = 'CC0000'
    borde = Border(
        left=Side(style='thin', color='CCCCCC'),
        right=Side(style='thin', color='CCCCCC'),
        top=Side(style='thin', color='CCCCCC'),
        bottom=Side(style='thin', color='CCCCCC'),
    )
    cabecera = openpyxl.styles.NamedStyle(name='cabecera')
    cabecera.font      = Font(bold=True, color='FFFFFF', size=11)
    cabecera.fill      = PatternFill('solid', fgColor=color_cabecera)
    cabecera.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    cabecera.border    = borde
    dato = openpyxl.styles.NamedStyle(name='dato')
    dato.font      = Font(size=10)
    dato.alignment = Alignment(vertical='center')
    dato.border    = borde
    return cabecera, dato, borde, color_acento


def _ajustar_columnas(ws):
    """Ajusta el ancho de cada columna al contenido más largo."""
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            try:
                if cell.value:
                    max_len = max(max_len, len(str(cell.value)))
            except Exception:
                pass
        ws.column_dimensions[col_letter].width = min(max_len + 4, 40)


def _nombre_usuario(usuario):
    if usuario:
        return f'{usuario.nombres} {usuario.apellidos}'
    return '—'


def _formato_fecha(dt):
    if dt:
        from zoneinfo import ZoneInfo
        from django.utils import timezone
        if timezone.is_aware(dt):
            dt = dt.astimezone(ZoneInfo('America/Bogota'))
        return dt.strftime('%d/%m/%Y %H:%M')
    return '—'


@login_requerido
def exportar_usuarios_excel(request):
    """Genera y descarga el reporte Excel de usuarios con auditoría."""
    usuarios = Usuario.objects.select_related('creado_por', 'modificado_por').order_by('nombres')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Usuarios'
    ws.freeze_panes = 'A2'

    cabecera, dato, borde, _ = _estilo_excel(wb)

    encabezados = [
        'Identificación', 'Nombre', 'Correo', 'Rol', 'Estado',
        'Creado por', 'Fecha creación', 'Modificado por', 'Última modificación'
    ]
    ws.append(encabezados)
    for cell in ws[1]:
        cell.style = cabecera

    tz_bogota = 'America/Bogota'
    for u in usuarios:
        ws.append([
            f'{u.tipo_identificacion} {u.identificacion}',
            f'{u.nombres} {u.apellidos}',
            u.correo_electronico,
            u.rol,
            u.estado,
            _nombre_usuario(u.creado_por),
            _formato_fecha(u.fecha_creacion),
            _nombre_usuario(u.modificado_por),
            _formato_fecha(u.modificado_en),
        ])

    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.border = borde
            cell.alignment = Alignment(vertical='center')

    _ajustar_columnas(ws)
    ws.row_dimensions[1].height = 30

    wb.properties.title   = 'Reporte de Usuarios — SOLGASES'
    wb.properties.creator = _nombre_usuario(request.user)

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    nombre_archivo = f'usuarios_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    return response


@login_requerido
def exportar_clientes_excel(request):
    """Genera y descarga el reporte Excel de clientes con auditoría."""
    clientes = Cliente.objects.select_related('creado_por', 'modificado_por').order_by('identificacion')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Clientes'
    ws.freeze_panes = 'A2'

    cabecera, dato, borde, _ = _estilo_excel(wb)

    encabezados = [
        'Identificación', 'Nombre / Razón social', 'Teléfono', 'Ciudad',
        'Estado', 'Creado por', 'Fecha creación', 'Modificado por', 'Última modificación'
    ]
    ws.append(encabezados)
    for cell in ws[1]:
        cell.style = cabecera

    for c in clientes:
        nombre = c.razon_social if c.tipo_identificacion == 'NIT' else f'{c.nombres} {c.apellidos}'
        ws.append([
            f'{c.tipo_identificacion} {c.identificacion}',
            nombre,
            c.telefono,
            c.ciudad,
            c.estado,
            _nombre_usuario(c.creado_por),
            _formato_fecha(c.fecha_creacion),
            _nombre_usuario(c.modificado_por),
            _formato_fecha(c.modificado_en),
        ])

    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.border = borde
            cell.alignment = Alignment(vertical='center')

    _ajustar_columnas(ws)
    ws.row_dimensions[1].height = 30

    wb.properties.title   = 'Reporte de Clientes — SOLGASES'
    wb.properties.creator = _nombre_usuario(request.user)

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    nombre_archivo = f'clientes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    return response


@login_requerido
def exportar_proveedores_excel(request):
    """Genera y descarga el reporte Excel de proveedores con auditoría."""
    proveedores = Proveedor.objects.select_related('creado_por', 'modificado_por').order_by('identificacion')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Proveedores'
    ws.freeze_panes = 'A2'

    cabecera, dato, borde, _ = _estilo_excel(wb)

    encabezados = [
        'Identificación', 'Nombre / Razón social', 'Teléfono', 'Ciudad',
        'Estado', 'Creado por', 'Fecha creación', 'Modificado por', 'Última modificación'
    ]
    ws.append(encabezados)
    for cell in ws[1]:
        cell.style = cabecera

    for p in proveedores:
        nombre = p.razon_social if p.tipo_identificacion == 'NIT' else f'{p.nombres} {p.apellidos}'
        ws.append([
            f'{p.tipo_identificacion} {p.identificacion}',
            nombre,
            p.telefono,
            p.ciudad,
            p.estado,
            _nombre_usuario(p.creado_por),
            _formato_fecha(p.fecha_creacion),
            _nombre_usuario(p.modificado_por),
            _formato_fecha(p.modificado_en),
        ])

    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.border = borde
            cell.alignment = Alignment(vertical='center')

    _ajustar_columnas(ws)
    ws.row_dimensions[1].height = 30

    wb.properties.title   = 'Reporte de Proveedores — SOLGASES'
    wb.properties.creator = _nombre_usuario(request.user)

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    nombre_archivo = f'proveedores_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    return response