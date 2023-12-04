from django.db.models import Q
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
from rest_framework import serializers

from apps.core.api.serializers import BaseModelSerializer
from apps.users.models import FriendRequest, Friendship, User


class FriendSerializer(BaseModelSerializer):
    """Serializer for the Friend model."""

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "avatar",
            "username",
        )
        read_only_fields = ("id",)


class FriendRequestSerializer(BaseModelSerializer):
    class Meta:
        model = FriendRequest
        fields = (
            "id",
            "sender",
            "receiver",
            "date_time_sent",
            "is_approved",
        )
        read_only_fields = (
            "id",
            "sender",
            "is_approved",
        )

    def create(self, validated_data):
        """Check the availability to create a new friend request.
        
        Check if the receiver is already a friend.
        or the receiver is already sent a friend request.
        
        """

        user = self._user
        if Friendship.objects.filter(
            Q(user1=validated_data["receiver"], user2=user)
            | Q(user2=validated_data["receiver"], user1=user)
        ).exists():
            raise serializers.ValidationError(
                "The receiver is already a friend.",
            )
        if FriendRequest.objects.filter(Q(sender=validated_data["receiver"])).exists():
            raise serializers.ValidationError(
                "The receiver already sent a friend request.",
            )
        validated_data["sender"] = user
        return super().create(validated_data)
