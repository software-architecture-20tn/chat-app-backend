from rest_framework import serializers

from apps.core.api.serializers import BaseSerializer


class PasswordChangeSerializer(BaseSerializer):
    """Serializer for password change."""

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
