from django import forms
from apps.usuarios.models import Usuario, Cliente, Proveedor


# =====================================================
# FORMULARIOS DE USUARIO
# =====================================================

class UsuarioForm(forms.ModelForm):
    """
    Formulario para crear un nuevo usuario.
    Incluye campo de contraseña que se encripta antes de guardar.
    """

    # Campo de contraseña — no viene del modelo, se maneja manualmente
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}),
        min_length=8,
    )

    confirmar_password = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}),
    )

    class Meta:
        model = Usuario
        fields = [
            'tipo_identificacion', 'identificacion', 'nombres', 'apellidos',
            'correo_electronico', 'telefono', 'direccion', 'ciudad',
            'departamento', 'rol', 'estado', 'imagen', 'observaciones',
        ]

    def clean(self):
        """Validación cruzada — verifica que las contraseñas coincidan."""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmar = cleaned_data.get('confirmar_password')

        if password and confirmar and password != confirmar:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cleaned_data


class UsuarioEditarForm(forms.ModelForm):
    """
    Formulario para editar un usuario existente.
    No incluye campo de contraseña — se cambia por separado.
    """

    class Meta:
        model = Usuario
        fields = [
            'tipo_identificacion', 'identificacion', 'nombres', 'apellidos',
            'correo_electronico', 'telefono', 'direccion', 'ciudad',
            'departamento', 'rol', 'estado', 'imagen', 'observaciones',
        ]


# =====================================================
# FORMULARIO DE CLIENTE
# =====================================================

class ClienteForm(forms.ModelForm):
    """
    Formulario para crear y editar clientes.
    Incluye validación condicional según tipo de identificación:
    - CC / CE / PS → nombres y apellidos obligatorios.
    - NIT → razon_social, nombre_comercial y representante_legal obligatorios.
    """

    class Meta:
        model = Cliente
        fields = [
            'tipo_identificacion', 'identificacion', 'nombres', 'apellidos',
            'razon_social', 'nombre_comercial', 'representante_legal',
            'correo_electronico', 'telefono', 'direccion', 'ciudad',
            'departamento', 'estado', 'imagen', 'observaciones',
        ]

    def clean(self):
        """Validación condicional según tipo de identificación (DA-001)."""
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo_identificacion')

        if tipo in ['CC', 'CE', 'PS']:
            # Persona natural — nombres y apellidos obligatorios
            if not cleaned_data.get('nombres'):
                self.add_error('nombres', 'Este campo es obligatorio para CC, CE o PS.')
            if not cleaned_data.get('apellidos'):
                self.add_error('apellidos', 'Este campo es obligatorio para CC, CE o PS.')

        elif tipo == 'NIT':
            # Empresa — razón social, nombre comercial y representante obligatorios
            if not cleaned_data.get('razon_social'):
                self.add_error('razon_social', 'Este campo es obligatorio para NIT.')
            if not cleaned_data.get('nombre_comercial'):
                self.add_error('nombre_comercial', 'Este campo es obligatorio para NIT.')
            if not cleaned_data.get('representante_legal'):
                self.add_error('representante_legal', 'Este campo es obligatorio para NIT.')

        return cleaned_data


# =====================================================
# FORMULARIO DE PROVEEDOR
# =====================================================

class ProveedorForm(forms.ModelForm):
    """
    Formulario para crear y editar proveedores.
    Misma lógica condicional que ClienteForm.
    """

    class Meta:
        model = Proveedor
        fields = [
            'tipo_identificacion', 'identificacion', 'nombres', 'apellidos',
            'razon_social', 'nombre_comercial', 'representante_legal',
            'correo_electronico', 'telefono', 'direccion', 'ciudad',
            'departamento', 'estado', 'imagen', 'observaciones',
        ]

    def clean(self):
        """Validación condicional según tipo de identificación (DA-001)."""
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo_identificacion')

        if tipo in ['CC', 'CE', 'PS']:
            if not cleaned_data.get('nombres'):
                self.add_error('nombres', 'Este campo es obligatorio para CC, CE o PS.')
            if not cleaned_data.get('apellidos'):
                self.add_error('apellidos', 'Este campo es obligatorio para CC, CE o PS.')

        elif tipo == 'NIT':
            if not cleaned_data.get('razon_social'):
                self.add_error('razon_social', 'Este campo es obligatorio para NIT.')
            if not cleaned_data.get('nombre_comercial'):
                self.add_error('nombre_comercial', 'Este campo es obligatorio para NIT.')
            if not cleaned_data.get('representante_legal'):
                self.add_error('representante_legal', 'Este campo es obligatorio para NIT.')

        return cleaned_data