from rest_framework.permissions import BasePermission

from apps.users.models import Client


class IsClientUser(BasePermission):
    """Checking if requesting user is a client user"""

    def has_permission(self, request, view):
        try:
            return bool(request.user.client)
        except Client.DoesNotExist:
            return False


class IsUnAuthenticatedUser(BasePermission):
    """Checking if requesting user is not authenticated"""

    def has_permission(self, request, view):
        return not request.user.is_authenticated
