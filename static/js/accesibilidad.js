(function () {
    'use strict';

    var STORAGE_TAMANO   = 'solgases_tamano';
    var STORAGE_CONTRASTE = 'solgases_contraste';
    var STORAGE_GRISES   = 'solgases_grises';

    var TAMANO_BASE = 13;
    var TAMANO_MIN  = 8;
    var TAMANO_MAX  = 20;

    /* -------------------------------------------------------
       Inyecta un <style> dinámico con los tamaños de letra.
       delta = tamanoActual - TAMANO_BASE
    ------------------------------------------------------- */
    function aplicarTamanoFuente(tamano) {
        tamano = Math.min(TAMANO_MAX, Math.max(TAMANO_MIN, tamano));
        var delta = tamano - TAMANO_BASE;

        var estilos = document.getElementById('solgases-fuente-dinamica');
        if (!estilos) {
            estilos = document.createElement('style');
            estilos.id = 'solgases-fuente-dinamica';
            document.head.appendChild(estilos);
        }

        if (delta === 0) {
            estilos.textContent = '';
            return;
        }

        /* Aplica el mismo delta a cada elemento, con mínimo 8px */
        var px = function (base) { return Math.max(8, base + delta) + 'px'; };

        estilos.textContent = [
            '.texto-descripcion { font-size: '          + px(13) + ' !important; }',
            '.tabla-sistema td, .tabla-sistema th { font-size: ' + px(12) + ' !important; }',
            '.form-label { font-size: '                 + px(13) + ' !important; }',
            '.detalle-valor { font-size: '              + px(14) + ' !important; }',
            '.detalle-label { font-size: '              + px(11) + ' !important; }',
            '.detalle-seccion-titulo { font-size: '     + px(13) + ' !important; }',
            '.breadcrumbs-item, .breadcrumbs-link { font-size: ' + px(12) + ' !important; }',
            'h5.fw-bold { font-size: '                  + px(14) + ' !important; }'
        ].join('\n');
    }

    /* -------------------------------------------------------
       Aplica preferencias guardadas (antes del render).
    ------------------------------------------------------- */
    function aplicarPreferencias() {
        var tamano    = parseInt(localStorage.getItem(STORAGE_TAMANO), 10) || TAMANO_BASE;
        var contraste = localStorage.getItem(STORAGE_CONTRASTE) === 'true';
        var grises    = localStorage.getItem(STORAGE_GRISES) === 'true';

        aplicarTamanoFuente(tamano);

        if (contraste) document.documentElement.classList.add('alto-contraste');
        if (grises)    document.documentElement.classList.add('escala-grises');
    }

    /* -------------------------------------------------------
       Actualiza botones y etiqueta de tamaño actual.
    ------------------------------------------------------- */
    function actualizarUIFuente(tamano) {
        var btnMenos   = document.getElementById('btn-fuente-menos');
        var btnReset   = document.getElementById('btn-fuente-reset');
        var btnMas     = document.getElementById('btn-fuente-mas');
        var etiqueta   = document.getElementById('fuente-actual-label');

        if (btnMenos)  btnMenos.disabled = (tamano <= TAMANO_MIN);
        if (btnMas)    btnMas.disabled   = (tamano >= TAMANO_MAX);

        if (btnReset) {
            btnReset.textContent = (tamano === TAMANO_BASE) ? 'A' : tamano + 'px';
            btnReset.setAttribute('aria-pressed', tamano === TAMANO_BASE ? 'false' : 'true');
        }

        if (etiqueta) {
            etiqueta.textContent = tamano === TAMANO_BASE
                ? ''
                : tamano + 'px';
        }
    }

    /* -------------------------------------------------------
       Inicializa el widget.
    ------------------------------------------------------- */
    function initWidget() {
        var btnToggle    = document.getElementById('btn-accesibilidad');
        var panel        = document.getElementById('panel-accesibilidad');
        var btnMenos     = document.getElementById('btn-fuente-menos');
        var btnReset     = document.getElementById('btn-fuente-reset');
        var btnMas       = document.getElementById('btn-fuente-mas');
        var btnContraste = document.getElementById('btn-contraste');
        var btnDaltonismo = document.getElementById('btn-daltonismo');

        if (!btnToggle || !panel) return;

        var tamanoActual = parseInt(localStorage.getItem(STORAGE_TAMANO), 10) || TAMANO_BASE;

        /* Abrir / cerrar panel */
        btnToggle.addEventListener('click', function () {
            var abierto = this.getAttribute('aria-expanded') === 'true';
            this.setAttribute('aria-expanded', abierto ? 'false' : 'true');
            panel.hidden = abierto;
        });

        /* Cerrar con Escape */
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && !panel.hidden) {
                panel.hidden = true;
                btnToggle.setAttribute('aria-expanded', 'false');
                btnToggle.focus();
            }
        });

        /* Disminuir tamaño */
        if (btnMenos) {
            btnMenos.addEventListener('click', function () {
                if (tamanoActual > TAMANO_MIN) {
                    tamanoActual--;
                    aplicarTamanoFuente(tamanoActual);
                    localStorage.setItem(STORAGE_TAMANO, tamanoActual);
                    actualizarUIFuente(tamanoActual);
                }
            });
        }

        /* Restaurar tamaño normal */
        if (btnReset) {
            btnReset.addEventListener('click', function () {
                tamanoActual = TAMANO_BASE;
                aplicarTamanoFuente(tamanoActual);
                localStorage.removeItem(STORAGE_TAMANO);
                actualizarUIFuente(tamanoActual);
            });
        }

        /* Aumentar tamaño */
        if (btnMas) {
            btnMas.addEventListener('click', function () {
                if (tamanoActual < TAMANO_MAX) {
                    tamanoActual++;
                    aplicarTamanoFuente(tamanoActual);
                    localStorage.setItem(STORAGE_TAMANO, tamanoActual);
                    actualizarUIFuente(tamanoActual);
                }
            });
        }

        /* Alto contraste */
        if (btnContraste) {
            btnContraste.addEventListener('click', function () {
                var activo = document.documentElement.classList.toggle('alto-contraste');
                this.setAttribute('aria-pressed', activo ? 'true' : 'false');
                localStorage.setItem(STORAGE_CONTRASTE, activo ? 'true' : 'false');
            });
            btnContraste.setAttribute(
                'aria-pressed',
                localStorage.getItem(STORAGE_CONTRASTE) === 'true' ? 'true' : 'false'
            );
        }

        /* Daltonismo — escala de grises */
        if (btnDaltonismo) {
            btnDaltonismo.addEventListener('click', function () {
                var activo = document.documentElement.classList.toggle('escala-grises');
                this.setAttribute('aria-pressed', activo ? 'true' : 'false');
                localStorage.setItem(STORAGE_GRISES, activo ? 'true' : 'false');
            });
            btnDaltonismo.setAttribute(
                'aria-pressed',
                localStorage.getItem(STORAGE_GRISES) === 'true' ? 'true' : 'false'
            );
        }

        /* Estado inicial de los botones de fuente */
        actualizarUIFuente(tamanoActual);
    }

    /* Aplicar preferencias de inmediato (antes del render) */
    aplicarPreferencias();

    /* Inicializar controles cuando el DOM esté listo */
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initWidget);
    } else {
        initWidget();
    }

}());
