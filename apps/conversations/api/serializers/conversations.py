from rest_framework import serializers

from apps.conversations.models import Message
from apps.core.api.serializers import BaseModelSerializer


class ConversationSerializer(BaseModelSerializer):
    """Serializer for managing conversations."""

    avatar = serializers.SerializerMethodField()
    conversation_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            "id",
            "sender",
            "receiver",
            "group",
            "time",
            "content",
            "media",
            "avatar",
            "conversation_name",
        )

    def get_avatar(self, message: Message) -> str | None:
        """Get the avatar of the message."""
        if message.group:
            return None
        if not message.receiver:
            return None  # This is to bypass the type checker
        if message.sender == self._user and message.receiver.avatar:
            return message.receiver.avatar.url
        if message.sender.avatar:
            return message.sender.avatar.url
        return None

    def get_conversation_name(self, message: Message) -> str:
        if message.group:
            return message.group.name
        if message.sender == self._user and message.receiver:
            return message.receiver.username
        return message.sender.username
