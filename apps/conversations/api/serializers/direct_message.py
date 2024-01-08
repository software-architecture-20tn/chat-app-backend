from rest_framework import serializers

from apps.conversations.models import Message
from apps.core.api.serializers import BaseModelSerializer


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

    def get_avatar(self, message: Message) -> str:
        """Get the avatar of the message."""
        if message.sender == self._user and message.receiver.avatar:
            return message.receiver.avatar.url
        if message.sender.avatar:
            return message.sender.avatar.url
        return None

    def get_conversation_name(self, message: Message) -> str:
        if message.sender == self._user:
            return message.receiver.username
        return message.sender.username


class DirectMessageCreateSerializer(BaseModelSerializer):
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
