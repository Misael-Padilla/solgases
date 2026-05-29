(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        var modalEl = document.getElementById('modal-cambiar-estado');
        if (!modalEl) return;

        // Bootstrap dispara 'show.bs.modal' antes de mostrar el modal.
        // event.relatedTarget es el botón que lo disparó.
        modalEl.addEventListener('show.bs.modal', function (event) {
            var btn = event.relatedTarget;
            document.getElementById('modal-nombre-objeto').textContent = btn.getAttribute('data-nombre');
            document.getElementById('modal-accion-texto').textContent  = btn.getAttribute('data-accion');
            document.getElementById('modal-form-toggle').action        = btn.getAttribute('data-url');
            var obs = document.getElementById('modal-observacion');
            obs.value = '';
            obs.classList.remove('is-invalid');
        });

        // Enfoca el textarea cuando el modal termina de abrirse (accesibilidad)
        modalEl.addEventListener('shown.bs.modal', function () {
            document.getElementById('modal-observacion').focus();
        });

        // Validación client-side: observación obligatoria antes de enviar
        var form = document.getElementById('modal-form-toggle');
        if (!form) return;
        form.addEventListener('submit', function (e) {
            var obs = document.getElementById('modal-observacion');
            if (!obs.value.trim()) {
                e.preventDefault();
                obs.classList.add('is-invalid');
                obs.focus();
            }
        });
        document.getElementById('modal-observacion').addEventListener('input', function () {
            this.classList.remove('is-invalid');
        });
    });
}());
