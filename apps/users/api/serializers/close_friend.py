from rest_framework import serializers

from apps.core.api.serializers import BaseModelSerializer, BaseSerializer
from apps.users.models import User


class CloseFriendListSerializer(BaseModelSerializer):
    """Serializer for close friend list API."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "avatar",
        )


class CloseFriendAddSerializer(BaseSerializer):
    """Serializer for close friend add API."""

    close_friend_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=True,
    )

    class Meta:
        fields = ("close_friend_id",)
