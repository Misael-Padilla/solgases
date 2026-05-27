# SOLGASES — Contexto Fase 6 (Para retomar conversación)

> **Última actualización:** 26 de mayo de 2026
> **Rama:** `main`
> **Último commit:** *(ver abajo)*

---

## Estado general

- **Fase actual:** 6 — Pruebas y Verificación
- **Módulo en progreso:** `usuarios` (siguiente)
- **Protocolo activo:** Protocolo de Veracidad — Fase 6 v1.1

---

## Módulos aprobados

| Módulo | Fecha aprobación | Commits |
|---|---|---|
| `core` | 2026-05-26 | `0604f36`, `d1e6771`, `429bd50`, commit cierre |

## Módulos pendientes (en orden)

1. `usuarios` — autenticación, roles, decoradores + Matriz de Roles 3.4
2. `productos`
3. `insumos`
4. `compras` — edición limitada, inactivación con reversión de stock, notificación ADMIN
5. `ventas` — ídem compras
6. `backup` — APScheduler

---

## Módulo siguiente: `usuarios`

**Pendientes de Fase 5 asignados:**
- Matriz de Roles 3.4 (documento formal — no código)

**Transversales a implementar:**
- Search/filters/pagination en: lista de usuarios, lista de clientes, lista de proveedores
- Breadcrumbs en todos los templates del módulo

**Archivos clave a revisar:**
- `apps/usuarios/models.py`
- `apps/usuarios/forms.py`
- `apps/usuarios/views.py`
- `apps/usuarios/urls.py`
- `templates/usuarios/`

---

## Decisiones de arquitectura vigentes

| Decisión | Detalle |
|---|---|
| `AXES_LOCKOUT_PARAMETERS = ['username']` | Sin ip_address — sistema interno, decisión consciente |
| Email dual | Consola (dev) con ConsoleEmailBackend legible / Gmail SMTP (prod) vía .env |
| `AUTH_USER_MODEL = 'usuarios.Usuario'` | Campo `estado='ACTIVO'` en vez de `is_active` |
| `USERNAME_FIELD = EMAIL_FIELD = 'correo_electronico'` | Login por correo, no por username |

---

## Archivos que la IA necesita para revisar `usuarios`

Pedir al desarrollador que comparta o que la IA lea directamente:
- `apps/usuarios/models.py`
- `apps/usuarios/forms.py`
- `apps/usuarios/views.py`
- `apps/usuarios/urls.py`
- `templates/usuarios/` (todos los templates)
- `apps/core/views.py` (decoradores: `@login_requerido`, `@admin_requerido`)

---

## Reglas clave del protocolo (recordatorio)

- **F6-04:** Ningún código sin autorización explícita
- **F6-05:** Explicar error + solución → esperar autorización → corregir
- **F6-03:** Solo "Módulo X APROBADO" explícito cierra un módulo
- **Commits:** Alta/SC individual + push inmediato. Media/Baja agrupadas en commit cierre.
- **Formato commit cierre:** `test(módulo): verificación Fase 6 completada`

---

*Documento generado al cierre del módulo `core` — 26 de mayo de 2026.*
