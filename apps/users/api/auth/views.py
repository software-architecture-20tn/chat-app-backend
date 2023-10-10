# https://www.section.io/engineering-education/api-authentication-with-django-knox-and-postman-testing/
from django.contrib import auth
from django.contrib.auth import authenticate
from knox.models import AuthToken
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import UserLoginSerializer, UserRegisterSerializer


class RegisterAPIView(generics.GenericAPIView):
    """API view for registering a new user."""
    
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs) -> Response:
        """Handle the registration of a new user."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(
            {
                "user": serializer.data,
            }
        )


class LoginAPIView(generics.GenericAPIView):
    """API view for logging in a user."""

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs) -> Response:
        """Handle the login of a user."""
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user and user.is_active:
            return Response(
                status=200,
                data={
                    "user": UserLoginSerializer(user).data,
                    "token": AuthToken.objects.create(user)[1],
                },
            )
        if user and not user.is_active:
            return Response(
                status=400,
                data={
                    "message": "User is not active.",
                },
            )
        return Response(
            status=400,
            data={
                "message": "Invalid credentials.",
            },
        )
