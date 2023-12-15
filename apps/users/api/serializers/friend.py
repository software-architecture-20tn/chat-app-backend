from django.db.models import Q

from rest_framework import serializers

from apps.core.api.serializers import BaseModelSerializer
from apps.users.models import FriendRequest, Friendship, User


class FriendSerializer(BaseModelSerializer):
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
        read_only_fields = ("id",)


class FriendRequestSerializer(BaseModelSerializer):
    class Meta:
        model = FriendRequest
        fields = (
            "id",
            "sender",
            "receiver",
            "date_time_sent",
            "is_approved",
        )
        read_only_fields = (
            "id",
            "sender",
            "is_approved",
        )

    def validate_receiver(self, value):
        user = self._user
        if value == user:
            raise serializers.ValidationError(
                "The receiver can't be the same as the sender.",
            )
        if not User.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError(
                "The receiver doesn't exist.",
            )
        if Friendship.objects.filter(
            Q(user1=value, user2=user)
            | Q(user2=value, user1=user)
        ).exists():
            raise serializers.ValidationError(
                "The receiver is already a friend.",
            )
        if FriendRequest.objects.filter(Q(sender=value)).exists():
            raise serializers.ValidationError(
                "The receiver already sent a friend request.",
            )
        if FriendRequest.objects.filter(Q(receiver=value)).exists():
            raise serializers.ValidationError(
                "The receiver already received a friend request.",
            )
        return value

    def create(self, validated_data):
        user = self._user
        validated_data["sender"] = user
        return super().create(validated_data)
