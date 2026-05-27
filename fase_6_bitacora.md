# SOLGASES — Bitácora Fase 6 (Pruebas y Verificación)

> **Proyecto:** SOLGASES — Plataforma de Gestión Empresarial
> **Fase:** 6 — Pruebas y Verificación Módulo por Módulo
> **Autor:** Jorge Padilla
> **Fecha de inicio:** 06 de mayo de 2026
> **Última actualización:** 26 de mayo de 2026
> **Commit de referencia (inicio Fase 6):** `b2a41ed`
> **Protocolo:** Protocolo de Veracidad — Fase 6 v1.1

---

## Índice de módulos

| Orden | Módulo | Estado | Fecha aprobación | Commit cierre |
|---|---|---|---|---|
| 1 | `core` | ✅ Aprobado | 2026-05-26 | `39bfcc5` |
| 2 | `usuarios` | ⏳ Pendiente | — | — |
| 3 | `productos` | ⏳ Pendiente | — | — |
| 4 | `insumos` | ⏳ Pendiente | — | — |
| 5 | `compras` | ⏳ Pendiente | — | — |
| 6 | `ventas` | ⏳ Pendiente | — | — |
| 7 | `backup` | ⏳ Pendiente | — | — |

---

## Módulo: `core` — ✅ Aprobado

### Capas verificadas

| Capa | Estado | Observaciones |
|---|---|---|
| 1 — Modelo | N/A | Core no tiene modelos |
| 2 — Formulario | ✅ Verificada | `CustomPasswordResetForm` creado para adaptarse al modelo Usuario |
| 3 — Vistas | ✅ Verificada | INC-001 a INC-004 corregidas |
| 4 — Templates | ✅ Verificada | INC-005 a INC-032 corregidas, password reset implementado |
| 5 — Integración | ✅ Verificada | I-01 e I-04 verificados sin incidencias |

### Incidencias detectadas y corregidas

#### Capa 3 — Vistas (`views.py`)

| Código | Severidad | Descripción | Estado |
|---|---|---|---|
| INC-001 | Alta | Login permite acceso a usuarios INACTIVOS | ✅ Corregido |
| INC-002 | Media | Imports duplicados y desorganizados | ✅ Corregido |
| INC-003 | Media | `cerrar_sesion` acepta método GET — riesgo CSRF | ✅ Corregido — `@require_POST` |
| INC-004 | Alta | Sin mensajes flash en flujo login/logout | ✅ Corregido |

#### Capa 3 — Configuración (`settings.py`)

| Código | Severidad | Descripción | Estado |
|---|---|---|---|
| INC-017 | Alta | Sin protección contra fuerza bruta (OWASP A07:2025) | ✅ Corregido — django-axes |
| INC-018 | Media | Sin registro de intentos fallidos | ✅ Corregido — django-axes |
| INC-019 | Alta | Redirect URLs sin namespace | ✅ Corregido |
| INC-020 | Media | ALLOWED_HOSTS vacío | ✅ Corregido |
| INC-021 | Media | Sin configuración de sesiones | ✅ Corregido |
| INC-022 | Media | Sin configuraciones de seguridad para producción | ✅ Corregido |
| INC-023 | Media | Sin AUTHENTICATION_BACKENDS | ✅ Corregido |
| INC-024 | Baja | Sin DEFAULT_AUTO_FIELD | ✅ Corregido |
| INC-025 | Alta | Bloqueo de axes no mostraba mensaje personalizado | ✅ Corregido — lockout.html |

#### Capa 4 — Templates

| Código | Severidad | Descripción | Estado |
|---|---|---|---|
| INC-004 | Alta | Bloque mensajes flash faltante en base.html | ✅ Corregido |
| INC-005 | Media | Estilos inline en inicio.html | ✅ Corregido — clases CSS |
| INC-006 | Media | Breadcrumbs no implementados (transversal) | ✅ Corregido |
| INC-012 | Media | CSS duplicado e inline en login.html | ✅ Corregido |
| INC-013 | Alta | Mensajes de error no se muestran en login | ✅ Corregido |
| INC-014 | Media | Login footer text (pendiente Fase 5) | ✅ Corregido — datos ficticios |
| INC-015 | Media | Sin atributos autocomplete en login | ✅ Corregido |
| INC-016 | Baja | Sin role="alert" para accesibilidad | ✅ Corregido |
| INC-026 | Media | Mensajes genéricos en login | ✅ Corregido — correo vs contraseña |
| INC-027 | Baja | AuthenticationForm sin usar | ✅ Corregido — eliminado |
| INC-028 | Media | Sidebar marca Dashboard activo para todas las páginas de core | ✅ Corregido |
| INC-029 | Baja | Estilo inline en contenedor principal | ✅ Corregido — `.layout-principal` |
| INC-030 | Media | Estilos inline en manual.html | ✅ Corregido — `.icono-acento`, `.texto-descripcion` |
| INC-031 | Baja | Bootstrap `card` en vez de `.card-detalle` en manual | ✅ Corregido |

#### Capa 4 — CSS (`solgases.css`)

| Código | Severidad | Descripción | Estado |
|---|---|---|---|
| INC-007 | Media | `.btn-cerrar-sesion` sin reset para `<button>` | ✅ Corregido |
| INC-008 | Media | Sin clase CSS para iconos de métricas | ✅ Corregido |
| INC-009 | Media | Sin clase `.alerta-sobrestock` | ✅ Corregido |
| INC-010 | Media | Sin media queries para responsive | ✅ Corregido |
| INC-011 | Baja | Sin clase `.link-ver-todo` | ✅ Corregido |

#### Capa 4 — Email (`apps/core/mail.py`)

| Código | Severidad | Descripción | Estado |
|---|---|---|---|
| INC-032 | Media | URL con `=` en consola por codificación quoted-printable de Django | ✅ Corregido — ConsoleEmailBackend personalizado |

### Solicitudes de cambio

| Código | Tipo | Descripción | Estado |
|---|---|---|---|
| SC-001 | Agregar | Breadcrumbs (base.html + CSS + views.py) | ✅ Implementado |
| SC-002 | Agregar | django-axes protección fuerza bruta | ✅ Implementado |
| SC-003 | Agregar | Toggle mostrar/ocultar contraseña en login | ✅ Implementado |
| SC-004 | Agregar | Imagen de fondo en login | ✅ Implementado |
| SC-005 | Agregar | Footer con datos ficticios en login | ✅ Implementado |
| SC-006 | Agregar | Template lockout.html | ✅ Implementado |
| SC-007 | Agregar | Mensajes específicos en login (correo vs contraseña) | ✅ Implementado |
| SC-008 | Agregar | Variables CSS nuevas | ✅ Implementado |
| SC-009 | Agregar | Media queries responsive (768px, 576px) | ✅ Implementado |
| SC-010 | Agregar | Sección Login en solgases.css | ✅ Implementado |
| SC-011 | Agregar | Clase `.layout-principal` | ✅ Implementado |
| SC-012 | Agregar | Password reset completo (4 templates + email + form personalizado) | ✅ Implementado |
| SC-013 | Agregar | Clases `.tabla-sistema-sm`, `.texto-vacio-inline`, `.icono-acento`, `.texto-descripcion` | ✅ Implementado |
| SC-014 | Agregar | `EMAIL_FIELD` en modelo Usuario | ✅ Implementado |
| SC-015 | Agregar | Email dual console/SMTP con variables de entorno + ConsoleEmailBackend legible | ✅ Implementado |
| SC-016 | Modificar | `.card-detalle` — eliminado `height: 100%` | ✅ Implementado |

### Decisiones tomadas en Fase 6

| Decisión | Justificación |
|---|---|
| `AXES_LOCKOUT_PARAMETERS = ['username']` — sin `ip_address` | Sistema interno de empresa. Bloqueo por usuario es suficiente. Agregar IP aumenta complejidad sin beneficio proporcional. |
| `EMAIL_BACKEND` default = ConsoleEmailBackend personalizado | En desarrollo el URL del password reset aparece legible en la terminal. En producción se configura Gmail SMTP vía `.env`. |

### Pendientes de Fase 5 resueltos en `core`

| Pendiente | Estado |
|---|---|
| Login footer text | ✅ Implementado con datos ficticios |

### Transversales implementados en `core`

| Transversal | Estado |
|---|---|
| Breadcrumbs | ✅ Implementado en inicio y manual |
| Search/filters/pagination | N/A — core no tiene listados |

### Resumen de cierre — `core`

```
## Módulo: core — APROBADO ✅

- Fecha de inicio de revisión: 2026-05-06
- Fecha de aprobación: 2026-05-26
- Commits del módulo:
    0604f36 — fix(core): seguridad login, django-axes, templates y CSS — Fase 6
    d1e6771 — feat(core): flujo recuperación de contraseña — Fase 6
    429bd50 — feat(core): email dual console/SMTP con backend legible
    39bfcc5 — test(core): verificación Fase 6 completada

Funcionalidades verificadas:
- Login seguro con mensajes específicos, toggle contraseña, imagen de fondo
- Protección fuerza bruta (django-axes) con template lockout personalizado
- Cierre de sesión solo por POST (CSRF)
- Dashboard con métricas reales y últimas ventas/compras
- Manual de usuario con diseño coherente
- Breadcrumbs en inicio y manual
- Flujo completo de recuperación de contraseña (4 templates + email + form)
- Email dual: consola legible en desarrollo, Gmail SMTP en producción

Incidencias: 32 detectadas, 32 corregidas
Solicitudes de cambio: 16 implementadas
Pendientes de Fase 5 resueltos: 1 (Login footer text)
Transversales: Breadcrumbs ✅ | Search/pagination N/A
```

---

## Archivos modificados en Fase 6

| Archivo | Cambios |
|---|---|
| `apps/core/views.py` | Login seguro, mensajes específicos, breadcrumbs, código limpio |
| `apps/core/urls.py` | Password reset con namespace, form_class, email_template, success_url |
| `apps/core/forms.py` | **Nuevo** — CustomPasswordResetForm (filtra por estado en vez de is_active) |
| `apps/core/mail.py` | **Nuevo** — ConsoleEmailBackend que decodifica quoted-printable |
| `apps/usuarios/models.py` | Agregado `EMAIL_FIELD = 'correo_electronico'` |
| `config/settings.py` | django-axes, sesiones, seguridad producción, AUTHENTICATION_BACKENDS, email dual |
| `static/css/solgases.css` | Reescrito: 19 secciones, variables, breadcrumbs, login, responsive, clases nuevas |
| `templates/base.html` | Logout POST, mensajes flash, breadcrumbs, sidebar corregido, layout-principal |
| `templates/core/inicio.html` | Inline styles eliminados — usa clases CSS |
| `templates/core/login.html` | Reconstruido: CSS externo, mensajes flash, toggle, fondo, footer, accesibilidad |
| `templates/core/lockout.html` | **Nuevo** — bloqueo de cuenta por django-axes |
| `templates/core/manual.html` | Corregido: card-detalle, icono-acento, texto-descripcion |
| `templates/core/password_reset.html` | **Nuevo** — formulario recuperar contraseña |
| `templates/core/password_reset_done.html` | **Nuevo** — confirmación envío de correo |
| `templates/core/password_reset_confirm.html` | **Nuevo** — formulario nueva contraseña |
| `templates/core/password_reset_complete.html` | **Nuevo** — confirmación cambio exitoso |
| `templates/core/password_reset_email.html` | **Nuevo** — cuerpo del correo de recuperación |
| `requirements.txt` | django-axes agregado |

---

## Resumen de commits — Fase 6

| Hash | Descripción | Fecha |
|---|---|---|
| `0604f36` | fix(core): seguridad login, django-axes, templates y CSS — Fase 6 | 2026-05-19 |
| `d1e6771` | feat(core): flujo recuperación de contraseña — Fase 6 | 2026-05-26 |
| `429bd50` | feat(core): email dual console/SMTP con backend legible | 2026-05-26 |
| `39bfcc5` | test(core): verificación Fase 6 completada | 2026-05-26 |

---

*Bitácora actualizada el 26 de mayo de 2026.*
