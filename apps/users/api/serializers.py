from rest_framework import serializers

from apps.core.api.serializers import BaseSerializer
from apps.users.models import User


class UserSerializer(BaseSerializer ,serializers.ModelSerializer):
    """Serializer for the User model."""

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            
        )
        read_only_fields = (
            "id",
        )