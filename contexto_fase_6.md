# SOLGASES — Contexto Fase 6 (Para retomar conversación)

> **Última actualización:** 29 de mayo de 2026
> **Rama:** `main`
> **Último commit:** `cierre-insumos` (se actualiza tras el commit de cierre)

---

## Estado general

- **Fase actual:** 6 — Pruebas y Verificación
- **Módulo en progreso:** `compras` (siguiente)
- **Protocolo activo:** Protocolo de Veracidad — Fase 6 v1.1

---

## Módulos

| Módulo | Estado | Commits clave |
|--------|--------|---------------|
| `core` | ✅ Aprobado — 2026-05-26 | `39bfcc5` (cierre) |
| `usuarios` | ✅ Aprobado — 2026-05-29 | `88d74b4` (cierre) |
| `productos` | ✅ Aprobado — 2026-05-29 | `9295480` (cierre) |
| `insumos` | ✅ Aprobado — 2026-05-29 | `cierre-insumos` (cierre) |
| `compras` | ⏳ Pendiente | — |
| `ventas` | ⏳ Pendiente | — |
| `backup` | ⏳ Pendiente | — |

---

## Módulo `insumos` — resumen de lo hecho

- Modelo `HistorialStockInsumo` dedicado
- Auditoría `creado_por`/`modificado_por`/`modificado_en` en `Insumo`
- `MinValueValidator` en stock y precio a nivel modelo
- `InsumoForm` con `es_edicion`: oculta `stock` al editar
- Queryset de `proveedor` filtrado solo a activos
- `@require_POST` + observación obligatoria en `cambiar_estado_insumo`
- Búsqueda por código/nombre/subcategoría/proveedor + paginación 15 registros
- Breadcrumbs en las 6 vistas
- Modal confirmación (reutiliza `modal_estado.js`)
- `get_subcategoria_display` en lista y detalle
- Historial de stock en vista de detalle
- `'INSUMO'` agregado a `HistorialCambio.MODELO_CHOICES`
- Manual del sistema: sección Productos e Insumos expandida + matriz de roles

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
| `HistorialStock` / `HistorialStockInsumo` como modelos dedicados | Datos consultables; cada módulo tiene su propio modelo |
| `stock` solo editable en creación (no en edición) | Edición de stock via modificar_stock con motivo obligatorio |
| Tooltip del modal toggle via `title` nativo | `data-bs-toggle` ya usado por modal |
| `MinValueValidator` en modelo Y en formulario | Modelo protege ORM directo; formulario da mensajes de usuario |
| Queryset `proveedor` filtrado a activos en `InsumoForm` | Un insumo no debe asignarse a un proveedor inactivo |
| `HistorialStockInsumo` independiente de `HistorialStock` | Módulos desacoplados; evita FK cruzada entre apps |

---

## Archivos JS del proyecto

| Archivo | Propósito |
|---------|-----------|
| `static/js/busqueda.js` | Búsqueda en tiempo real debounce 350ms (reutilizado en todos los módulos) |
| `static/js/modal_estado.js` | Modal confirmación activar/desactivar (reutilizado en todos los módulos) |

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
