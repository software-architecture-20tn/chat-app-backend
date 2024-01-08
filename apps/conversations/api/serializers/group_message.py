from rest_framework import serializers

from apps.conversations.models import Message
from apps.core.api.serializers import BaseModelSerializer


class GroupMessageSerializer(BaseModelSerializer):
    """Serializer for managing conversations."""

    conversation_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            "id",
            "sender",
            "group",
            "time",
            "content",
            "media",
            "conversation_name",
        )

    def get_conversation_name(self, message: Message) -> str:
        return message.group.name
