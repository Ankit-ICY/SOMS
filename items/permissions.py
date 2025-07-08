from rest_framework import permissions
from users.models import CustomUser

class IsFoodItemAdminOrReadOnly(permissions.BasePermission):
    """
    SuperAdmin: full access.
    Admin: create/delete own, update own.
    Normal: read-only.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.role in [CustomUser.Roles.ADMIN, CustomUser.Roles.SUPERADMIN]

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.role == CustomUser.Roles.SUPERADMIN:
            return True
        return obj.created_by == request.user
