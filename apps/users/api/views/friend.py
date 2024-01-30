from django.db.models import Q

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from apps.core.api.views import BaseViewSet, ReadOnlyViewSet
from apps.users.models import FriendRequest, Friendship, User

from ..serializers import (
    FriendRequestSerializer,
    FriendSerializer,
    UserSerializer,
)


class FriendViewSet(ReadOnlyViewSet):
    serializer_class = UserSerializer
    serializers_map = {
        "list": UserSerializer,
        "retrieve": FriendSerializer,
        "default": UserSerializer,
    }
    queryset = User.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            Q(friendship_user1__user2=self.request.user)
            | Q(friendship_user2__user1=self.request.user),
        )


class FriendRequestViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    BaseViewSet,
):
    serializer_class = FriendRequestSerializer

    queryset = FriendRequest.objects.all()

    @extend_schema(
        request=None,  # Indicate that the request body is empty
    )
    @action(detail=True, methods=["post"])
    def accept(self, request, pk):
        qs = self.get_object()
        if qs.receiver != self.request.user:
            return Response(status=403)
        if qs.is_approved:
            return Response(
                status=400,
                data={
                    "message": "Friend request already approved.",
                },
            )
        qs.is_approved = True
        qs.save()
        Friendship.objects.create(user1=qs.sender, user2=qs.receiver)

        return Response()

    def create(self, request, *args, **kwargs):
        if request.data.get("receiver") == request.user.pk:
            return Response(
                status=400,
                data={
                    "message": "The receiver can't be the same as the sender.",
                },
            )
        if not User.objects.filter(pk=request.data.get("receiver")).exists():
            return Response(
                status=400,
                data={
                    "message": "The receiver doesn't exist.",
                },
            )
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        # list all friend requests sended to the current user but not accepted
        return (
            super()
            .get_queryset()
            .filter(
                receiver=self.request.user,
                is_approved=False,
            ).order_by("-date_time_sent")
        )
