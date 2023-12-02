from django.db.models import Q
from rest_framework import mixins, response, status

from apps.core.api.views import BaseViewSet
from apps.users.models import Friendship, User

from ..serializers import CloseFriendAddSerializer, CloseFriendListSerializer


class CloseFriendViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    BaseViewSet,
):
    """Viewset for managing close friends."""

    serializer_class = CloseFriendListSerializer
    serializers_map = {
        "create": CloseFriendAddSerializer,
        "default": CloseFriendListSerializer,
    }
    queryset = User.objects.all()

    def get_queryset(self):
        close_friend_ids = Friendship.objects.filter(
            Q(user1=self.request.user) | Q(user2=self.request.user),
            is_close=True,
        ).values_list("user1_id", "user2_id")
        # Unpack the tuple into a list, then flatten it, then remove duplicates
        close_friend_ids = list(set(sum(close_friend_ids, ())))
        return User.objects.filter(id__in=close_friend_ids)

    def create(self, request, *args, **kwargs):
        """Update the Friendship.

        Set `is_close` to True if the Friendship exists,

        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        close_friend_id = serializer.validated_data["close_friend_id"]
        friendship = Friendship.objects.filter(
            Q(user1=request.user, user2=close_friend_id)
            | Q(user1=close_friend_id, user2=request.user),
        )
        if not friendship.exists():
            return response.Response(
                {"detail": "Friendship does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        friendship = friendship.first()
        friendship.is_close = True
        friendship.save()
        return response.Response(
            self.get_serializer(friendship).data,
            status=status.HTTP_201_CREATED,
        )

    def perform_create(self, serializer) -> None:
        """Do nothing."""

    def destroy(self, request, *args, **kwargs):
        """Set `is_close` to False."""
        friendship = Friendship.objects.filter(
            Q(user1=request.user, user2=self.get_object())
            | Q(user1=self.get_object(), user2=request.user),
        )
        if not friendship.exists():
            return response.Response(
                {"detail": "Friendship does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        friendship = friendship.first()
        friendship.is_close = False
        friendship.save()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
