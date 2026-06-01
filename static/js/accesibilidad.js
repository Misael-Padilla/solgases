(function () {
    'use strict';

    var STORAGE_FUENTE    = 'solgases_fuente';
    var STORAGE_CONTRASTE = 'solgases_contraste';
    var STORAGE_GRISES    = 'solgases_grises';
    var CLASES_FUENTE    = ['tamanio-grande', 'tamanio-pequeno'];

    /* -------------------------------------------------------
       Aplica las preferencias guardadas en localStorage.
       Se llama antes del DOMContentLoaded para evitar flash.
    ------------------------------------------------------- */
    function aplicarPreferencias() {
        var fuente    = localStorage.getItem(STORAGE_FUENTE);
        var contraste = localStorage.getItem(STORAGE_CONTRASTE);

        CLASES_FUENTE.forEach(function (c) {
            document.documentElement.classList.remove(c);
        });

        if (fuente) {
            document.documentElement.classList.add(fuente);
        }

        if (contraste === 'true') {
            document.documentElement.classList.add('alto-contraste');
        }

        if (localStorage.getItem(STORAGE_GRISES) === 'true') {
            document.documentElement.classList.add('escala-grises');
        }
    }

    /* -------------------------------------------------------
       Marca el botón activo de tamaño de fuente.
    ------------------------------------------------------- */
    function actualizarBotonesFuente(activo) {
        var mapa = {
            'tamanio-pequeno': document.getElementById('btn-fuente-pequena'),
            'normal':          document.getElementById('btn-fuente-normal'),
            'tamanio-grande':  document.getElementById('btn-fuente-grande')
        };
        Object.keys(mapa).forEach(function (clave) {
            var btn = mapa[clave];
            if (!btn) return;
            var estaActivo = clave === activo;
            btn.setAttribute('aria-pressed', estaActivo ? 'true' : 'false');
        });
    }

    /* -------------------------------------------------------
       Inicializa el widget una vez que el DOM está listo.
    ------------------------------------------------------- */
    function initWidget() {
        var btnToggle   = document.getElementById('btn-accesibilidad');
        var panel       = document.getElementById('panel-accesibilidad');
        var btnPequena  = document.getElementById('btn-fuente-pequena');
        var btnNormal   = document.getElementById('btn-fuente-normal');
        var btnGrande   = document.getElementById('btn-fuente-grande');
        var btnContraste = document.getElementById('btn-contraste');

        if (!btnToggle || !panel) return;

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

        /* Fuente pequeña */
        if (btnPequena) {
            btnPequena.addEventListener('click', function () {
                CLASES_FUENTE.forEach(function (c) { document.documentElement.classList.remove(c); });
                document.documentElement.classList.add('tamanio-pequeno');
                localStorage.setItem(STORAGE_FUENTE, 'tamanio-pequeno');
                actualizarBotonesFuente('tamanio-pequeno');
            });
        }

        /* Fuente normal */
        if (btnNormal) {
            btnNormal.addEventListener('click', function () {
                CLASES_FUENTE.forEach(function (c) { document.documentElement.classList.remove(c); });
                localStorage.removeItem(STORAGE_FUENTE);
                actualizarBotonesFuente('normal');
            });
        }

        /* Fuente grande */
        if (btnGrande) {
            btnGrande.addEventListener('click', function () {
                CLASES_FUENTE.forEach(function (c) { document.documentElement.classList.remove(c); });
                document.documentElement.classList.add('tamanio-grande');
                localStorage.setItem(STORAGE_FUENTE, 'tamanio-grande');
                actualizarBotonesFuente('tamanio-grande');
            });
        }

        /* Alto contraste */
        if (btnContraste) {
            btnContraste.addEventListener('click', function () {
                var activo = document.documentElement.classList.toggle('alto-contraste');
                this.setAttribute('aria-pressed', activo ? 'true' : 'false');
                localStorage.setItem(STORAGE_CONTRASTE, activo ? 'true' : 'false');
            });
        }

        /* Daltonismo — escala de grises */
        var btnDaltonismo = document.getElementById('btn-daltonismo');
        if (btnDaltonismo) {
            btnDaltonismo.addEventListener('click', function () {
                var activo = document.documentElement.classList.toggle('escala-grises');
                this.setAttribute('aria-pressed', activo ? 'true' : 'false');
                localStorage.setItem(STORAGE_GRISES, activo ? 'true' : 'false');
            });
        }

        /* Sincronizar estado visual de botones con localStorage */
        var fuenteActual    = localStorage.getItem(STORAGE_FUENTE) || 'normal';
        var contrasteActivo = localStorage.getItem(STORAGE_CONTRASTE) === 'true';
        var grisesActivo    = localStorage.getItem(STORAGE_GRISES) === 'true';

        actualizarBotonesFuente(fuenteActual);

        if (btnContraste) {
            btnContraste.setAttribute('aria-pressed', contrasteActivo ? 'true' : 'false');
        }
        if (btnDaltonismo) {
            btnDaltonismo.setAttribute('aria-pressed', grisesActivo ? 'true' : 'false');
        }
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
