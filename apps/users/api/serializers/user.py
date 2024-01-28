from rest_framework import serializers

from apps.core.api.serializers import BaseModelSerializer, BaseSerializer
from apps.users.models import User


class UserSerializer(BaseSerializer, serializers.ModelSerializer):
    """Serializer for the User model."""

    class Meta:
        model = User
        fields: tuple[str, ...] = (
            "id",
            "first_name",
            "last_name",
            "email",
        )


class UserSearchSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar",
        )
