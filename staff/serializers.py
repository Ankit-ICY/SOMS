from rest_framework import serializers
from users.models import CustomUser
from .models import CompanyStaff

class CompanyStaffSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    name = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)
    profile_image = serializers.ImageField(required=False, write_only=True)

    class Meta:
        model = CompanyStaff
        fields = ['id', 'company', 'email', 'name', 'phone', 'profile_image']
        read_only_fields = ['id']

    def create(self, validated_data):
        request_user = self.context['request'].user
        company = validated_data['company']

        if company.owner != request_user:
            raise serializers.ValidationError("You are not authorized to add staff to this company.")

        user, created = CustomUser.objects.get_or_create(
            email=validated_data['email'],
            defaults={
                'name': validated_data['name'],
                'phone': validated_data['phone'],
                'role': CustomUser.Roles.NORMAL,
                'profile_image': validated_data.get('profile_image')
            }
        )

        if user.role != CustomUser.Roles.NORMAL:
            raise serializers.ValidationError("Cannot assign an admin or superadmin as staff.")

        if CompanyStaff.objects.filter(company=company, user=user).exists():
            raise serializers.ValidationError("User is already a staff member of this company.")
        
        if created:
            staff = CompanyStaff.objects.create(
                company=company,
                user=user,
                assigned_by=request_user
            )

        return staff
