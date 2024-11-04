from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import AuthenticationFailed

from ..permissions import IsAdminUser


# models
from ..models import ContraseñaSoloUso, Usuario

# utils
from ..utils import send_code_to_user

# serializer
from ..serializers import (LogoutUserSerializer, PasswordResetSerializer, RegistroUsuarioSerializer, 
                           LoginSerializer, SetNewPasswordSerializer,
                           VerificarEmailSerializer)


class RegistroUserView(GenericAPIView):
    serializer_class = RegistroUsuarioSerializer
    
    
    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)

        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                user = serializer.data
                #enviar email funcion ['email']
                send_code_to_user(user['email'])
            
                return Response({
                    'data': user,
                    'message': f'Hola  gracias por registrarse con nosotros, se ha enviado un codigo a su \
                    correo electronico, no comparta este codigo', }, status=status.HTTP_201_CREATED)
       
        except Exception as e:
            # Manejo de excepciones: Puedes registrar el error o imprimirlo para debug
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
             
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerificarEmail(GenericAPIView):
    serializer_class = VerificarEmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            otpcode = serializer.validated_data.get('otp')

            try:
                user_code_obj = ContraseñaSoloUso.objects.get(code=otpcode)
                user = user_code_obj.user

                if not user.is_verified:
                    user.is_verified=True
                    user.save()
                    return Response({
                        'message': 'Cuenta de usuario verificado con exito'
                    }, status=status.HTTP_200_OK)

                return Response ({
                    'message': 'El código es inválido o el usuario ya ha sido verificado'
                }, status=status.HTTP_400_BAD_REQUEST)

            except ContraseñaSoloUso.DoesNotExist:
                return Response({
                    'message': 'Contraseña no proporcionada'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUsuarioView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request}
        )  # el contexto se va instanciar en el serializer

        try:
            serializer.is_valid(raise_exception=True)
            return Response({
                    "message": "Inicio de sesion exitoso",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
        
        except AuthenticationFailed as e:
            return Response({
                "message": str(e)
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                "message": "Ocurrió un error inesperado.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AutenticaciónView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        data = {
            'message': 'Bienvenido a nuestro servicio'
        }
        
        return Response(
            data, status=status.HTTP_200_OK
        )

class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        return Response({
                'message': 'Se ha enviado un enlace a su correo electronico para que reestablezca su contraseña'
            
        }, status=status.HTTP_200_OK)


class PasswordResetConfirmView(GenericAPIView):
    def get(self, request, uidb64, token, *args, **kwargs):
        
        try:

            # if not uidb64 or not token:
            #     return Response({'error': 'Parametos invalidos'}, status=status.HTTP_400_BAD_REQUEST),
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = Usuario.objects.get(id=user_id)
            
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({
                    'message':'Token invalido o ha sido expirado'},status=status.HTTP_401_UNAUTHORIZED)
                
            return Response({
                'success': True,
                'message': 'Credenciales son validas',
                'uidb64': uidb64,
                'token': token
            }, status=status.HTTP_200_OK)
            
        except DjangoUnicodeDecodeError as identifier:
            return Response({
                'message': 'El token es invalido o ha expirado'
            }, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            'message': 'Contraseña ha sido reseteado con exito!!!.'
        }, status=status.HTTP_200_OK)


class LogoutUserView(GenericAPIView):
    serializer_class = LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "Error en la solicitud", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(
            {"message": "Sesión cerrada con éxito"}, status=status.HTTP_200_OK
        )
