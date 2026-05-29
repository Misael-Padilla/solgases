# SOLGASES — Bitácora Fase 6 (Pruebas y Verificación)

> **Proyecto:** SOLGASES — Plataforma de Gestión Empresarial
> **Fase:** 6 — Pruebas y Verificación Módulo por Módulo
> **Autor:** Jorge Padilla
> **Fecha de inicio:** 06 de mayo de 2026
> **Última actualización:** 29 de mayo de 2026
> **Commit de referencia (inicio Fase 6):** `b2a41ed`
> **Protocolo:** Protocolo de Veracidad — Fase 6 v1.1

---

## Índice de módulos

| Orden | Módulo | Estado | Fecha aprobación | Commit cierre |
|---|---|---|---|---|
| 1 | `core` | ✅ Aprobado | 2026-05-26 | `39bfcc5` |
| 2 | `usuarios` | ✅ Aprobado | 2026-05-29 | `88d74b4` |
| 3 | `productos` | ✅ Aprobado | 2026-05-29 | `9295480` |
| 4 | `insumos` | ✅ Aprobado | 2026-05-29 | `670218d` |
| 5 | `compras` | ✅ Aprobado | 2026-05-29 | `840fb04` |
| 6 | `ventas` | ✅ Aprobado | 2026-05-29 | `132b459` |
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

## Módulo: `usuarios` — ✅ Aprobado

### Capas verificadas

| Capa | Estado | Observaciones |
|---|---|---|
| 1 — Modelo | ✅ Verificada | Campos auditoría agregados: `creado_por`, `modificado_por`, `modificado_en` |
| 2 — Formulario | ✅ Verificada | `aria-required` via templatetag `form_extras` |
| 3 — Vistas | ✅ Verificada | `@require_POST`, auditoría en create/edit, exportación Excel |
| 4 — Templates | ✅ Verificada | `aria-label`, badges con ícono, `scope="col"`, búsqueda en tiempo real |
| 5 — Integración | ✅ Verificada | I-01 sidebar ✅ I-02 links ✅ I-03 datos coherentes ✅ I-04 dashboard contadores reales ✅ |

### Incidencias detectadas y corregidas

| Código | Severidad | Descripción | Commit | Estado |
|---|---|---|---|---|
| INC-033 | Alta | `cambiar_estado_*` acepta GET — riesgo CSRF | `45fcafb` | ✅ Corregido |
| INC-034 | Media | Botones de acción sin `aria-label` — WCAG | `bbac370` | ✅ Corregido |
| INC-035 | Media | Sidebar solo resalta en página exacta de lista | `60c55c3` | ✅ Corregido |
| INC-036 | Media | `campo_form.html` sin `aria-required` en campos requeridos | `3613bd4` | ✅ Corregido |
| INC-037 | Media | Sin `SECURE_REFERRER_POLICY` en settings | `dfbf014` | ✅ Corregido |
| INC-038 | Media | Sin Content Security Policy | `bc6da03` | ✅ Corregido |
| INC-039 | Baja | `check --deploy` reporta SECRET_KEY insegura | sin commit (.env) | ✅ Corregido |
| INC-040 | Baja | Sin skip-to-content — WCAG 2.4.1 | `691625d` + `27d7ae4` | ✅ Corregido |
| INC-041 | Baja | Badges de estado usan solo color — WCAG 1.4.1 | `d2f6304` | ✅ Corregido |
| INC-042 | Baja | `<th>` sin `scope="col"` — WCAG 1.3.1 | `e901f91` | ✅ Corregido |
| INC-043 | Media | Sin auditoría de creación/modificación ni exportación Excel | `65ce604` | ✅ Corregido |

### Solicitudes de cambio

| Código | Tipo | Descripción | Commit | Estado |
|---|---|---|---|---|
| SC-T01 | Agregar | Breadcrumbs en 12 vistas de usuarios | `07638d1` | ✅ Implementado |
| SC-T02 | Agregar | Búsqueda en tiempo real con debounce en 3 listas | `d86ada6` | ✅ Implementado |
| SC-T03 | Agregar | Logo empresa en encabezado de reportes Excel | `5d342b1` | ✅ Implementado |
| SC-T04 | Agregar | Reporte PDF (facturas/órdenes) | — | ⏳ Diferido a módulos ventas/compras |
| SC-T05 | Agregar | Historial de cambios con observaciones — activar/desactivar/editar | `73c0528` | ✅ Implementado |
| SC-T06 | Agregar | Paginación 15 registros por página en 3 listas | `b172195` | ✅ Implementado |
| SC-T07 | Agregar | Matriz de Roles 3.4 en Manual del sistema | `6188480` | ✅ Implementado |
| SC-A01 | Agregar | Widget de accesibilidad (tamaño letra, alto contraste) | — | ⏳ Al final Fase 6 |

### Decisiones tomadas en módulo `usuarios`

| Decisión | Justificación |
|---|---|
| `django-simple-history` descartado | Overkill para sistema interno; campos manuales `creado_por/modificado_por` son suficientes |
| `openpyxl` para Excel | Suficiente para volúmenes de SOLGASES; más simple que xlsxwriter |
| `zoneinfo` en vez de `pytz` | Python 3.9+ built-in; no requiere dependencia extra |
| `'unsafe-inline'` en `style-src` CSP | Bootstrap 5 inyecta estilos inline dinámicos; es el compromiso estándar |
| Búsqueda via GET (no POST) | URL compartible/recargable; compatible con historial del navegador |
| Debounce 350ms | Balance entre respuesta inmediata y carga al servidor |

### Nuevas dependencias instaladas

| Paquete | Versión | Propósito |
|---|---|---|
| `django-csp` | 4.0 | Content Security Policy |
| `openpyxl` | 3.1.5 | Exportación Excel |

### Nuevos archivos creados

| Archivo | Descripción |
|---|---|
| `apps/core/templatetags/__init__.py` | Paquete templatetags |
| `apps/core/templatetags/form_extras.py` | Filtro `with_aria_required` |
| `static/js/busqueda.js` | Búsqueda en tiempo real con debounce |
| `static/js/modal_estado.js` | **Nuevo** — modal confirmación con observación obligatoria |
| `apps/usuarios/migrations/0002_*.py` | Campos de auditoría |
| `apps/usuarios/migrations/0003_historialcambio.py` | **Nuevo** — modelo HistorialCambio |
| `static/img/logo_solgases.png` | Logo de la empresa para reportes Excel |

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

## Resumen de commits — módulo `usuarios`

| Hash | Descripción | Fecha |
|---|---|---|
| `45fcafb` | fix(usuarios): cambiar_estado requiere POST — previene CSRF por GET | 2026-05-26 |
| `bbac370` | fix(usuarios): aria-label en botones de tabla — accesibilidad WCAG | 2026-05-26 |
| `60c55c3` | fix(usuarios): sidebar resalta correctamente en sub-páginas | 2026-05-26 |
| `3613bd4` | fix(core): aria-required en campos requeridos via templatetag | 2026-05-26 |
| `dfbf014` | fix(config): SECURE_REFERRER_POLICY strict-origin-when-cross-origin | 2026-05-27 |
| `bc6da03` | feat(config): Content Security Policy via django-csp 4.0 | 2026-05-27 |
| `691625d` | feat(accesibilidad): skip-to-content y aria-label nav — WCAG 2.4.1 | 2026-05-27 |
| `27d7ae4` | fix(accesibilidad): skip-to-content invisible hasta foco — tecnica sr-only | 2026-05-27 |
| `d2f6304` | feat(usuarios): icono en badges de estado — WCAG 1.4.1 | 2026-05-27 |
| `e901f91` | fix(usuarios): scope=col en th de tablas — WCAG 1.3.1 | 2026-05-27 |
| `d86ada6` | feat(usuarios): busqueda en tiempo real con debounce en listas | 2026-05-28 |
| `65ce604` | feat(usuarios): auditoria creado_por/modificado_por y exportacion Excel | 2026-05-28 |
| `5d342b1` | feat(usuarios): logo empresa en encabezado de reportes Excel | 2026-05-29 |
| `211d13c` | feat(usuarios): tooltips Bootstrap 5 en botones de accion | 2026-05-29 |
| `07638d1` | feat(usuarios): breadcrumbs en 12 vistas — SC-T01 | 2026-05-29 |
| `211d13c` | feat(usuarios): tooltips Bootstrap 5 en botones de accion | 2026-05-29 |
| `73c0528` | feat(usuarios): historial de cambios con observaciones obligatorias | 2026-05-29 |
| `b172195` | feat(usuarios): paginacion 15 registros por pagina en listas | 2026-05-29 |
| `6188480` | feat(usuarios): matriz de roles en manual del sistema | 2026-05-29 |
| `88d74b4` | test(usuarios): verificacion Fase 6 completada | 2026-05-29 |

---

---

## Resumen de cierre — `usuarios`

```
## Módulo: usuarios — APROBADO ✅

- Fecha de inicio de revisión: 2026-05-26
- Fecha de aprobación: 2026-05-29
- Commits del módulo:
    45fcafb — fix(usuarios): cambiar_estado requiere POST — previene CSRF
    bbac370 — fix(usuarios): aria-label en botones de tabla
    60c55c3 — fix(usuarios): sidebar resalta en sub-páginas
    3613bd4 — fix(core): aria-required en campos requeridos via templatetag
    dfbf014 — fix(config): SECURE_REFERRER_POLICY
    bc6da03 — feat(config): Content Security Policy via django-csp 4.0
    691625d — feat(accesibilidad): skip-to-content — WCAG 2.4.1
    27d7ae4 — fix(accesibilidad): skip-to-content invisible hasta foco
    d2f6304 — feat(usuarios): icono en badges de estado — WCAG 1.4.1
    e901f91 — fix(usuarios): scope=col en th de tablas — WCAG 1.3.1
    d86ada6 — feat(usuarios): búsqueda en tiempo real con debounce
    65ce604 — feat(usuarios): auditoría creado_por/modificado_por + Excel
    5d342b1 — feat(usuarios): logo empresa en encabezado Excel
    211d13c — feat(usuarios): tooltips Bootstrap 5
    07638d1 — feat(usuarios): breadcrumbs en 12 vistas
    73c0528 — feat(usuarios): historial de cambios con observaciones
    b172195 — feat(usuarios): paginación 15 registros por página
    6188480 — feat(usuarios): matriz de roles en manual del sistema
    88d74b4 — test(usuarios): verificación Fase 6 completada

Incidencias: 11 detectadas, 11 corregidas
Solicitudes de cambio: 7 implementadas
Pendientes Fase 5 resueltos: Matriz de Roles 3.4
Transversales: Búsqueda ✅ | Breadcrumbs ✅ | Paginación ✅
```

---

## Módulo: `productos` — ✅ Aprobado

### Capas verificadas

| Capa | Estado | Observaciones |
|---|---|---|
| 1 — Modelo | ✅ Verificada | Auditoría `creado_por`/`modificado_por`/`modificado_en` + modelo `HistorialStock` + `MinValueValidator` |
| 2 — Formulario | ✅ Verificada | `es_edicion` oculta `stock` en edición, labels con tildes, validación `precio_venta >= precio_compra` |
| 3 — Vistas | ✅ Verificada | `@require_POST`, auditoría, búsqueda Q, paginación, breadcrumbs, `HistorialStock` en modificar_stock |
| 4 — Templates | ✅ Verificada | POST modal estado, `aria-label`, `scope="col"`, badges con ícono, `get_categoria_display`, `linebreaksbr`, búsqueda, paginación, breadcrumbs |
| 5 — Integración | ✅ Verificada | I-01 sidebar ✅ I-02 links ✅ I-03 datos coherentes ✅ I-04 dashboard contadores reales ✅ |

### Incidencias detectadas y corregidas

| Código | Severidad | Descripción | Commit | Estado |
|---|---|---|---|---|
| INC-P01 | **Alta** | `cambiar_estado_producto` acepta GET — riesgo CSRF | `2330617` | ✅ Corregido |
| INC-P02 | Media | `stock` editable sin control en `ProductoForm` al editar | `17642e8` | ✅ Corregido |
| INC-P03 | Media | Sin validación `precio_venta >= precio_compra` | `17642e8` | ✅ Corregido |
| INC-P04 | Media | Sin auditoría `creado_por`/`modificado_por` | `06d9463` + `0ea2c06` | ✅ Corregido |
| INC-P05 | Media | Sin paginación en lista | `0ea2c06` | ✅ Corregido |
| INC-P06 | Media | Sin búsqueda/filtro en lista | `0ea2c06` | ✅ Corregido |
| INC-P07 | Media | Sin breadcrumbs en los 4 templates | `0ea2c06` + `64ee9fc` | ✅ Corregido |
| INC-P08 | Media | Sin `aria-label` en botones de tabla — WCAG 4.1.2 | `920f7db` | ✅ Corregido |
| INC-P09 | Media | `{{ producto.categoria }}` muestra valor interno | `920f7db` + `df51f38` | ✅ Corregido |
| INC-P10 | Media | `observaciones` sin `\|linebreaksbr` | `df51f38` | ✅ Corregido |
| INC-P11 | Media | Sin auditoría en `cambiar_estado_producto` | `2330617` | ✅ Corregido |
| INC-P12 | Baja | Sin `scope="col"` en `<th>` — WCAG 1.3.1 | `920f7db` | ✅ Corregido |
| INC-P13 | Baja | Badges de estado sin ícono — WCAG 1.4.1 | `920f7db` | ✅ Corregido |
| INC-P14 | Baja | Sin `fecha_modificacion` en modelo | `06d9463` | ✅ Corregido |
| INC-P15 | Baja | Sin `MinValueValidator` a nivel modelo | `06d9463` | ✅ Corregido |
| INC-P16 | Baja | `admin_requerido` redirige sin mensaje | `7704fb0` | ✅ Corregido |
| INC-P17 | Baja | Labels sin tildes en formulario | `17642e8` | ✅ Corregido |
| INC-P18 | Baja | Historial de stock en campo `observaciones` (texto plano) | `06d9463` + `0ea2c06` | ✅ Corregido |
| INC-P19 | Media | `{% include 'partials/breadcrumbs.html' %}` inexistente en templates | `aab9017` | ✅ Corregido (verificación) |
| INC-P20 | Media | `AttributeError` en editar — `form.stock` popeado rompe `with_aria_required` | `aab9017` | ✅ Corregido (verificación) |
| INC-P21 | Baja | Botón toggle sin `title` — sin tooltip al hover | `51058f0` | ✅ Corregido (verificación) |

### Solicitudes de cambio

| Código | Tipo | Descripción | Commit | Estado |
|---|---|---|---|---|
| SC-P01 | Agregar | Modelo `HistorialStock` dedicado | `06d9463` | ✅ Implementado |
| SC-P02 | Agregar | Auditoría `creado_por`/`modificado_por`/`modificado_en` en `Producto` | `06d9463` | ✅ Implementado |
| SC-P03 | Agregar | Breadcrumbs en 6 vistas | `0ea2c06` + `64ee9fc` | ✅ Implementado |
| SC-P04 | Agregar | Búsqueda en tiempo real con debounce (reutiliza `busqueda.js`) | `0ea2c06` + `920f7db` | ✅ Implementado |
| SC-P05 | Agregar | Paginación 15 registros por página | `0ea2c06` + `920f7db` | ✅ Implementado |
| SC-P06 | Agregar | Modal confirmación con observación obligatoria para cambiar estado | `920f7db` | ✅ Implementado |
| SC-P07 | Agregar | Historial de stock en vista de detalle | `0ea2c06` + `df51f38` | ✅ Implementado |
| SC-P08 | Agregar | `'PRODUCTO'` en `HistorialCambio.MODELO_CHOICES` | `d46398a` | ✅ Implementado |

### Decisiones tomadas en módulo `productos`

| Decisión | Justificación |
|---|---|
| `HistorialStock` como modelo dedicado (no texto en `observaciones`) | Consistente con `HistorialCambio` de usuarios; datos consultables y estructurados |
| `stock` solo editable en formulario de creación | En edición se gestiona via `modificar_stock` para mantener trazabilidad obligatoria con motivo |
| `HistorialCambio` reutilizado para cambios de estado de productos | DRY — misma tabla con `modelo='PRODUCTO'`; evita nueva migración |
| `MinValueValidator` en modelo y en formulario | Doble validación: modelo protege el ORM directo, formulario da mensajes de usuario |
| Tooltip del modal via `title` nativo (no `data-bs-toggle="tooltip"`) | El botón ya usa `data-bs-toggle="modal"`; Bootstrap no permite dos triggers en el mismo atributo |

### Nuevas dependencias instaladas

Ninguna — se reutilizaron `openpyxl`, `django-csp` y `pillow` ya instalados en módulo `usuarios`.

### Nuevos archivos y migraciones

| Archivo | Descripción |
|---|---|
| `apps/productos/migrations/0002_auditoria_historialstock_validadores.py` | Campos de auditoría + modelo `HistorialStock` + validadores |

---

## Resumen de commits — módulo `productos`

| Hash | Descripción | Fecha |
|---|---|---|
| `d46398a` | feat(usuarios): agregar PRODUCTO a HistorialCambio.MODELO_CHOICES | 2026-05-29 |
| `06d9463` | feat(productos): auditoria creado_por/modificado_por, HistorialStock y validadores | 2026-05-29 |
| `17642e8` | fix(productos): validaciones formulario y control de stock en edicion | 2026-05-29 |
| `2330617` | fix(productos): cambiar_estado requiere POST y observacion obligatoria — previene CSRF | 2026-05-29 |
| `0ea2c06` | feat(productos): auditoria, HistorialStock, paginacion, busqueda y breadcrumbs en vistas | 2026-05-29 |
| `7704fb0` | fix(usuarios): mensaje de acceso denegado en admin_requerido | 2026-05-29 |
| `920f7db` | fix(productos): POST estado, aria-label, scope, badges icono, busqueda y paginacion | 2026-05-29 |
| `df51f38` | fix(productos): detalle con get_categoria_display, linebreaksbr, historial stock y auditoria | 2026-05-29 |
| `64ee9fc` | fix(productos): breadcrumbs en formularios y auditoria en admin | 2026-05-29 |
| `aab9017` | fix(productos): eliminar include breadcrumbs inexistente y condicionar campo stock en edicion | 2026-05-29 |
| `51058f0` | fix(productos): tooltip title en boton toggle activar/desactivar | 2026-05-29 |

---

## Resumen de cierre — `productos`

```
## Módulo: productos — APROBADO ✅

- Fecha de inicio de revisión: 2026-05-29
- Fecha de aprobación: 2026-05-29
- Commits del módulo:
    d46398a — feat(usuarios): PRODUCTO en HistorialCambio.MODELO_CHOICES
    06d9463 — feat(productos): auditoria, HistorialStock y validadores
    17642e8 — fix(productos): validaciones formulario y control stock en edicion
    2330617 — fix(productos): cambiar_estado requiere POST — previene CSRF
    0ea2c06 — feat(productos): auditoria, HistorialStock, paginacion, busqueda, breadcrumbs
    7704fb0 — fix(usuarios): mensaje acceso denegado en admin_requerido
    920f7db — fix(productos): POST estado, aria-label, scope, badges, busqueda, paginacion
    df51f38 — fix(productos): detalle — get_categoria_display, linebreaksbr, historial, auditoria
    64ee9fc — fix(productos): breadcrumbs en formularios y auditoria en admin
    aab9017 — fix(productos): breadcrumbs inexistente y stock condicional en edicion
    51058f0 — fix(productos): tooltip title en boton toggle

Incidencias: 21 detectadas, 21 corregidas (18 en análisis + 3 en verificación)
Solicitudes de cambio: 8 implementadas
Pendientes Fase 5 resueltos: N/A
Transversales: Búsqueda ✅ | Breadcrumbs ✅ | Paginación ✅
```

---

## Módulo: `insumos` — ✅ Aprobado

### Capas verificadas

| Capa | Estado | Observaciones |
|---|---|---|
| 1 — Modelo | ✅ Verificada | Auditoría `creado_por`/`modificado_por`/`modificado_en` + modelo `HistorialStockInsumo` + `MinValueValidator` |
| 2 — Formulario | ✅ Verificada | `es_edicion` oculta `stock` en edición, queryset solo proveedores activos, labels con tildes |
| 3 — Vistas | ✅ Verificada | `@require_POST`, auditoría, búsqueda Q (código/nombre/subcategoría/proveedor), paginación, breadcrumbs, `HistorialStockInsumo` |
| 4 — Templates | ✅ Verificada | POST modal estado, `aria-label`, `scope="col"`, badges con ícono, `get_subcategoria_display`, `linebreaksbr`, búsqueda, paginación, breadcrumbs |
| 5 — Integración | ✅ Verificada | I-01 sidebar ✅ I-03 FK Proveedor con PROTECT ✅ I-04 dashboard contadores y alertas reales ✅ |

### Incidencias detectadas y corregidas

| Código | Severidad | Descripción | Commit | Estado |
|---|---|---|---|---|
| INC-I01 | **Alta** | `cambiar_estado_insumo` acepta GET — riesgo CSRF | `91a645d` | ✅ Corregido |
| INC-I02 | Media | `stock` editable sin control en `InsumoForm` al editar | `fab1bed` | ✅ Corregido |
| INC-I03 | Media | `proveedor` queryset muestra proveedores INACTIVOS | `fab1bed` | ✅ Corregido |
| INC-I04 | Media | Sin auditoría `creado_por`/`modificado_por` | `a4e8087` + `60bb19a` | ✅ Corregido |
| INC-I05 | Media | Sin paginación en lista | `60bb19a` | ✅ Corregido |
| INC-I06 | Media | Sin búsqueda/filtro en lista | `60bb19a` | ✅ Corregido |
| INC-I07 | Media | Sin breadcrumbs en 6 vistas | `60bb19a` | ✅ Corregido |
| INC-I08 | Media | Sin `aria-label` en botones de tabla — WCAG 4.1.2 | `9fb4653` | ✅ Corregido |
| INC-I09 | Media | `{{ insumo.subcategoria }}` sin `get_subcategoria_display` | `9fb4653` + `38f54c4` | ✅ Corregido |
| INC-I10 | Media | `{{ insumo.observaciones }}` sin `\|linebreaksbr` | `38f54c4` | ✅ Corregido |
| INC-I11 | Media | Sin auditoría en `cambiar_estado_insumo` | `91a645d` | ✅ Corregido |
| INC-I12 | Media | `modificar_stock_insumo` escribe en `observaciones` (no estructurado) | `a4e8087` + `60bb19a` | ✅ Corregido |
| INC-I13 | Media | `HistorialCambio.MODELO_CHOICES` sin `'INSUMO'` | `990adde` | ✅ Corregido |
| INC-I14 | Baja | Sin `scope="col"` en `<th>` — WCAG 1.3.1 | `9fb4653` | ✅ Corregido |
| INC-I15 | Baja | Badges de estado sin ícono — WCAG 1.4.1 | `9fb4653` | ✅ Corregido |
| INC-I16 | Baja | Sin `MinValueValidator` a nivel modelo | `a4e8087` | ✅ Corregido |
| INC-I17 | Baja | Labels sin tildes en formulario | `fab1bed` | ✅ Corregido |
| INC-I18 | Baja | Historial de stock en `observaciones` (texto plano) | `a4e8087` + `60bb19a` | ✅ Corregido |

### Solicitudes de cambio

| Código | Tipo | Descripción | Commit | Estado |
|---|---|---|---|---|
| SC-I01 | Agregar | Modelo `HistorialStockInsumo` dedicado | `a4e8087` | ✅ Implementado |
| SC-I02 | Agregar | Auditoría `creado_por`/`modificado_por`/`modificado_en` en `Insumo` | `a4e8087` | ✅ Implementado |
| SC-I03 | Agregar | Queryset solo proveedores activos en `InsumoForm` | `fab1bed` | ✅ Implementado |
| SC-I04 | Agregar | Breadcrumbs en 6 vistas | `60bb19a` | ✅ Implementado |
| SC-I05 | Agregar | Búsqueda en tiempo real (código/nombre/subcategoría/proveedor) | `60bb19a` + `9fb4653` | ✅ Implementado |
| SC-I06 | Agregar | Paginación 15 registros por página | `60bb19a` + `9fb4653` | ✅ Implementado |
| SC-I07 | Agregar | Modal confirmación con observación obligatoria | `9fb4653` | ✅ Implementado |
| SC-I08 | Agregar | Historial de stock en vista de detalle | `60bb19a` + `38f54c4` | ✅ Implementado |
| SC-I09 | Agregar | `'INSUMO'` en `HistorialCambio.MODELO_CHOICES` | `990adde` | ✅ Implementado |
| SC-I10 | Agregar | Manual del sistema — sección Productos e Insumos + matriz de roles | `405a2b9` | ✅ Implementado |

### Decisiones tomadas en módulo `insumos`

| Decisión | Justificación |
|---|---|
| `HistorialStockInsumo` como modelo independiente (no reutilizar `HistorialStock` de productos) | Módulos independientes; evita acoplamiento entre apps |
| Queryset de `proveedor` filtrado a `estado='ACTIVO'` | Un insumo no debe asignarse a un proveedor inactivo |
| Búsqueda incluye `proveedor__razon_social` y `proveedor__nombres` | Permite buscar por proveedor tanto empresas (NIT) como personas naturales |
| `HistorialCambio` reutilizado para cambios de estado (modelo `'INSUMO'`) | DRY — misma infraestructura que usuarios y productos |

### Nuevas dependencias instaladas

Ninguna — reutilización completa del stack ya instalado.

### Nuevos archivos y migraciones

| Archivo | Descripción |
|---|---|
| `apps/insumos/migrations/0002_auditoria_historialstockinsumo_validadores.py` | Campos de auditoría + modelo `HistorialStockInsumo` + validadores |

---

## Resumen de commits — módulo `insumos`

| Hash | Descripción | Fecha |
|---|---|---|
| `990adde` | feat(usuarios): agregar INSUMO a HistorialCambio.MODELO_CHOICES | 2026-05-29 |
| `a4e8087` | feat(insumos): auditoria, HistorialStockInsumo y validadores | 2026-05-29 |
| `fab1bed` | fix(insumos): InsumoForm — es_edicion, queryset activos y labels | 2026-05-29 |
| `91a645d` | fix(insumos): cambiar_estado requiere POST — previene CSRF | 2026-05-29 |
| `60bb19a` | feat(insumos): auditoria, HistorialStockInsumo, paginacion, busqueda, breadcrumbs | 2026-05-29 |
| `9fb4653` | fix(insumos): POST estado, aria-label, scope, badges, busqueda y paginacion | 2026-05-29 |
| `38f54c4` | fix(insumos): detalle con get_subcategoria_display, linebreaksbr, historial y auditoria | 2026-05-29 |
| `143d870` | fix(insumos): stock condicional en formulario de edicion | 2026-05-29 |
| `3b5fe7b` | fix(insumos): auditoria en admin y registro HistorialStockInsumo | 2026-05-29 |
| `405a2b9` | feat(manual): matriz de roles y descripcion completa de productos e insumos | 2026-05-29 |

---

## Resumen de cierre — `insumos`

```
## Módulo: insumos — APROBADO ✅

- Fecha de inicio de revisión: 2026-05-29
- Fecha de aprobación: 2026-05-29
- Commits del módulo:
    990adde — feat(usuarios): INSUMO en HistorialCambio.MODELO_CHOICES
    a4e8087 — feat(insumos): auditoria, HistorialStockInsumo y validadores
    fab1bed — fix(insumos): InsumoForm — es_edicion, queryset activos y labels
    91a645d — fix(insumos): cambiar_estado requiere POST — previene CSRF
    60bb19a — feat(insumos): auditoria, HistorialStockInsumo, paginacion, busqueda, breadcrumbs
    9fb4653 — fix(insumos): POST estado, aria-label, scope, badges, busqueda y paginacion
    38f54c4 — fix(insumos): detalle — get_subcategoria_display, linebreaksbr, historial
    143d870 — fix(insumos): stock condicional en formulario de edicion
    3b5fe7b — fix(insumos): auditoria en admin y registro HistorialStockInsumo
    405a2b9 — feat(manual): productos e insumos en manual del sistema

Incidencias: 18 detectadas, 18 corregidas — 0 bugs en verificación
Solicitudes de cambio: 10 implementadas
Pendientes Fase 5 resueltos: N/A
Transversales: Búsqueda ✅ | Breadcrumbs ✅ | Paginación ✅
```

---

---

## Módulo: `compras` — ✅ Aprobado

### Capas verificadas

| Capa | Estado | Observaciones |
|---|---|---|
| 1 — Modelo | ✅ Verificada | `HistorialCambio` con `'COMPRA'`, sin migración requerida |
| 2 — Formulario | ✅ Verificada | Queryset proveedores activos, labels con tildes, validación monetaria existente |
| 3 — Vistas | ✅ Verificada | `@require_POST`, reversión de stock al desactivar (Pendiente Fase 5 resuelto), `HistorialCambio`, paginación, búsqueda, breadcrumbs |
| 4 — Templates | ✅ Verificada | POST modal estado, sin `onclick` inline (CSP), sin mensajes duplicados, `get_tipo_item_display`, `linebreaksbr`, `scope="col"`, badges con ícono, exportar Excel |
| 5 — Integración | ✅ Verificada | I-01 sidebar ✅ I-02 stock actualizado por `DetalleCompra.save()` ✅ I-03 FK Proveedor PROTECT ✅ I-04 dashboard últimas compras ✅ |

### Incidencias detectadas y corregidas

| Código | Severidad | Descripción | Commit | Estado |
|---|---|---|---|---|
| INC-C01 | **Alta** | `cambiar_estado_compra` acepta GET — CSRF | `9fa2349` | ✅ Corregido |
| INC-C02 | **Alta** | `onclick="eliminarFila(this)"` — viola CSP activa | `8e77213` | ✅ Corregido |
| INC-C03 | **Alta** | `<a href>` toggle en `detalle_compra.html` — GET | `3665d42` | ✅ Corregido |
| INC-C04 | Media | `HistorialCambio.MODELO_CHOICES` sin `'COMPRA'` | `0073de1` | ✅ Corregido |
| INC-C05 | Media | Sin observación obligatoria en cambiar estado | `9fa2349` | ✅ Corregido |
| INC-C06 | Media | Sin reversión de stock al desactivar (Pendiente Fase 5) | `d58430b` | ✅ Corregido |
| INC-C07 | Media | Sin `HistorialCambio` al cambiar estado | `d58430b` | ✅ Corregido |
| INC-C08 | Media | Sin paginación en lista | `d58430b` | ✅ Corregido |
| INC-C09 | Media | Sin búsqueda en lista | `d58430b` | ✅ Corregido |
| INC-C10 | Media | Sin breadcrumbs en 3 vistas | `d58430b` | ✅ Corregido |
| INC-C11 | Media | Mensajes flash duplicados en lista y form | `0fc6f27` + `8f255aa` | ✅ Corregido |
| INC-C12 | Media | Sin `aria-label` en botones — WCAG 4.1.2 | `0fc6f27` | ✅ Corregido |
| INC-C13 | Media | `get_tipo_item_display` no usado | `3665d42` | ✅ Corregido |
| INC-C14 | Media | `{{ compra.observaciones }}` sin `\|linebreaksbr` | `3665d42` | ✅ Corregido |
| INC-C15 | Media | `proveedor` queryset sin filtrar | `ce1b55c` | ✅ Corregido |
| INC-C16 | Baja | Sin `scope="col"` en `<th>` — WCAG 1.3.1 | `0fc6f27` + `3665d42` | ✅ Corregido |
| INC-C17 | Baja | Badges de estado sin ícono — WCAG 1.4.1 | `0fc6f27` + `3665d42` | ✅ Corregido |
| INC-C18 | Baja | Estilo inline en `detalle_compra.html` | `e4cdbb8` | ✅ Corregido (verificación) |
| INC-C19 | Baja | Labels sin tildes en formulario | `ce1b55c` | ✅ Corregido |

### Solicitudes de cambio

| Código | Tipo | Descripción | Commit | Estado |
|---|---|---|---|---|
| SC-C01 | Agregar | Reversión de stock al desactivar (Pendiente Fase 5) | `d58430b` | ✅ Implementado |
| SC-C02 | Agregar | Event delegation para `.btn-eliminar-item` (CSP) | `8e77213` | ✅ Implementado |
| SC-C03 | Agregar | Paginación + búsqueda + breadcrumbs | `d58430b` | ✅ Implementado |
| SC-C04 | Agregar | Modal confirmación con observación obligatoria | `0fc6f27` + `3665d42` | ✅ Implementado |
| SC-C05 | Agregar | Exportación Excel de facturas de compra | `af023f5` | ✅ Implementado |
| SC-C06 | Diferido | PDF de factura de compra | — | ⏳ Diferido a Ventas |

### Decisiones tomadas en módulo `compras`

| Decisión | Justificación |
|---|---|
| Reversión de stock con `max(0, stock - cantidad)` | Evita stock negativo si el stock fue modificado después de la compra |
| Reactivación restaura stock (`stock + cantidad`) | Simetría con la desactivación |
| `HistorialStock`/`HistorialStockInsumo` creados en la reversión | Trazabilidad completa de cada movimiento de stock |
| PDF diferido | Se implementará junto con ventas para consistencia de layout |
| Event delegation en JS en vez de `onclick` | CSP bloquea `script-src 'unsafe-inline'`; event delegation es el patrón correcto |

---

## Resumen de commits — módulo `compras`

| Hash | Descripción | Fecha |
|---|---|---|
| `0073de1` | feat(usuarios): agregar COMPRA a HistorialCambio.MODELO_CHOICES | 2026-05-29 |
| `8e77213` | fix(compras): event delegation btn-eliminar-item — previene violacion CSP | 2026-05-29 |
| `ce1b55c` | fix(compras): FacturaCompraForm — queryset proveedores activos y labels | 2026-05-29 |
| `9fa2349` | fix(compras): cambiar_estado requiere POST — previene CSRF | 2026-05-29 |
| `d58430b` | feat(compras): reversion stock, HistorialCambio, paginacion, busqueda, breadcrumbs | 2026-05-29 |
| `0fc6f27` | fix(compras): lista — POST estado, aria-label, scope, badges, busqueda, paginacion | 2026-05-29 |
| `3665d42` | fix(compras): detalle — modal estado, tipo_item display, linebreaksbr, scope, badges | 2026-05-29 |
| `8f255aa` | fix(compras): form — eliminar mensajes duplicados y atributo onclick | 2026-05-29 |
| `1f053f6` | feat(productos): exportacion Excel de productos | 2026-05-29 |
| `44c2ac9` | feat(insumos): exportacion Excel de insumos | 2026-05-29 |
| `af023f5` | feat(compras): exportacion Excel de facturas de compra | 2026-05-29 |
| `e4cdbb8` | fix(compras): eliminar style inline en boton toggle del detalle | 2026-05-29 |

---

## Resumen de cierre — `compras`

```
## Módulo: compras — APROBADO ✅

- Fecha de inicio de revisión: 2026-05-29
- Fecha de aprobación: 2026-05-29
- Commits del módulo:
    0073de1 — feat(usuarios): COMPRA en HistorialCambio.MODELO_CHOICES
    8e77213 — fix(compras): event delegation btn-eliminar-item — CSP
    ce1b55c — fix(compras): FacturaCompraForm — queryset activos y labels
    9fa2349 — fix(compras): cambiar_estado requiere POST — previene CSRF
    d58430b — feat(compras): reversion stock, HistorialCambio, paginacion, busqueda
    0fc6f27 — fix(compras): lista completa
    3665d42 — fix(compras): detalle completo
    8f255aa — fix(compras): form limpiado
    1f053f6 — feat(productos): exportacion Excel
    44c2ac9 — feat(insumos): exportacion Excel
    af023f5 — feat(compras): exportacion Excel
    e4cdbb8 — fix(compras): style inline eliminado

Incidencias: 19 detectadas, 19 corregidas (18 análisis + 1 verificación)
Solicitudes de cambio: 5 implementadas, 1 diferida (PDF)
Pendientes Fase 5 resueltos: Reversión de stock al desactivar ✅
Transversales: Búsqueda ✅ | Breadcrumbs ✅ | Paginación ✅ | Excel ✅
```

---

---

## Módulo: `ventas` — ✅ Aprobado

### Capas verificadas

| Capa | Estado | Observaciones |
|---|---|---|
| 1 — Modelo | ✅ Verificada | `HistorialCambio` con `'VENTA'`, sin migración requerida |
| 2 — Formulario | ✅ Verificada | Queryset clientes activos, labels con tildes, validación monetaria existente |
| 3 — Vistas | ✅ Verificada | `@require_POST`, restauración de stock al desactivar, validación de stock al reactivar (Pendiente Fase 5 resuelto), `HistorialCambio`, paginación, búsqueda, breadcrumbs, exportar Excel |
| 4 — Templates | ✅ Verificada | POST modal estado, sin `onclick` (CSP), sin mensajes duplicados, `get_tipo_item_display`, `get_metodo_pago_display`, `linebreaksbr`, `scope="col"`, badges con ícono, botón detalle con `btn-accion` |
| 5 — Integración | ✅ Verificada | I-01 sidebar ✅ I-02 stock descontado por `DetalleVenta.save()` con validación ✅ I-04 dashboard ventas del mes ✅ |

### Incidencias detectadas y corregidas

| Código | Severidad | Descripción | Commit | Estado |
|---|---|---|---|---|
| INC-V01 | **Alta** | `cambiar_estado_venta` acepta GET — CSRF | `2f254de` | ✅ Corregido |
| INC-V02 | **Alta** | `onclick="eliminarFila(this)"` — viola CSP | `a3ca513` | ✅ Corregido |
| INC-V03 | **Alta** | `<a href>` toggle en `detalle_venta.html` — GET | `a3b0f62` | ✅ Corregido |
| INC-V04 | Media | `HistorialCambio.MODELO_CHOICES` sin `'VENTA'` | `63c2323` | ✅ Corregido |
| INC-V05 | Media | Sin observación obligatoria en cambiar estado | `2f254de` | ✅ Corregido |
| INC-V06 | Media | Sin restauración de stock al desactivar (Pendiente Fase 5) | `493fa7a` | ✅ Corregido |
| INC-V07 | Media | Sin validación de stock al reactivar | `493fa7a` | ✅ Corregido |
| INC-V08 | Media | Sin `HistorialCambio` al cambiar estado | `2f254de` | ✅ Corregido |
| INC-V09 | Media | Sin paginación | `493fa7a` | ✅ Corregido |
| INC-V10 | Media | Sin búsqueda | `493fa7a` | ✅ Corregido |
| INC-V11 | Media | Sin breadcrumbs | `493fa7a` | ✅ Corregido |
| INC-V12 | Media | Mensajes duplicados en lista y form | `1e2012e` + `a3ca513` | ✅ Corregido |
| INC-V13 | Media | Sin `aria-label` en botones — WCAG 4.1.2 | `1e2012e` | ✅ Corregido |
| INC-V14 | Media | `get_tipo_item_display` no usado | `a3b0f62` | ✅ Corregido |
| INC-V15 | Media | `get_metodo_pago_display` no usado | `1e2012e` + `a3b0f62` | ✅ Corregido |
| INC-V16 | Media | `{{ venta.observaciones }}` sin `\|linebreaksbr` | `a3b0f62` | ✅ Corregido |
| INC-V17 | Media | `cliente` queryset sin filtrar | `3c1c777` | ✅ Corregido |
| INC-V18 | Baja | Sin `scope="col"` en `<th>` — WCAG 1.3.1 | `1e2012e` + `a3b0f62` | ✅ Corregido |
| INC-V19 | Baja | Badges de estado sin ícono — WCAG 1.4.1 | `1e2012e` + `a3b0f62` | ✅ Corregido |
| INC-V20 | Baja | Estilo inline + `btn-tabla` para botón con texto en detalle | `be50530` | ✅ Corregido (verificación) |

### Solicitudes de cambio

| Código | Tipo | Descripción | Commit | Estado |
|---|---|---|---|---|
| SC-V01 | Agregar | Restauración de stock al desactivar + validación al reactivar (Pendiente Fase 5) | `493fa7a` | ✅ Implementado |
| SC-V02 | Agregar | Paginación + búsqueda + breadcrumbs | `493fa7a` | ✅ Implementado |
| SC-V03 | Agregar | Modal confirmación con observación obligatoria | `1e2012e` + `a3b0f62` | ✅ Implementado |
| SC-V04 | Agregar | Exportación Excel de facturas de venta | `493fa7a` | ✅ Implementado |
| SC-V05 | Diferido | PDF de factura de venta | — | ⏳ Diferido (junto con compras) |

### Decisiones tomadas en módulo `ventas`

| Decisión | Justificación |
|---|---|
| Validación de stock ANTES de la transacción al reactivar | Evita partial-update: si falla la validación, no se modifica nada en BD |
| `max(0, stock + cantidad)` al restaurar (desactivar) | Por simetría con compras; evita stock negativo en casos extremos |
| `btn-accion` / `btn-secundario` en botón del detalle | `btn-tabla` es para íconos pequeños; el detalle muestra texto + ícono |
| PDF diferido junto con compras | Implementar los dos juntos para consistencia de layout |

---

## Resumen de commits — módulo `ventas`

| Hash | Descripción | Fecha |
|---|---|---|
| `63c2323` | feat(usuarios): agregar VENTA a HistorialCambio.MODELO_CHOICES | 2026-05-29 |
| `3c1c777` | fix(ventas): FacturaVentaForm — queryset clientes activos y labels | 2026-05-29 |
| `2f254de` | fix(ventas): cambiar_estado requiere POST — previene CSRF | 2026-05-29 |
| `493fa7a` | feat(ventas): reversion stock con validacion, HistorialCambio, paginacion, busqueda, breadcrumbs y Excel | 2026-05-29 |
| `1e2012e` | fix(ventas): lista completa | 2026-05-29 |
| `a3b0f62` | fix(ventas): detalle completo | 2026-05-29 |
| `a3ca513` | fix(ventas): form — mensajes duplicados y onclick | 2026-05-29 |
| `be50530` | fix(ventas,compras): boton activar/desactivar en detalle usa btn-accion/btn-secundario | 2026-05-29 |

---

## Resumen de cierre — `ventas`

```
## Módulo: ventas — APROBADO ✅

- Fecha de inicio de revisión: 2026-05-29
- Fecha de aprobación: 2026-05-29
- Commits del módulo: (ver tabla de commits arriba)

Incidencias: 20 detectadas, 20 corregidas (19 análisis + 1 verificación)
Solicitudes de cambio: 4 implementadas, 1 diferida (PDF)
Pendientes Fase 5 resueltos: Restauración stock al desactivar + validación al reactivar ✅
Transversales: Búsqueda ✅ | Breadcrumbs ✅ | Paginación ✅ | Excel ✅
```

---

*Bitácora actualizada el 29 de mayo de 2026 — módulo ventas.*
