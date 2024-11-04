from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _



class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Por favor presione enter para validar su Correo Electronico"))
        
    
    def create_user(self, email, primer_nombre, primer_apellido, password, **extra_fields):
        if email:
            email=self.normalize_email(email)
            self.email_validator(email)
            
        else:
            raise ValueError(_("Se requiere la direccion de un Correo Electronico"))
        
        if not primer_nombre:
            raise ValueError(_("Primer Nombre es obligatorio"))
        
        if not primer_apellido:
            raise ValueError(_("Primer Apellido es obligatorio"))
        
        user = self.model(email=email, primer_nombre=primer_nombre, primer_apellido=primer_apellido, **extra_fields)
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, primer_nombre, primer_apellido, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)
        
        
        if extra_fields.get("is_staff") is not True:
            raise ValidationError(_("El usuario es personal deber ser verificado por el administrador "))
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("El superusuario deber ser verificado por el administrador"))
        
        user = self.create_user(
            email, primer_nombre, primer_apellido, password, **extra_fields
        )
        
        user.save(using=self.db)
        return user