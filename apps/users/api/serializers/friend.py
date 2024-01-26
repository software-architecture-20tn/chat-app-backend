from django.db.models import Q

from rest_framework import serializers

from apps.core.api.serializers import BaseModelSerializer
from apps.users.api.serializers.user import UserSerializer
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
    """Serializer for the FriendRequest model."""

    sender_username = serializers.CharField(
        source="sender.username", read_only=True
    )
    sender_first_name = serializers.CharField(
        source="sender.first_name", read_only=True
    )
    sender_last_name = serializers.CharField(
        source="sender.last_name", read_only=True
    )
    sender_avatar = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = (
            "id",
            "sender",
            "sender_username",
            "sender_first_name",
            "sender_last_name",
            "sender_avatar",
            "receiver",
            "date_time_sent",
            "is_approved",
        )
        read_only_fields = (
            "id",
            "sender",
            "sender_username",
            "sender_first_name",
            "sender_last_name",
            "is_approved",
            "sender_avatar",
        )

    def get_sender_avatar(self, obj):
        return obj.sender.avatar.url if obj.sender.avatar else None

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
            Q(user1=value, user2=user) | Q(user2=value, user1=user)
        ).exists():
            raise serializers.ValidationError(
                "The receiver is already a friend.",
            )
        if FriendRequest.objects.filter(
            sender=value,
            receiver=user,
            is_approved=False,
        ).exists():
            raise serializers.ValidationError(
                "The receiver already sent you a friend request.",
            )
        if FriendRequest.objects.filter(
            sender=user,
            receiver=value,
            is_approved=False,
        ).exists():
            raise serializers.ValidationError(
                "The receiver already received a friend request from you.",
            )
        return value

    def create(self, validated_data):
        user = self._user
        validated_data["sender"] = user
        return super().create(validated_data)
