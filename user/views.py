from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password, check_password
from .models import CustomUser
from .serializer import CustomUserSerializer
from .utils import send_otp_email

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def perform_create(self, serializer):
        user = serializer.save(password=make_password(serializer.validated_data['password']))
        user.generate_otp()
        send_otp_email(user)
        return Response({'message': 'User created, OTP sent!', 'user': serializer.data}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='verify-otp')
    def verify_otp(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        try:
            user = CustomUser.objects.get(email=email)
            if user.verify_otp(otp):
                return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        identifier = request.data.get('username') or request.data.get('email')
        password = request.data.get('password')
        user = None
        if '@' in str(identifier):
            user = CustomUser.objects.filter(email=identifier).first()
        else:
            user = CustomUser.objects.filter(username=identifier).first()
        if user and check_password(password, user.password):
            if not user.is_email_verified:
                return Response({'error': 'Email not verified'}, status=status.HTTP_401_UNAUTHORIZED)
            serializer = CustomUserSerializer(user)
            return Response({'message': 'Login successful', 'user': serializer.data}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid username/email or password'}, status=status.HTTP_401_UNAUTHORIZED)
