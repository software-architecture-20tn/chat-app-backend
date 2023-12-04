from django.contrib.auth import authenticate

from rest_framework import serializers


class UserLoginSerializer(serializers.Serializer):
    """Provide a serializer for handling the login of a user."""

    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        """Define the fields to use in the serializer."""

        fields = (
            "id",
            "email",
            "password",
        )

    def validate(self, attrs):
        """Validate the user's credentials."""
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError(
                        "User account is disabled.",
                    )
                return user

            raise serializers.ValidationError(
                "Unable to log in with provided credentials.",
            )

        raise serializers.ValidationError(
            "Must include 'email' and 'password'.",
        )

    def create(self, validated_data):
        """Bypass check."""

    def update(self, instance, validated_data):
        """Bypass check."""


class UserLoginResponseSerializer(serializers.Serializer):
    """Provide a serializer for the response of logging in a user."""

    user = UserLoginSerializer()
    token = serializers.CharField()

    class Meta:
        fields = (
            "user",
            "token",
        )

    def create(self, validated_data):
        """Bypass check."""

    def update(self, instance, validated_data):
        """Bypass check."""
