from rest_framework import viewsets, permissions
from .models import FoodItem, CompanyFoodItem, FoodCategory
from .serializers import FoodItemSerializer, CompanyFoodItemSerializer, FoodCategorySerializer
from .permissions import IsFoodItemAdminOrReadOnly
from django.db.models import Q
from users.models import CustomUser

class FoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    permission_classes = [IsFoodItemAdminOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.role == CustomUser.Roles.SUPERADMIN:
            return FoodItem.objects.all()
        return FoodItem.objects.filter(
            Q(created_by=self.request.user) |Q(visibility=FoodItem.FoodVisibility.PUBLIC)
            |Q(active=True)
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        if self.request.user.role == CustomUser.Roles.Admin and instance.created_by != self.request.user:
            raise permissions.PermissionDenied("Admins can only update their own food items.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.role == CustomUser.Roles.Admin and instance.created_by != self.request.user:
            raise permissions.PermissionDenied("Admins can only delete their own food items.")
        instance.delete()


class CompanyFoodItemViewSet(viewsets.ModelViewSet):
    serializer_class = CompanyFoodItemSerializer
    permission_classes = [IsFoodItemAdminOrReadOnly]

    def get_queryset(self):
        company_id = self.request.query_params.get('company_id')
        if not company_id:
            return CompanyFoodItem.objects.none()
        return CompanyFoodItem.objects.filter(company__id=company_id)

    def perform_create(self, serializer):
        serializer.save()
