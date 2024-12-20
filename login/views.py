# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from django.shortcuts import render

def index(request):
    return render(request, 'login/index.html')

def loginpage(request):
    return render(request, 'login/loginpage.html')

def signuppage(request):
    return render(request, 'login/signuppage.html')



class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            email = request.data.get("email")
            password = request.data.get("password")
            name = request.data.get("username")
            user = authenticate(request, email=email, password=password)
            if user:
            # Generate tokens
                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "username ": str(name),
                    "email ": str(email)
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)

        if user:
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "username": user.username,  # No need to create a separate variable for the username
                "email": user.email
            }, status=status.HTTP_200_OK)
        
        # Return an error response if authentication fails
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
