# users/serializers.py
from rest_framework import serializers
from users.models import CustomUser
from django.contrib.auth import authenticate

from rest_framework import serializers
from users.models import CustomUser

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
        fields = ['id', 'name', 'email', 'phone', 'role', 'date_joined']

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