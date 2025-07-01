# users/authentication.py
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from users.models import CustomUser
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from google.oauth2 import id_token
from google.auth.transport import requests
from users.models import CustomUser

def get_tokens_for_user(user):
    """
    Securely returns access and refresh tokens for a user
    """
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }

User = get_user_model()

def secure_authenticate(identifier, password):
    try:
        user = User.objects.filter(email=identifier).first()
        if not user:
            user = User.objects.filter(phone=identifier).first()
        if user and user.check_password(password):
            return user
    except User.DoesNotExist:
        return None
    return None


def authenticate_google_user(token):
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request())
        
        # Check audience/client_id if needed:
        # if idinfo['aud'] != YOUR_GOOGLE_CLIENT_ID:
        #     raise ValueError('Unrecognized client.')

        email = idinfo.get('email')
        name = idinfo.get('name')

        if not email:
            return None, "Email not found in token"

        user, created = CustomUser.objects.get_or_create(email=email, defaults={'name': name})
        return user, None

    except ValueError as e:
        return None, str(e)
