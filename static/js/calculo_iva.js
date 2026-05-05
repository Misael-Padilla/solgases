// =====================================================
// SOLGASES - Cálculo automático de IVA y Total
// Usado en: form_compra.html y form_venta.html
// =====================================================

function calcularIVA() {
    const subtotalCampo       = document.getElementById('id_subtotal');
    const ivaPorcentajeCampo  = document.getElementById('id_iva_porcentaje');
    const ivaMontoCampo       = document.getElementById('id_iva');
    const totalCampo          = document.getElementById('id_total');

    const subtotal      = parseFloat(subtotalCampo.value) || 0;
    const ivaPorcentaje = parseFloat(ivaPorcentajeCampo.value) || 0;

    const ivaMonto = (subtotal * ivaPorcentaje / 100).toFixed(2);
    const total    = (subtotal + parseFloat(ivaMonto)).toFixed(2);

    ivaMontoCampo.value = ivaMonto;
    totalCampo.value    = total;
}

// Recalcular cuando el usuario modifica Subtotal o IVA (%)
document.getElementById('id_subtotal').addEventListener('input', calcularIVA);
document.getElementById('id_iva_porcentaje').addEventListener('input', calcularIVA);