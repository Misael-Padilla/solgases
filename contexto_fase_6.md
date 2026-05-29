# SOLGASES — Contexto Fase 6 (Para retomar conversación)

> **Última actualización:** 29 de mayo de 2026
> **Rama:** `main`
> **Último commit:** `cierre-compras` (se actualiza tras el commit de cierre)

---

## Estado general

- **Fase actual:** 6 — Pruebas y Verificación
- **Módulo en progreso:** `ventas` (siguiente)
- **Protocolo activo:** Protocolo de Veracidad — Fase 6 v1.1

---

## Módulos

| Módulo | Estado | Commits clave |
|--------|--------|---------------|
| `core` | ✅ Aprobado — 2026-05-26 | `39bfcc5` (cierre) |
| `usuarios` | ✅ Aprobado — 2026-05-29 | `88d74b4` (cierre) |
| `productos` | ✅ Aprobado — 2026-05-29 | `9295480` (cierre) |
| `insumos` | ✅ Aprobado — 2026-05-29 | `670218d` (cierre) |
| `compras` | ✅ Aprobado — 2026-05-29 | `cierre-compras` (cierre) |
| `ventas` | ⏳ Pendiente | — |
| `backup` | ⏳ Pendiente | — |

---

## Módulo `compras` — resumen de lo hecho

- `'COMPRA'` agregado a `HistorialCambio.MODELO_CHOICES`
- Event delegation para `.btn-eliminar-item` — corrige violación CSP
- `FacturaCompraForm`: queryset proveedores activos + labels con tildes
- `@require_POST` + observación obligatoria en `cambiar_estado_compra`
- **Reversión de stock al desactivar** (Pendiente Fase 5 resuelto): al desactivar una factura se restan las cantidades de Productos/Insumos con `HistorialStock`/`HistorialStockInsumo`; al reactivar se suman
- `HistorialCambio` registra cada cambio de estado
- Paginación 15 registros, búsqueda por N° factura/proveedor, breadcrumbs en 3 vistas
- Modal confirmación con advertencia sobre reversión de stock
- Exportación Excel de facturas (cabecera, no detalles)
- **PDF diferido junto con ventas** — usar `xhtml2pdf` cuando llegue el momento
- Exportación Excel también agregada a `productos` e `insumos`

---

## Decisiones técnicas vigentes (no renegociar)

| Decisión | Razón |
|----------|-------|
| `AXES_LOCKOUT_PARAMETERS = ['username']` sin ip_address | Sistema interno |
| `'unsafe-inline'` solo en `style-src`, NO en `script-src` | CSP: Bootstrap CSS lo necesita, JS no |
| **JS personalizado siempre en archivo externo** | CSP bloquea `onclick="..."` e `<script>` inline |
| `data-bs-toggle="modal"` sin onclick | Bootstrap nativo no requiere JS inline |
| **Event delegation para formset** (no `onclick`) | CSP bloquea inline handlers |
| PDF diferido a `ventas` | Implementar junto con ventas para consistencia |
| `openpyxl` + `zoneinfo` para Excel | Sin `pytz` — Python 3.9+ tiene `zoneinfo` nativo |
| Auditoría manual (sin `django-simple-history`) | Overkill para sistema interno |
| `HistorialCambio` para trazabilidad de estado | Observación obligatoria en activar/desactivar |
| `HistorialStock` / `HistorialStockInsumo` como modelos dedicados | Datos consultables; cada módulo tiene su propio modelo |
| `stock` solo editable en creación de productos/insumos | Edición via modificar_stock con motivo obligatorio |
| `max(0, stock - cantidad)` en reversión de compras | Evita stock negativo si el stock fue modificado después |
| Queryset `proveedor` filtrado a activos | No asignar insumos/compras a proveedores inactivos |
| Funciones Excel `_estilo_excel`, `_nombre_usuario`, etc. en `usuarios.views` | Reutilizadas via import en productos, insumos, compras |

---

## Archivos JS del proyecto

| Archivo | Propósito |
|---------|-----------|
| `static/js/busqueda.js` | Búsqueda en tiempo real debounce 350ms |
| `static/js/modal_estado.js` | Modal confirmación activar/desactivar |
| `static/js/formset_dinamico.js` | Gestión dinámica de filas de formset (compras/ventas) |
| `static/js/calculo_iva.js` | Cálculo automático de IVA y Total |

---

## Pendiente al final de Fase 6

- **SC-A01**: Widget de accesibilidad (tamaño de letra, alto contraste)
- **PDF facturas**: `xhtml2pdf` para compras y ventas juntos

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
