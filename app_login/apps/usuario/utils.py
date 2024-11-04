import random
from django.core.mail import EmailMessage

# from app_login.app_login import settings
from  django.conf import settings

from ..usuario.models import Usuario, ContraseñaSoloUso


def generateOtp():
    otp=""
    
    for i in range(6):
        otp += str(random.randint(1,9))
    return otp


def send_code_to_user(email):
    Subject = 'Contraseña de un solo uso, verifique su correo '
    otp_code = generateOtp()
    print(otp_code)
    user = Usuario.objects.get(email=email)

    #current site del env
    current_site = settings.CURRENT_SITE

    email_body = f"Hola!! {user.primer_nombre} gracias por registrarse {current_site}. por favor verifique su correo electronico \n tiempo expiracion del codigo {otp_code}  "
    from_email = settings.DEFAULT_FROM_EMAIL
    
    ContraseñaSoloUso.objects.create(user=user, code=otp_code)
    
    
    d_email = EmailMessage(subject=Subject, body=email_body, from_email=from_email, to=[email])
    d_email.send(fail_silently=True)
    

def send_normal_email(data):
    email = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']]
    )
    
    email.send()