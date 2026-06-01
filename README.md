# SOLGASES — Sistema de Gestión Empresarial

[🇨🇴 Español](#español) | [🇺🇸 English](#english)

---

<a name="español"></a>
## 🇨🇴 Español

### Descripción

SOLGASES es una plataforma web de gestión empresarial desarrollada con Django 6. Permite administrar usuarios, inventario de productos e insumos, compras, ventas y copias de seguridad de la base de datos desde una interfaz web centralizada, segura y accesible.

### Módulos

| Módulo | Descripción |
|---|---|
| `core` | Autenticación, dashboard, recuperación de contraseña |
| `usuarios` | Gestión de usuarios del sistema, clientes y proveedores |
| `productos` | Catálogo de productos (dotación y EPP) con control de stock |
| `insumos` | Catálogo de gases industriales e insumos con control de stock |
| `compras` | Registro de facturas de compra — actualiza stock automáticamente |
| `ventas` | Registro de facturas de venta — descuenta stock con validación |
| `backup` | Copias de seguridad manuales y automáticas de la base de datos |

### Stack tecnológico

| Componente | Tecnología |
|---|---|
| Backend | Django 6.0.3 + Python 3.13 |
| Base de datos | MySQL (mysqlclient 2.2.8) |
| Frontend | Bootstrap 5.3 + Bootstrap Icons 1.11 |
| Seguridad | django-axes 8.3.1 + django-csp 4.0 |
| Variables de entorno | django-environ 0.13.0 |
| Tareas programadas | APScheduler 3.11.2 + django-apscheduler 0.7.0 |
| Reportes | openpyxl 3.1.5 (Excel) + xhtml2pdf 0.2.17 (PDF) |
| Imágenes | Pillow 12.2.0 |

### Requisitos previos

- Python 3.11 o superior
- MySQL 8.0 o superior
- pip y virtualenv

### Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/<usuario>/solgases.git
cd solgases

# 2. Crear y activar el entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

### Configuración del entorno

Crear el archivo `.env` en la raíz del proyecto basándose en el siguiente ejemplo:

```env
SECRET_KEY=cambiar-por-clave-secreta-segura
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=solgases_db
DB_USER=root
DB_PASSWORD=tu_password
DB_HOST=127.0.0.1
DB_PORT=3306

# Solo para producción (dejar vacío en desarrollo)
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

> En desarrollo el sistema usa `ConsoleEmailBackend` — los correos se muestran en la terminal.
> En producción, completar las variables de email para activar Gmail SMTP.

### Base de datos

```bash
# Crear la base de datos en MySQL
mysql -u root -p -e "CREATE DATABASE solgases_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Aplicar migraciones
python manage.py migrate

# Crear superusuario administrador
python manage.py createsuperuser
```

### Ejecutar el servidor

```bash
python manage.py runserver
```

Acceder en: `http://127.0.0.1:8000`

### Estructura del proyecto

```
solgases/
├── apps/
│   ├── core/           # Login, dashboard, recuperación contraseña
│   ├── usuarios/       # Usuarios, clientes, proveedores
│   ├── productos/      # Catálogo de productos y stock
│   ├── insumos/        # Catálogo de insumos y stock
│   ├── compras/        # Facturas de compra
│   ├── ventas/         # Facturas de venta
│   └── backup/         # Copias de seguridad
├── config/
│   ├── settings.py     # Configuración principal
│   └── urls.py         # URLs raíz
├── static/
│   ├── css/            # solgases.css — hoja de estilos del sistema
│   ├── js/             # Scripts: búsqueda, modal, formset, IVA, accesibilidad
│   └── img/            # Logo y recursos gráficos
├── templates/
│   ├── base.html       # Template base con sidebar y navegación
│   ├── partials/       # Componentes reutilizables
│   └── <módulo>/       # Templates de cada módulo
├── backups/            # Archivos de backup (excluido de git)
├── .env                # Variables de entorno (excluido de git)
├── manage.py
└── requirements.txt
```

### Roles y permisos

El sistema tiene dos roles:

- **ADMIN** — acceso completo a todos los módulos
- **EMP** (Empleado) — acceso de lectura y registro, sin permisos de configuración ni eliminación

La matriz de permisos completa está disponible en el **Manual del sistema** en `/manual/`.

### Seguridad

- Protección contra fuerza bruta con `django-axes` (bloqueo tras 5 intentos, 15 min)
- Content Security Policy activa (`django-csp`) — sin inline scripts
- Sesiones con expiración automática (1 hora de inactividad)
- HTTPS y cabeceras de seguridad activadas en producción (`DEBUG=False`)

### Accesibilidad

El sistema incluye un widget de accesibilidad (botón flotante inferior derecho) con:

- Ajuste de tamaño de letra (8px – 20px)
- Modo alto contraste
- Modo daltonismo (escala de grises)

Cumple con los criterios WCAG 2.1: SC 1.4.1, 1.4.11, 2.4.1, 4.1.2.

---

<a name="english"></a>
## 🇺🇸 English

### Description

SOLGASES is a web-based business management platform built with Django 6. It provides centralized management of users, product and supply inventory, purchases, sales, and database backups through a secure, accessible web interface.

### Modules

| Module | Description |
|---|---|
| `core` | Authentication, dashboard, password recovery |
| `usuarios` | System users, customers, and supplier management |
| `productos` | Product catalog (PPE and workwear) with stock control |
| `insumos` | Industrial gas and supply catalog with stock control |
| `compras` | Purchase invoice recording — automatically updates stock |
| `ventas` | Sales invoice recording — stock deduction with validation |
| `backup` | Manual and automatic database backups |

### Tech Stack

| Component | Technology |
|---|---|
| Backend | Django 6.0.3 + Python 3.13 |
| Database | MySQL (mysqlclient 2.2.8) |
| Frontend | Bootstrap 5.3 + Bootstrap Icons 1.11 |
| Security | django-axes 8.3.1 + django-csp 4.0 |
| Environment | django-environ 0.13.0 |
| Scheduler | APScheduler 3.11.2 + django-apscheduler 0.7.0 |
| Reports | openpyxl 3.1.5 (Excel) + xhtml2pdf 0.2.17 (PDF) |
| Images | Pillow 12.2.0 |

### Prerequisites

- Python 3.11 or higher
- MySQL 8.0 or higher
- pip and virtualenv

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/<user>/solgases.git
cd solgases

# 2. Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Environment Configuration

Create a `.env` file in the project root based on the following template:

```env
SECRET_KEY=change-to-a-secure-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=solgases_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=3306

# Production only (leave empty in development)
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

> In development, the system uses `ConsoleEmailBackend` — emails are printed to the terminal.
> In production, fill in the email variables to enable Gmail SMTP.

### Database Setup

```bash
# Create the database in MySQL
mysql -u root -p -e "CREATE DATABASE solgases_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Apply migrations
python manage.py migrate

# Create admin superuser
python manage.py createsuperuser
```

### Running the Server

```bash
python manage.py runserver
```

Open in browser: `http://127.0.0.1:8000`

### Project Structure

```
solgases/
├── apps/
│   ├── core/           # Login, dashboard, password recovery
│   ├── usuarios/       # Users, customers, suppliers
│   ├── productos/      # Product catalog and stock
│   ├── insumos/        # Supply catalog and stock
│   ├── compras/        # Purchase invoices
│   ├── ventas/         # Sales invoices
│   └── backup/         # Database backups
├── config/
│   ├── settings.py     # Main configuration
│   └── urls.py         # Root URL configuration
├── static/
│   ├── css/            # solgases.css — system stylesheet
│   ├── js/             # Scripts: search, modal, formset, VAT, accessibility
│   └── img/            # Logo and graphic assets
├── templates/
│   ├── base.html       # Base template with sidebar and navigation
│   ├── partials/       # Reusable components
│   └── <module>/       # Module-specific templates
├── backups/            # Backup files (git-ignored)
├── .env                # Environment variables (git-ignored)
├── manage.py
└── requirements.txt
```

### Roles and Permissions

The system has two roles:

- **ADMIN** — full access to all modules
- **EMP** (Employee) — read and record access, no configuration or deletion rights

The full permissions matrix is available in the **System Manual** at `/manual/`.

### Security

- Brute-force protection via `django-axes` (lockout after 5 attempts, 15 min cooldown)
- Active Content Security Policy (`django-csp`) — no inline scripts
- Session expiration (1 hour of inactivity)
- HTTPS and security headers enabled in production (`DEBUG=False`)

### Accessibility

The system includes an accessibility widget (floating button, bottom-right) with:

- Font size adjustment (8px – 20px)
- High contrast mode
- Colorblind mode (grayscale)

Complies with WCAG 2.1 criteria: SC 1.4.1, 1.4.11, 2.4.1, 4.1.2.
