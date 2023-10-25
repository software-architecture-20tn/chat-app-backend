from django.contrib.auth import authenticate
# from django.contrib.auth import get_user_model
from rest_framework import serializers

# from ..serializers import UserSerializer

# User = get_user_model()


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

    def validate(self, data):
        """Validate the user's credentials."""
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                return user
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")