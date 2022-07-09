from rest_framework.permissions import BasePermission

from apps.users.models import Author


class IsAuthorUser(BasePermission):
    """Checking if requesting user is an author user"""

    def has_permission(self, request, view):
        try:
            return bool(request.user.author)
        except Author.DoesNotExist:
            return False


class IsUnAuthenticatedUser(BasePermission):
    """Checking if requesting user is not authenticated"""

    def has_permission(self, request, view):
        return not request.user.is_authenticated
