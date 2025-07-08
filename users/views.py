# users/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from .serializers import RegisterSerializer, LoginSerializer
from users.models import CustomUser
from .authentication import get_tokens_for_user, secure_authenticate, authenticate_google_user
from users.serializers import UserSerializer  
from rest_framework import generics, permissions
from .serializers import MyInfoSerializer

class RegisterViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Handles user registration with meaningful error handling"""
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            user_data = UserSerializer(user).data  
            return Response({
                'msg': 'Registration successful',
                'user': user_data,
                'tokens': tokens
            }, status=status.HTTP_201_CREATED)
        except ValidationError:
            return Response({
                'msg': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'msg': 'Something went wrong. Please try again later.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginViewSet(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identifier = serializer.validated_data['identifier']
        password = serializer.validated_data['password']

        user = secure_authenticate(identifier, password)
        if user:
            tokens = get_tokens_for_user(user)
            user_data = UserSerializer(user).data
            return Response({
                'msg': 'Login successful',
                'user': user_data,
                'tokens': tokens
            }, status=status.HTTP_200_OK)

        return Response({'msg': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)



class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')

        if not token:
            return Response({'msg': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        user, error = authenticate_google_user(token)
        if error or not user:
            return Response({'msg': 'Google authentication failed', 'error': error}, status=status.HTTP_400_BAD_REQUEST)

        jwt_tokens = get_tokens_for_user(user)

        return Response({
            'msg': 'Login successful',
            'user': {
                'id': str(user.id),
                'email': user.email,
                'name': user.name,
                'phone': user.phone,
            },
            'tokens': jwt_tokens    
            
        }, status=status.HTTP_200_OK)



class MyInfoAPIView(viewsets.ModelViewSet):
    serializer_class = MyInfoSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        print('----------------------')
        return CustomUser.objects.filter(id=self.request.user.id)