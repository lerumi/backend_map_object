from rest_framework import permissions, authentication
from rest_framework import exceptions
from app.redis import session_storage
from .models import CustomUser
class AuthBySessionID(authentication.BaseAuthentication):
    def authenticate(self, request):
        session_id = request.COOKIES.get("session_id")
        if session_id is None:
            raise exceptions.AuthenticationFailed("Нужно авторизоваться")
        try:
            username = session_storage.get(session_id).decode("utf-8")
        except Exception as e:
            raise exceptions.AuthenticationFailed("session_id not found")
        user = CustomUser.objects.filter(email=username).first()
        if user is None:
            raise exceptions.AuthenticationFailed("No such user")
        #request.user = user

        return user, None
class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_staff or request.user.is_superuser)

class IsSimpleUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(not request.user.is_staff)

