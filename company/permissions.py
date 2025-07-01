from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSuperAdminOrOwner(BasePermission):
    """
    Allow full access to superadmins.
    Allow CRUD for company owner.
    Allow read-only to others.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser:
            return True
        if request.method in SAFE_METHODS:
            return obj.owner == user
        return obj.owner == user
