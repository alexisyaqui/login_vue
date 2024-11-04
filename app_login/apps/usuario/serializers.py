from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes, force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


#validacion de email
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError

from app_login import settings
from apps.usuario.models import Usuario

# utils
from .utils import send_normal_email


class RegistroUsuarioSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100, min_length=6)
    password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=100, min_length=6, write_only=True)
    is_staff = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(default=False)

    class Meta:
        model = Usuario
        fields = [
            "email",
            "primer_nombre",
            "primer_apellido",
            "password",
            "password2",
            'roles',
            "is_staff",
            "is_superuser",
        ]


    def validate(self, attrs):
        password = attrs.get("password", "")
        password2 = attrs.get("password2", "")

        # Validar que ambas contraseñas coincidan
        if password != password2:
            raise serializers.ValidationError(
                "La contraseña no coinciden, vuelva a intentarlo"
            )
        return attrs
    
    def validate_email(self, value):
        try:
            validate_email(value)

        except DjangoValidationError:
            raise serializers.ValidationError("El formato del correo electronico no es valido ")
        
        if "example.com" in value:
            raise serializers.ValidationError("No se permiten correos de example.com")
        
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo Electronico ya se encuentra registrado")
        return value

    def create(self, validated_data):
        # Eliminar password2 de validated_data porque no es necesario guardarlo en el modelo
        validated_data.pop("password2", None)

        user = Usuario.objects.create_user(
            email=validated_data["email"],
            primer_nombre=validated_data["primer_nombre"],
            primer_apellido=validated_data["primer_apellido"],
            password=validated_data["password"],
            is_staff=validated_data.get("is_staff", True),
            is_superuser=validated_data.get("is_superuser", False),
        )

        return user


class VerificarEmailSerializer(serializers.Serializer):

    otp = serializers.CharField(max_length=6, required=True)

    def validate_otp(self, value):
        if len(value) != 6 or not value.isdigit():
            raise serializers.ValidationError(
                "El codigo debe ser un numero de 6 digitos."
            )

        return value


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)

    class Meta:
        model = Usuario
        fields = ["email"]

    def validate(self, attrs):
    

        email = attrs.get("email")
        if Usuario.objects.filter(email=email).exists():
            user = Usuario.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            # request = self.context.get("request")
            # site_domain = get_current_site(request).domain
            # relative_link = reverse(
            #     "password-reset-confirm", kwargs={"uidb64": uidb64, "token": token}
            # )
            frontend_domain = settings.frontend_domain
            relative_link = f"/password-reset-confirm/{uidb64}/{token}"
            abslink = f"{frontend_domain}{relative_link}"
            email_body = f"Hola {user.primer_nombre} {user.primer_apellido} ingrese en el siguiente link para resetear su contraseña {abslink}"
            data = {
                "email_body": email_body,
                "email_subject": "Resetear la Contraseña",
                "to_email": user.email,
            }

            send_normal_email(data)
        return attrs

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    confirm_password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = ["password", "confirm_password", "uidb64", "token"]

    def validate(self, attrs):
        try:
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")
            password = attrs.get("password")
            confirm_password = attrs.get("confirm_password")

            # decodificar el uidb64
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = Usuario.objects.get(id=user_id)

            # verificar si el token es valido
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed(
                    "el enlace para resetear su contraseña ha expirado", 401
                )

            # comprobar que las conntraseñas coincidan
            if password != confirm_password:
                raise AuthenticationFailed("La contraseña no coincide")

            # establecer la nueva contraseña
            user.set_password(password)
            user.save()
            return user

        except Usuario.DoesNotExist:
            raise AuthenticationFailed("Usuario no encontrado.", 404)

        except Exception as e:
            return AuthenticationFailed("enlace es invalido o ha expirado")
        
        return attrs
        
        

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100, min_length=6)
    password = serializers.CharField(max_length=100, write_only=True)
    full_name = serializers.CharField(max_length=100, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    is_admin = serializers.BooleanField(source='is_superuser', read_only=True)


    class Meta:
        model = Usuario
        fields = [
            "email",
            "password",
            "full_name",
            "access_token",
            "refresh_token",
            "is_staff",
            "is_superuser",
            "is_admin",
        ]

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        request = self.context.get("request")  # viene de ls api. context


        try:
            user = Usuario.objects.get(email= email)
        except Usuario.DoesNotExist:
            raise AuthenticationFailed("Este correo no esta registrado")

        # Autenticar usuario
        user = authenticate(request, email=email, password=password)

        if not user:
            raise AuthenticationFailed("credenciales invalidas")

        if not user.is_verified:
            raise AuthenticationFailed("Correo electronico no verificado")

        # generar los tokens de acceso desde el modelo
        user_tokens = user.tokens()  # del modelo tokens

        return {
            "email": user.email,
            "full_name": user.get_full_name,
            "access_token": str(user_tokens.get("access")),
            "refresh_token": str(user_tokens.get("refresh")),
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,

        }

class LogoutUserSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    default_error_messages = {"bad_token": ("Token invalido o ha expirado")}

    def validate(self, attrs):
        self.token = attrs.get("refresh_token")
        if not self.token:
            raise serializers.ValidationError("El token de actualización es requerido.")
        return attrs


    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:

            return self.fail("bad_token")


