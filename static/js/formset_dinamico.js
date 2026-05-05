// =====================================================
// SOLGASES - Gestion dinamica de formsets
// Usado en: form_compra.html y form_venta.html
// =====================================================

let totalForms = 0;

// Agrega una nueva fila clonando la plantilla oculta
document.getElementById('btn-agregar-item').addEventListener('click', function () {
    const plantilla  = document.getElementById('fila-plantilla').innerHTML;
    const nuevaFila  = plantilla.replace(/__prefix__/g, totalForms);
    const contenedor = document.getElementById('formset-contenedor');

    contenedor.insertAdjacentHTML('beforeend', nuevaFila);
    totalForms++;

    document.getElementById('id_detalles-TOTAL_FORMS').value = totalForms;
});

// Elimina la fila y recalcula totales
function eliminarFila(boton) {
    const fila = boton.closest('.formset-fila');
    fila.remove();
    totalForms--;
    document.getElementById('id_detalles-TOTAL_FORMS').value = totalForms;

    // Reindexar todas las filas restantes
    const filas = document.querySelectorAll('.formset-fila');
    filas.forEach(function (f, idx) {
        f.querySelectorAll('input, select, textarea').forEach(function (campo) {
            if (campo.name) campo.name = campo.name.replace(/detalles-\d+-/, `detalles-${idx}-`);
            if (campo.id)   campo.id   = campo.id.replace(/detalles-\d+-/, `detalles-${idx}-`);
        });
    });

    calcularSubtotalGeneral();
}

// Calcula subtotal de una fila: cantidad x precio_unitario
function calcularSubtotalFila(fila) {
    const cantidad = parseFloat(fila.querySelector('[name$="-cantidad"]').value) || 0;
    const precio   = parseFloat(fila.querySelector('[name$="-precio_unitario"]').value) || 0;
    const subtotal = (cantidad * precio).toFixed(2);

    fila.querySelector('[name$="-subtotal"]').value = subtotal;
}

// Suma los subtotales de todas las filas y actualiza la cabecera
function calcularSubtotalGeneral() {
    let sumaTotal = 0;
    const filas = document.querySelectorAll('.formset-fila');

    filas.forEach(function (fila) {
        const subtotal = parseFloat(fila.querySelector('[name$="-subtotal"]').value) || 0;
        sumaTotal += subtotal;
    });

    const campoSubtotal = document.getElementById('id_subtotal');
    campoSubtotal.value = sumaTotal.toFixed(2);

    // Dispara recalculo de IVA y Total en calculo_iva.js
    campoSubtotal.dispatchEvent(new Event('input'));
}

// Event delegation — detecta cambios en cantidad y precio de cualquier fila
document.getElementById('formset-contenedor').addEventListener('input', function (e) {
    const campo = e.target;
    if (campo.name && (campo.name.includes('-cantidad') || campo.name.includes('-precio_unitario'))) {
        const fila = campo.closest('.formset-fila');
        calcularSubtotalFila(fila);
        calcularSubtotalGeneral();
    }
});

// Agrega una fila vacia automaticamente al cargar la pagina
document.getElementById('btn-agregar-item').click();