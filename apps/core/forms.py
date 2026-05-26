from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

UserModel = get_user_model()


class CustomPasswordResetForm(PasswordResetForm):
    """Formulario de recuperación de contraseña adaptado al modelo Usuario.

    Django's PasswordResetForm filtra por is_active=True a nivel de base de datos,
    pero el modelo Usuario usa estado='ACTIVO' (CharField) en vez de is_active
    (BooleanField). Este formulario sobreescribe get_users() para usar el campo
    correcto y mantener compatibilidad con el flujo de password reset de Django.
    """

    def get_users(self, email):
        """Retorna usuarios activos que coincidan con el correo ingresado."""
        email_field_name = UserModel.get_email_field_name()
        active_users = UserModel._default_manager.filter(
            **{
                '%s__iexact' % email_field_name: email,
                'estado': 'ACTIVO',
            }
        )
        return (
            u
            for u in active_users
            if u.has_usable_password()
        )