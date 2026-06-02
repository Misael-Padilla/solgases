from django.test import SimpleTestCase, TestCase

from .models import Cliente, Proveedor, Usuario


# ─── Tests: UsuarioManager ────────────────────────────────────────────────────

class UsuarioManagerTest(TestCase):
    """
    Verifica el manager personalizado del modelo Usuario.
    Usa TestCase porque create_user y create_superuser persisten en BD.
    """

    def test_create_user_usa_correo_como_credencial(self):
        """El USERNAME_FIELD debe ser correo_electronico, no username."""
        usuario = Usuario.objects.create_user(
            correo_electronico='empleado@solgases.com',
            password='clave123',
            tipo_identificacion='CC',
            identificacion='11223344',
            nombres='Ana',
            apellidos='Gómez',
            telefono='3005555555',
            direccion='Calle 10',
            ciudad='Bogotá',
            departamento='Cundinamarca',
            rol='EMP',
        )
        self.assertEqual(usuario.correo_electronico, 'empleado@solgases.com')
        self.assertEqual(Usuario.USERNAME_FIELD, 'correo_electronico')

    def test_create_user_hashea_la_contrasena(self):
        """La contraseña no debe guardarse en texto plano."""
        usuario = Usuario.objects.create_user(
            correo_electronico='hash@solgases.com',
            password='clave_secreta',
            tipo_identificacion='CC',
            identificacion='22334455',
            nombres='Pedro',
            apellidos='Ruiz',
            telefono='3006666666',
            direccion='Carrera 5',
            ciudad='Medellín',
            departamento='Antioquia',
            rol='EMP',
        )
        self.assertNotEqual(usuario.password, 'clave_secreta')
        self.assertTrue(usuario.check_password('clave_secreta'))

    def test_create_superuser_tiene_rol_admin(self):
        """create_superuser debe asignar rol ADMIN por defecto."""
        admin = Usuario.objects.create_superuser(
            correo_electronico='admin@solgases.com',
            password='admin123',
            tipo_identificacion='CC',
            identificacion='33445566',
            nombres='Super',
            apellidos='Admin',
            telefono='3007777777',
            direccion='Av Principal',
            ciudad='Cali',
            departamento='Valle del Cauca',
        )
        self.assertEqual(admin.rol, 'ADMIN')

    def test_create_superuser_tiene_is_staff_true(self):
        """create_superuser debe marcar is_staff=True para acceso al panel de administración."""
        admin = Usuario.objects.create_superuser(
            correo_electronico='staff@solgases.com',
            password='admin123',
            tipo_identificacion='CC',
            identificacion='44556677',
            nombres='Staff',
            apellidos='Admin',
            telefono='3008888888',
            direccion='Calle 50',
            ciudad='Barranquilla',
            departamento='Atlántico',
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)


# ─── Tests: Usuario __str__ ───────────────────────────────────────────────────

class UsuarioStrTest(SimpleTestCase):
    """Verifica el formato de representación textual del modelo Usuario."""

    def test_str_retorna_nombre_completo_y_correo(self):
        """__str__ debe retornar 'Nombres Apellidos (correo)'."""
        usuario = Usuario(
            nombres='Jorge',
            apellidos='Padilla',
            correo_electronico='ing.jorge.padilla.cardenas@gmail.com',
        )
        self.assertEqual(str(usuario), 'Jorge Padilla (ing.jorge.padilla.cardenas@gmail.com)')


# ─── Tests: Cliente __str__ ───────────────────────────────────────────────────

class ClienteStrTest(SimpleTestCase):
    """
    Verifica el formato de representación textual del modelo Cliente.
    La lógica es condicional: NIT muestra razón social, CC/CE/PS muestra nombre personal.
    """

    def test_str_persona_natural_retorna_nombre_e_identificacion(self):
        """Cliente con CC debe mostrar 'Nombres Apellidos (identificacion)'."""
        cliente = Cliente(
            tipo_identificacion='CC',
            identificacion='87654321',
            nombres='Juan',
            apellidos='Pérez',
        )
        self.assertEqual(str(cliente), 'Juan Pérez (87654321)')

    def test_str_empresa_retorna_razon_social_e_identificacion(self):
        """Cliente con NIT debe mostrar 'Razón Social (identificacion)'."""
        cliente = Cliente(
            tipo_identificacion='NIT',
            identificacion='900123456',
            razon_social='Gases del Norte S.A.S.',
        )
        self.assertEqual(str(cliente), 'Gases del Norte S.A.S. (900123456)')

    def test_str_cliente_con_ce_retorna_nombre_personal(self):
        """Cliente con CE también debe mostrar nombre personal, no razón social."""
        cliente = Cliente(
            tipo_identificacion='CE',
            identificacion='E123456',
            nombres='María',
            apellidos='López',
        )
        self.assertEqual(str(cliente), 'María López (E123456)')


# ─── Tests: Proveedor __str__ ─────────────────────────────────────────────────

class ProveedorStrTest(SimpleTestCase):
    """
    Verifica el formato de representación textual del modelo Proveedor.
    Misma lógica condicional que Cliente: NIT vs persona natural.
    """

    def test_str_proveedor_persona_natural_retorna_nombre(self):
        """Proveedor con CC debe mostrar 'Nombres Apellidos (identificacion)'."""
        proveedor = Proveedor(
            tipo_identificacion='CC',
            identificacion='55667788',
            nombres='Carlos',
            apellidos='Martínez',
        )
        self.assertEqual(str(proveedor), 'Carlos Martínez (55667788)')

    def test_str_proveedor_empresa_retorna_razon_social(self):
        """Proveedor con NIT debe mostrar 'Razón Social (identificacion)'."""
        proveedor = Proveedor(
            tipo_identificacion='NIT',
            identificacion='800200300',
            razon_social='Distribuidora Nacional S.A.',
        )
        self.assertEqual(str(proveedor), 'Distribuidora Nacional S.A. (800200300)')
