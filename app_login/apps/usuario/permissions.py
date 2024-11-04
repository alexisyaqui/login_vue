from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):

    # Permiso personalizado que permite el acceso solo a los usuarios administradores.

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roles == 'admin'
