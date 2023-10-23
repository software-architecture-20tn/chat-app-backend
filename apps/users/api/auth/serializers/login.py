# from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import serializers

# from ..serializers import UserSerializer

User = get_user_model()


# TODO: modify this to adapt
class UserLoginSerializer(serializers.Serializer):
    """Provide a serializer for handling the login of a user."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        """Define the fields to use in the serializer."""

        fields = (
            "email",
            "password",
        )
