document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (el) {
        new bootstrap.Tooltip(el);
    });

    const btn   = document.getElementById('btn-toggle-password');
    const input = document.getElementById('password');
    const icono = document.getElementById('icono-password');

    if (btn) {
        btn.addEventListener('click', function () {
            if (input.type === 'password') {
                input.type = 'text';
                icono.classList.replace('bi-eye', 'bi-eye-slash');
                const t = bootstrap.Tooltip.getInstance(btn);
                if (t) t.setContent({ '.tooltip-inner': 'Ocultar contraseña' });
            } else {
                input.type = 'password';
                icono.classList.replace('bi-eye-slash', 'bi-eye');
                const t = bootstrap.Tooltip.getInstance(btn);
                if (t) t.setContent({ '.tooltip-inner': 'Mostrar contraseña' });
            }
        });
    }
});
