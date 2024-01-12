from django.db.models import Q

from rest_framework import response, status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from apps.conversations.models import Message
from apps.users.models import User

from ..serializers import (
    DirectMessageCreateSerializer,
    DirectMessageListSerializer,
)


class DirectMessageListAPIView(ListAPIView):
    """View for listing direct messages."""

    permission_classes = (IsAuthenticated,)
    serializer_class = DirectMessageListSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        # Get the `id` of the user from the URL.
        user_id = self.kwargs.get("receiver_id")
        current_user = self.request.user
        target_user = User.objects.filter(id=user_id).first()
        if not target_user:
            return response.Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Get the messages between the two users.
        return Message.objects.filter(
            Q(sender=current_user, receiver=target_user)
            | Q(sender=target_user, receiver=current_user),
        ).order_by("-id")


class DirectMessageCreateAPIView(CreateAPIView):
    """View for listing direct messages."""

    permission_classes = (IsAuthenticated,)
    serializer_class = DirectMessageCreateSerializer

    def post(self, request, *args, **kwargs):
        """Create a new direct message."""
        data = request.data
        data["sender"] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )
