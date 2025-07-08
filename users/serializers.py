# users/serializers.py
from rest_framework import serializers
from users.models import CustomUser
from django.contrib.auth import authenticate
from company.serializers import CompanySerializer
from rest_framework import serializers
from users.models import CustomUser
from company.models import Company

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    role = serializers.ChoiceField(choices=CustomUser.Roles.choices, default=CustomUser.Roles.ADMIN)

    class Meta:
        model = CustomUser
        fields = ('email', 'phone', 'name', 'password', 'role')

    def validate(self, data):
        if not data.get('email') and not data.get('phone'):
            raise serializers.ValidationError("Either email or phone is required.")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        role = validated_data.pop('role', CustomUser.Roles.ADMIN)
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.role = role 
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name','profile_image', 'email', 'phone', 'role', 'date_joined']

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        identifier = data.get("identifier")
        password = data.get("password")

        if not identifier or not password:
            raise serializers.ValidationError("Both identifier and password are required.")

        user = CustomUser.objects.filter(email=identifier).first()
        if not user:
            user = CustomUser.objects.filter(phone=identifier).first()

        if user and user.check_password(password):
            data["user"] = user
            return data

        raise serializers.ValidationError("Invalid credentials.")
    

class MyInfoSerializer(serializers.ModelSerializer):
    # companies = CompanySerializer(many=True, read_only=True)
    companies = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'phone', 'date_joined','companies']

    def get_companies(self, obj):
        if obj.role == CustomUser.Roles.ADMIN or obj.role == CustomUser.Roles.SUPERADMIN:
            companies = Company.objects.filter(owner = obj)
            company = []
            for comp in companies:
                company.append(
                    {
                        "id" : comp.id,
                        "name" : comp.name,
                    }
                )
            return company
        
        elif obj.role == CustomUser.Roles.NORMAL:
            company_staff = Company.objects.filter(staff=obj)
            company = []
            for staff in company_staff:
                company.append( 
                    {
                        "id" : staff.company.id,
                        "name" : staff.company.name,
                    }
                )
            return company
        else:
            return None

