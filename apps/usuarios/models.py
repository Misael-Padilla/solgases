from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from apps.usuarios.managers import UsuarioManager

# --- MODELO DE USUARIO PERSONALIZADO ---

class Usuario(AbstractBaseUser, PermissionsMixin):
    """
    Representa a los trabajadores o administradores que acceden al sistema.
    Se utiliza el correo electrónico como credencial principal (login).
    """

    # Opciones para listas desplegables
    TIPO_IDENTIFICACION_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('PS', 'Pasaporte'),
    ]

    ROL_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('EMP', 'Empleado'),
    ]

    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]

    # Campos de identificación y contacto
    tipo_identificacion = models.CharField(max_length=5, choices=TIPO_IDENTIFICACION_CHOICES)
    identificacion      = models.CharField(max_length=20, unique=True)
    nombres             = models.CharField(max_length=100)
    apellidos           = models.CharField(max_length=100)
    correo_electronico  = models.EmailField(unique=True) # Requerido para el USERNAME_FIELD
    telefono            = models.CharField(max_length=20)
    direccion           = models.CharField(max_length=200)
    ciudad              = models.CharField(max_length=100)
    departamento        = models.CharField(max_length=100)
    
    # Control de permisos y estado
    rol                 = models.CharField(max_length=10, choices=ROL_CHOICES)
    estado              = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='ACTIVO')
    imagen              = models.ImageField(upload_to='usuarios/', null=True, blank=True)
    observaciones       = models.TextField(null=True, blank=True)
    fecha_creacion      = models.DateTimeField(auto_now_add=True)

    # Atributos de Django Auth para gestión de permisos
    is_staff            = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)

    # Manager que controla la creación de usuarios desde consola/admin
    objects = UsuarioManager()

    # Configuración de credenciales
    USERNAME_FIELD  = 'correo_electronico'
    REQUIRED_FIELDS = ['nombres', 'apellidos', 'identificacion']

    class Meta:
        db_table = 'usuario' # Nombre de la tabla en MySQL
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        # Muestra el nombre completo y correo en el panel administrativo
        return f'{self.nombres} {self.apellidos} ({self.correo_electronico})'

# --- MODELO DE CLIENTE ---

class Cliente(models.Model):
    """
    Almacena la información de los compradores (personas naturales o empresas).
    """

    TIPO_IDENTIFICACION_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('PS', 'Pasaporte'),
        ('NIT', 'NIT'),
    ]

    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]

    # Identificación básica
    tipo_identificacion = models.CharField(max_length=5, choices=TIPO_IDENTIFICACION_CHOICES)
    identificacion      = models.CharField(max_length=20, unique=True)
    
    # Campos para personas naturales
    nombres             = models.CharField(max_length=100, null=True, blank=True)
    apellidos           = models.CharField(max_length=100, null=True, blank=True)
    
    # Campos para personas jurídicas (Empresas)
    razon_social        = models.CharField(max_length=200, null=True, blank=True)
    nombre_comercial    = models.CharField(max_length=200, null=True, blank=True)
    representante_legal = models.CharField(max_length=200, null=True, blank=True)
    
    # Ubicación y contacto
    correo_electronico  = models.EmailField(null=True, blank=True)
    telefono            = models.CharField(max_length=20)
    direccion           = models.CharField(max_length=200)
    ciudad              = models.CharField(max_length=100)
    departamento        = models.CharField(max_length=100)
    
    # Otros datos
    estado              = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='ACTIVO')
    imagen              = models.ImageField(upload_to='clientes/', null=True, blank=True)
    observaciones       = models.TextField(null=True, blank=True)
    fecha_creacion      = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cliente'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        # Valida si es empresa (NIT) para mostrar la razón social, sino el nombre personal
        if self.tipo_identificacion == 'NIT':
            return f'{self.razon_social} ({self.identificacion})'
        return f'{self.nombres} {self.apellidos} ({self.identificacion})'

# --- MODELO DE PROVEEDOR ---

class Proveedor(models.Model):
    """
    Almacena la información de los proveedores de gases y equipos.
    """

    TIPO_IDENTIFICACION_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('PS', 'Pasaporte'),
        ('NIT', 'NIT'),
    ]

    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]

    # Identificación básica
    tipo_identificacion = models.CharField(max_length=5, choices=TIPO_IDENTIFICACION_CHOICES)
    identificacion      = models.CharField(max_length=20, unique=True)
    
    # Campos para personas naturales
    nombres             = models.CharField(max_length=100, null=True, blank=True)
    apellidos           = models.CharField(max_length=100, null=True, blank=True)
    
    # Campos para empresas
    razon_social        = models.CharField(max_length=200, null=True, blank=True)
    nombre_comercial    = models.CharField(max_length=200, null=True, blank=True)
    representante_legal = models.CharField(max_length=200, null=True, blank=True)
    
    # Ubicación y contacto
    correo_electronico  = models.EmailField(null=True, blank=True)
    telefono            = models.CharField(max_length=20)
    direccion           = models.CharField(max_length=200)
    ciudad              = models.CharField(max_length=100)
    departamento        = models.CharField(max_length=100)
    
    # Otros datos
    estado              = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='ACTIVO')
    imagen              = models.ImageField(upload_to='proveedores/', null=True, blank=True)
    observaciones       = models.TextField(null=True, blank=True)
    fecha_creacion      = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'proveedor'
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

    def __str__(self):
        # Similar a clientes, diferencia entre razón social y nombres personales
        if self.tipo_identificacion == 'NIT':
            return f'{self.razon_social} ({self.identificacion})'
        return f'{self.nombres} {self.apellidos} ({self.identificacion})'