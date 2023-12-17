from rest_framework import serializers

from apps.conversations.models import Message
from apps.core.api.serializers import BaseModelSerializer


class ConversationSerializer(BaseModelSerializer):
    """Serializer for managing conversations."""

    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            "id",
            "sender",
            "receiver",
            "group",
            "date",
            "content",
            "media",
            "avatar",
        )

    def get_avatar(self, message: Message) -> str:
        """Get the avatar of the message."""
        if message.group:
            return None
        if message.sender == self._user and message.receiver.avatar:
            return message.receiver.avatar.url
        if message.sender.avatar:
            return message.sender.avatar.url
        return None
