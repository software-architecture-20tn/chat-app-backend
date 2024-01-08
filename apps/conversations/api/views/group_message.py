from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.conversations.models import GroupMember, Message

from ..serializers import GroupMessageSerializer


class GroupMessageListAPIView(ListAPIView):
    """View for listing direct messages."""

    permission_classes = (IsAuthenticated,)
    serializer_class = GroupMessageSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        # Get the `id` of the user from the URL.
        group_id = self.kwargs.get("group_id")
        return Message.objects.filter(group_id=group_id).order_by("-id")

    def get(self, request, *args, **kwargs):
        group_id = self.kwargs.get("group_id")
        # Check if the user is a member of the group.
        group_member = GroupMember.objects.filter(
            group_id=group_id,
            member=request.user,
        ).first()
        if not group_member:
            return Response(
                {"detail": "You are not a member of this group."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().get(request, *args, **kwargs)


class GroupMessageCreateAPIView(CreateAPIView):
    """View for listing direct messages."""

    permission_classes = (IsAuthenticated,)
    serializer_class = GroupMessageSerializer
