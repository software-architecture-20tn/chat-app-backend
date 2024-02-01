from rest_framework import serializers

from apps.conversations.models import GroupMember, Message
from apps.core.api.serializers import BaseModelSerializer


class GroupMessageSerializer(BaseModelSerializer):
    """Serializer for managing conversations."""

    conversation_name = serializers.SerializerMethodField(read_only=True)
    sender_username = serializers.CharField(
        source="sender.username",
        read_only=True,
    )
    sender_first_name = serializers.CharField(
        source="sender.first_name",
        read_only=True,
    )
    sender_last_name = serializers.CharField(
        source="sender.last_name",
        read_only=True,
    )
    sender_avatar = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            "id",
            "sender",
            "sender_username",
            "sender_first_name",
            "sender_last_name",
            "sender_avatar",
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

    def get_sender_avatar(self, message: Message) -> str | None:
        if not message.sender:
            return ""
        if not message.sender.avatar:
            return None
        return message.sender.avatar.url

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
