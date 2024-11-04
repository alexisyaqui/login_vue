from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext as _


# importarndo manager.py
from .managers import UserManager

# impportando simplejwt.tokens
from rest_framework_simplejwt.tokens import RefreshToken


# creando modelos
class Usuario(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("admin", "Admin"), 
        ("editor", "Editor"),
        ("vista", "Vista")
        )

    email = models.EmailField(
        max_length=100, unique=True, verbose_name="Correo Electronico"
    )
    primer_nombre = models.CharField(max_length=100, verbose_name="Primer Nombre")
    segundo_nombre = models.CharField(max_length=100, verbose_name="Segundo Nombre")
    primer_apellido = models.CharField(max_length=100, verbose_name="Primer Apellido")
    segundo_apellido = models.CharField(max_length=100, verbose_name="Segundo Apellido")
    roles = models.CharField(max_length=10, choices=ROLE_CHOICES, default='vista')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_inicioSesion = models.DateTimeField(auto_now=True)
    fecha_ultimaSesion = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "primer_nombre",
        "segundo_nombre",
        "primer_apellido",
        "segundo_apellido",
    ]

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return f"{self.primer_nombre} {self.primer_apellido}"

    def tokens(self):
        # importmos refreshtoken
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),  # se  instancia al serializer
        }


class ContraseñaSoloUso(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.user.primer_nombre}--passcode"
