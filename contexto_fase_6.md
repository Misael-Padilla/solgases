# SOLGASES — Contexto Fase 6 (Para retomar conversación)

> **Última actualización:** 29 de mayo de 2026
> **Rama:** `main`
> **Último commit:** `9295480`

---

## Estado general

- **Fase actual:** 6 — Pruebas y Verificación
- **Módulo en progreso:** `insumos` (siguiente)
- **Protocolo activo:** Protocolo de Veracidad — Fase 6 v1.1

---

## Módulos

| Módulo | Estado | Commits clave |
|--------|--------|---------------|
| `core` | ✅ Aprobado — 2026-05-26 | `0604f36`, `d1e6771`, `429bd50`, `39bfcc5` |
| `usuarios` | ✅ Aprobado — 2026-05-29 | `88d74b4` (cierre) |
| `productos` | ✅ Aprobado — 2026-05-29 | `9295480` (cierre) |
| `insumos` | ⏳ Pendiente | — |
| `compras` | ⏳ Pendiente | — |
| `ventas` | ⏳ Pendiente | — |
| `backup` | ⏳ Pendiente | — |

---

## Módulo `productos` — resumen de lo hecho

### Capas

| Capa | Estado |
|------|--------|
| 1 — Modelo | ✅ Verificada |
| 2 — Formulario | ✅ Verificada |
| 3 — Vistas | ✅ Verificada |
| 4 — Templates | ✅ Verificada |
| 5 — Integración | ✅ Verificada |

### Cambios principales implementados

- Modelo `HistorialStock` dedicado (reemplaza texto en `observaciones`)
- Auditoría `creado_por`/`modificado_por`/`modificado_en` en `Producto`
- `MinValueValidator` en stock y precios a nivel modelo
- `ProductoForm` con `es_edicion`: oculta `stock` al editar
- Validación `precio_venta >= precio_compra` en `clean()`
- `@require_POST` + observación obligatoria en `cambiar_estado_producto`
- Búsqueda por código/nombre/categoría + paginación 15 registros
- Breadcrumbs en las 6 vistas
- Modal confirmación (reutiliza `modal_estado.js`)
- `get_categoria_display` en lista y detalle
- Historial de stock en vista de detalle
- `'PRODUCTO'` agregado a `HistorialCambio.MODELO_CHOICES`
- Mensaje de acceso denegado en `admin_requerido` (mejora global)

---

## Decisiones técnicas vigentes (no renegociar)

| Decisión | Razón |
|----------|-------|
| `AXES_LOCKOUT_PARAMETERS = ['username']` sin ip_address | Sistema interno |
| `'unsafe-inline'` solo en `style-src`, NO en `script-src` | CSP: Bootstrap CSS lo necesita, JS no |
| **JS personalizado siempre en archivo externo** | CSP bloquea `onclick="..."` e `<script>` inline |
| `data-bs-toggle="modal"` sin onclick | Bootstrap nativo no requiere JS inline |
| PDF diferido a `ventas`/`compras` | Usar `xhtml2pdf` cuando llegue el momento |
| `openpyxl` + `zoneinfo` para Excel | Sin `pytz` — Python 3.9+ tiene `zoneinfo` nativo |
| Auditoría manual (sin `django-simple-history`) | Overkill para sistema interno |
| `HistorialCambio` para trazabilidad de estado | Observación obligatoria en activar/desactivar |
| `HistorialStock` como modelo dedicado en productos | Datos consultables; consistente con `HistorialCambio` |
| `stock` solo editable en creación (no en edición) | Edición de stock va por `modificar_stock` con motivo obligatorio |
| Tooltip del modal toggle via `title` nativo | `data-bs-toggle` ya usado por modal; no se puede duplicar |
| `MinValueValidator` en modelo Y en formulario | Modelo protege ORM directo; formulario da mensajes de usuario |

---

## Archivos JS del proyecto

| Archivo | Propósito |
|---------|-----------|
| `static/js/busqueda.js` | Búsqueda en tiempo real debounce 350ms |
| `static/js/modal_estado.js` | Modal confirmación activar/desactivar (escucha `show.bs.modal`) |

Ambos se cargan en `base.html` al final del `<body>`, después del Bootstrap bundle.
El `modal_estado.js` es reutilizable: cualquier módulo que tenga `#modal-cambiar-estado` lo usa sin cambios.

---

## Al final de la Fase 6 completa

- **SC-A01**: Widget de accesibilidad (tamaño de letra, alto contraste)

---

## Reglas activas del protocolo (NO omitir)

1. **Antes de cualquier cambio**: commit + push de lo pendiente
2. **Commits**: Conventional Commits corto — `tipo(módulo): descripción`
3. **Después de cada commit**: `git push` inmediato
4. **Investigar antes de implementar**: OWASP + WCAG
5. **Flujo**: Detectar → Explicar → Autorización → Implementar → CPs → Commit
6. **Idioma**: español
7. **Nota del usuario**: *"siga las reglas e instrucciones al pie de la letra"*

---

## Stack técnico

- Django 6.0.3 + MySQL + Bootstrap 5.3 + Bootstrap Icons 1.11
- Python 3.13.12 en Windows 11 | Entorno: `venv\`
- Servidor: `venv\Scripts\python manage.py runserver`
- Usuario: `correo_electronico` como USERNAME_FIELD, `estado='ACTIVO'`
- Decoradores: `@login_requerido`, `@admin_requerido` en `apps/usuarios/decoradores.py`
- Dependencias Fase 6: `django-axes==8.3.1`, `django-csp==4.0`, `openpyxl==3.1.5`, `pillow==12.2.0`
