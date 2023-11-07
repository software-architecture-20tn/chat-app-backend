from apps.core.api.serializers import BaseModelSerializer
from apps.users.models import User


class UserProfileSerializer(BaseModelSerializer):
    """Serializer for user profile."""

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "date_of_birth",
            "avatar",
            "bio",
        )
        extra_kwargs = {
            "email": {"read_only": True},
        }
