from django.urls import path
from apps.usuario.api.api import (
    RegistroUserView, VerificarEmail,
    LoginUsuarioView, AutenticaciónView, 
    PasswordResetView, PasswordResetConfirmView, 
    SetNewPasswordView, LogoutUserView
)

urlpatterns = [
    path('registro/', RegistroUserView.as_view(), name='registro'),
    path('verificar/', VerificarEmail.as_view(), name='verificarEmail'),
    path('login/', LoginUsuarioView.as_view(), name='login'),
    path('autenticated/', AutenticaciónView.as_view(), name='autenticated'),
    path('password-reset-confirm/', PasswordResetView.as_view(), name='password-reset-confirm'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set-new-password'),
    path('logout/', LogoutUserView.as_view(), name='logout')
    
]


