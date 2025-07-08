# company/views.py

from rest_framework import viewsets, permissions
from .models import CompanyStaff
from .serializers import CompanyStaffSerializer
from users.models import CustomUser

class IsCompanyAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == CustomUser.Roles.ADMIn

class CompanyStaffViewSet(viewsets.ModelViewSet):
    queryset = CompanyStaff.objects.all()
    serializer_class = CompanyStaffSerializer
    permission_classes = [permissions.IsAuthenticated, IsCompanyAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role == CustomUser.Roles.SUPERADMIN:
            return CompanyStaff.objects.all()
        return CompanyStaff.objects.filter(company__owner=user)

    def perform_create(self, serializer):
        serializer.save()
