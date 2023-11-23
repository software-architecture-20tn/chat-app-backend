from rest_framework import serializers

from apps.core.api.serializers import BaseSerializer
from apps.users.models import User


class FriendSerializer(BaseSerializer, serializers.ModelSerializer):
    """Serializer for the Friend model."""

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "avatar",
            "username",

        )
        read_only_fields = (
            "id",
        )