from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    """Provide a base serializer."""

    def __init__(self, *args, **kwargs):
        """Set the current user to the context."""
        super().__init__(*args, **kwargs)
        self._user = getattr(self.context.get("request"), "user", None)

    @property
    def _meta(self):
        """Get Meta class."""
        return self.Meta

    def create(self, validated_data) -> None:
        """Bypass create method."""

    def update(self, instance, validated_data):
        """Bypass update method."""


class BaseModelSerializer(serializers.ModelSerializer, BaseSerializer):
    """Base serializer for model."""
