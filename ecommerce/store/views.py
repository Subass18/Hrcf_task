from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

def home(request):
    return render(request,'home.html')

def home_view(request):
    return render(request, 'store/home.html')


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['email'] = self.user.email
        data['is_admin'] = self.user.is_admin
        data['is_customer'] = self.user.is_customer
        return data

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "is_staff": user.is_staff
        })
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "email": request.user.email
        })
