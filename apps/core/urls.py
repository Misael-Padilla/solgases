from django.urls import path
from apps.core import views
from django.contrib.auth import views as auth_views

# Namespace del módulo core — permite usar {% url 'core:inicio' %} en los templates
app_name = 'core'

urlpatterns = [
    # Dashboard principal
    path('', views.inicio, name='inicio'),

    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),

    # Recuperación de contraseña — vistas integradas de Django
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='core/password_reset.html'
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='core/password_reset_done.html'
    ), name='password_reset_done'),

    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='core/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='core/password_reset_complete.html'
    ), name='password_reset_complete'),

    # Manual de usuario
    path('manual/', views.manual, name='manual'),
]