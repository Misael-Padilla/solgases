from django.urls import path, reverse_lazy
from apps.core import views
from apps.core.forms import CustomPasswordResetForm
from django.contrib.auth import views as auth_views

# Namespace del módulo core — permite usar {% url 'core:inicio' %} en los templates
app_name = 'core'

urlpatterns = [
    # Dashboard principal
    path('', views.inicio, name='inicio'),

    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),

    # Recuperación de contraseña — vistas integradas de Django con namespace
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='core/password_reset.html',
        form_class=CustomPasswordResetForm,
        email_template_name='core/password_reset_email.html',
        success_url=reverse_lazy('core:password_reset_done')
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='core/password_reset_done.html'
    ), name='password_reset_done'),

    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='core/password_reset_confirm.html',
        success_url=reverse_lazy('core:password_reset_complete')
    ), name='password_reset_confirm'),

    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='core/password_reset_complete.html'
    ), name='password_reset_complete'),

    # Manual de usuario
    path('manual/', views.manual, name='manual'),
]