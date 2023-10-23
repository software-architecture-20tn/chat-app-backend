from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.users.api.serializers import UserSerializer

User = get_user_model()


# https://www.codersarts.com/post/how-to-create-register-and-login-api-using-django-rest-framework-and-token-authentication
class UserRegisterSerializer(UserSerializer):
    """Provide a serializer for handling the registration of a user."""

    first_name = serializers.CharField(required=False, max_length=30)
    last_name = serializers.CharField(required=False, max_length=30)
    password = serializers.CharField(
        required=True,
        write_only=True,
        validators=(validate_password,),
    )
    password_retype = serializers.CharField(required=True, write_only=True)

    class Meta(UserSerializer.Meta):
        """Define the fields to use in the serializer."""

        fields = UserSerializer.Meta.fields + (
            "password",
            "password_retype",
            "username",
        )

    def validate_password_retype(self, value):
        """Check if the password and the password_retype are the same."""
        if self.initial_data.get("password") != value:
            raise serializers.ValidationError("The passwords don't match.")
        return value

    def create(self, validated_data):
        """Create a new user."""
        validated_data.pop("password_retype")
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        user = User.objects.create_user(
            email=email,
            password=password,
            **validated_data,
        )
        return user
