from rest_framework import viewsets, permissions
from .models import Company
from .serializers import CompanySerializer
from .permissions import IsSuperAdminOrOwner

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperAdminOrOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Company.objects.all()
        return Company.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
