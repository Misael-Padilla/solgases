(function () {
    'use strict';

    const input = document.querySelector('.busqueda-input');
    if (!input) return;

    const limpiarBtn = document.querySelector('.busqueda-limpiar');
    const contenedor = document.getElementById('resultados-container');
    let timer;

    function actualizarLimpiar(q) {
        if (!limpiarBtn) return;
        if (q) {
            limpiarBtn.classList.remove('d-none');
        } else {
            limpiarBtn.classList.add('d-none');
        }
    }

    input.addEventListener('input', function () {
        clearTimeout(timer);
        const q = input.value.trim();
        actualizarLimpiar(q);

        timer = setTimeout(async function () {
            const url = new URL(window.location.href);
            if (q) {
                url.searchParams.set('q', q);
            } else {
                url.searchParams.delete('q');
            }

            contenedor.setAttribute('aria-busy', 'true');

            try {
                const res = await fetch(url.toString(), {
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                });
                const html = await res.text();
                const doc = new DOMParser().parseFromString(html, 'text/html');
                const nuevo = doc.getElementById('resultados-container');
                if (nuevo) {
                    contenedor.innerHTML = nuevo.innerHTML;
                    contenedor.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (el) {
                        new bootstrap.Tooltip(el);
                    });
                }
                history.pushState({}, '', url.toString());
            } catch (_) {
                // Fallback: el formulario GET sigue funcionando sin JS
            } finally {
                contenedor.setAttribute('aria-busy', 'false');
            }
        }, 350);
    });
})();
