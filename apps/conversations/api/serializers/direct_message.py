from django.db.models import Q

from rest_framework import serializers

from apps.conversations.models import Message
from apps.core.api.serializers import BaseModelSerializer
from apps.users.models import Friendship


class DirectMessageListSerializer(BaseModelSerializer):
    """Serializer for managing conversations."""

    avatar = serializers.SerializerMethodField()
    conversation_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            "id",
            "sender",
            "receiver",
            "time",
            "content",
            "media",
            "avatar",
            "conversation_name",
        )

    def get_avatar(self, message: Message) -> str | None:
        """Get the avatar of the message."""
        if not message.receiver:
            return None  # This is to bypass the type checker
        if message.sender == self._user and message.receiver.avatar:
            return message.receiver.avatar.url
        if message.sender.avatar:
            return message.sender.avatar.url
        return None

    def get_conversation_name(self, message: Message) -> str:
        """Get the conversation name of the message."""
        if not message.receiver:
            return ""
        if message.sender == self._user:
            return message.receiver.username
        return message.sender.username


class DirectMessageCreateSerializer(BaseModelSerializer):
    """Serializer for managing conversations."""

    class Meta:
        model = Message
        fields = (
            "id",
            "sender",
            "receiver",
            "content",
            "media",
            "time",
        )
        extra_kwargs = {
            "time": {"read_only": True},
        }

    def validate(self, attrs):
        """Validate the serializer."""
        if attrs.get("group"):
            raise serializers.ValidationError(
                "A direct message cannot have a group."
            )
        receiver = attrs.get("receiver")
        if not receiver:
            raise serializers.ValidationError(
                "A direct message must have a receiver."
            )
        if not Friendship.objects.filter(
            Q(user1=self._user, user2=receiver)
            | Q(user1=receiver, user2=self._user),
        ).exists():
            raise serializers.ValidationError(
                "You are not friends with this user."
            )
        return super().validate(attrs)
