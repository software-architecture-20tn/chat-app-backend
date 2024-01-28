from rest_framework import serializers

from apps.conversations.models import GroupMember, Message
from apps.core.api.serializers import BaseModelSerializer


class GroupMessageSerializer(BaseModelSerializer):
    """Serializer for managing conversations."""

    conversation_name = serializers.SerializerMethodField(read_only=True)

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
        extra_kwargs = {
            "time": {"read_only": True},
        }

    def get_conversation_name(self, message: Message) -> str:
        if not message.group:
            return ""  # This is to bypass the type checker
        return message.group.name

    def validate(self, attrs):
        """Validate the serializer."""
        if attrs.get("receiver"):
            raise serializers.ValidationError(
                "A group message cannot have a receiver."
            )
        group = attrs.get("group")
        if not group:
            raise serializers.ValidationError(
                "A group message must have a group."
            )
        if not GroupMember.objects.filter(
            group=group,
            member=self._user,
        ).exists():
            raise serializers.ValidationError(
                "You are not a member of this group."
            )
        return super().validate(attrs)
