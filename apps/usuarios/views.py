from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from apps.usuarios.models import Usuario, Cliente, Proveedor
from apps.usuarios.decoradores import login_requerido, admin_requerido


# =====================================================
# VISTAS DE USUARIOS (ADMIN / EMP)
# =====================================================

@login_requerido
def lista_usuarios(request):
    """Lista todos los usuarios del sistema — accesible para ADMIN y EMP."""
    usuarios = Usuario.objects.all().order_by('nombres')
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})


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
            form.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('usuarios:detalle_usuario', id=usuario.id)
    else:
        form = UsuarioEditarForm(instance=usuario)
    return render(request, 'usuarios/form_usuario.html', {'form': form, 'titulo': 'Editar usuario'})


@admin_requerido
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
    clientes = Cliente.objects.all().order_by('identificacion')
    return render(request, 'usuarios/lista_clientes.html', {'clientes': clientes})


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
            form.save()
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
            form.save()
            messages.success(request, 'Cliente actualizado correctamente.')
            return redirect('usuarios:detalle_cliente', id=cliente.id)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'usuarios/form_cliente.html', {'form': form, 'titulo': 'Editar cliente'})


@admin_requerido
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
    proveedores = Proveedor.objects.all().order_by('identificacion')
    return render(request, 'usuarios/lista_proveedores.html', {'proveedores': proveedores})


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
            form.save()
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
            form.save()
            messages.success(request, 'Proveedor actualizado correctamente.')
            return redirect('usuarios:detalle_proveedor', id=proveedor.id)
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'usuarios/form_proveedor.html', {'form': form, 'titulo': 'Editar proveedor'})


@admin_requerido
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