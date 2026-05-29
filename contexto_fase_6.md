# SOLGASES — Contexto Fase 6 (Para retomar conversación)

> **Última actualización:** 29 de mayo de 2026
> **Rama:** `main`
> **Último commit:** `cierre-ventas` (se actualiza tras el commit de cierre)

---

## Estado general

- **Fase actual:** 6 — Pruebas y Verificación
- **Módulo en progreso:** `backup` (siguiente — último módulo)
- **Protocolo activo:** Protocolo de Veracidad — Fase 6 v1.1

---

## Módulos

| Módulo | Estado | Commits clave |
|--------|--------|---------------|
| `core` | ✅ Aprobado — 2026-05-26 | `39bfcc5` (cierre) |
| `usuarios` | ✅ Aprobado — 2026-05-29 | `88d74b4` (cierre) |
| `productos` | ✅ Aprobado — 2026-05-29 | `9295480` (cierre) |
| `insumos` | ✅ Aprobado — 2026-05-29 | `670218d` (cierre) |
| `compras` | ✅ Aprobado — 2026-05-29 | `840fb04` (cierre) |
| `ventas` | ✅ Aprobado — 2026-05-29 | `cierre-ventas` (cierre) |
| `backup` | ⏳ Pendiente | — |

---

## Módulo `ventas` — resumen de lo hecho

- `'VENTA'` agregado a `HistorialCambio.MODELO_CHOICES`
- `FacturaVentaForm`: queryset clientes activos + labels con tildes
- `@require_POST` + observación obligatoria en `cambiar_estado_venta`
- **Restauración de stock al desactivar** (Pendiente Fase 5 resuelto): suma de vuelta las cantidades con `HistorialStock`/`HistorialStockInsumo`
- **Validación de stock al reactivar** (diferencia clave vs compras): verifica disponibilidad ANTES de la transacción; si insuficiente, muestra error sin modificar nada
- `HistorialCambio` registra cada cambio de estado
- Paginación 15 registros, búsqueda por N° factura/cliente, breadcrumbs en 3 vistas
- Modal confirmación con advertencia de stock
- `get_metodo_pago_display` y `get_tipo_item_display`
- Exportación Excel de facturas
- **PDF diferido junto con compras** — usar `xhtml2pdf` cuando llegue el momento
- Botón Activar/Desactivar en detalle usa `btn-accion`/`btn-secundario` (no `btn-tabla`)

---

## Decisiones técnicas vigentes (no renegociar)

| Decisión | Razón |
|----------|-------|
| `AXES_LOCKOUT_PARAMETERS = ['username']` sin ip_address | Sistema interno |
| `'unsafe-inline'` solo en `style-src`, NO en `script-src` | CSP |
| JS personalizado siempre en archivo externo | CSP bloquea inline handlers |
| Event delegation para formset (no `onclick`) | CSP |
| PDF diferido a implementación conjunta compras+ventas | Consistencia de layout |
| `openpyxl` + `zoneinfo` para Excel | Sin `pytz` |
| Auditoría manual (sin `django-simple-history`) | Overkill para sistema interno |
| `HistorialCambio` para trazabilidad de estado | Observación obligatoria |
| `HistorialStock` / `HistorialStockInsumo` como modelos dedicados | Datos consultables |
| `stock` solo editable en creación de productos/insumos | Via modificar_stock con motivo |
| Validación stock ANTES de transacción al reactivar ventas | Evita partial-update en BD |
| `btn-accion`/`btn-secundario` para botones con texto en detalle | `btn-tabla` es para íconos |
| Funciones Excel `_estilo_excel`, etc. en `usuarios.views` | Reutilizadas via import |

---

## Archivos JS del proyecto

| Archivo | Propósito |
|---------|-----------|
| `static/js/busqueda.js` | Búsqueda en tiempo real debounce 350ms |
| `static/js/modal_estado.js` | Modal confirmación activar/desactivar |
| `static/js/formset_dinamico.js` | Gestión dinámica de filas (compras/ventas) — event delegation para delete |
| `static/js/calculo_iva.js` | Cálculo automático de IVA y Total |

---

## Pendientes al final de Fase 6

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
