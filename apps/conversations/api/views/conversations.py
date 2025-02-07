from django.db.models import Q

from rest_framework import response, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from apps.conversations.models import Group, Message

from ..serializers import ConversationSerializer


class ConversationListAPIView(GenericAPIView):
    """View for listing conversations."""

    permission_classes = (IsAuthenticated,)
    serializer_class = ConversationSerializer

    def get_queryset(self):
        """Get the list of conversations."""
        if getattr(self, "swagger_fake_view", False):
            # queryset just for schema generation metadata
            return Message.objects.none()
        # Get all group that the user is a member of.
        group_ids = self.request.user.joined_groups.all().values_list(
            "group_id",
        )
        groups = Group.objects.filter(id__in=group_ids)
        # For each group, get the last message.
        last_messages = []
        for group in groups:
            last_messages.append(group.messages.last())
        # Append messages from other user, which are a private conversation,
        # not a group
        senders_and_receivers = Message.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user),
            group=None,
        ).values_list("sender", "receiver")
        # Remove duplicates
        senders_and_receivers = list(set(senders_and_receivers))
        # Remove the symmetrical conversation
        for sender, receiver in senders_and_receivers:
            if (receiver, sender) in senders_and_receivers:
                senders_and_receivers.remove((receiver, sender))
        # For each sender and receiver, get the last message.
        for sender, receiver in senders_and_receivers:
            last_messages.append(
                Message.objects.filter(
                    Q(sender=sender, receiver=receiver)
                    | Q(sender=receiver, receiver=sender),
                ).last(),
            )
        # Remove None values
        last_messages = list(filter(None, last_messages))
        # Sort by date
        last_messages.sort(key=lambda x: x.time, reverse=True)
        return Message.objects.filter(
            id__in=[message.id for message in last_messages],
        ).order_by("-id")

    @extend_schema(
        responses={
            status.HTTP_200_OK: ConversationSerializer(many=True),
        },
    )
    def get(self, request, *args, **kwargs) -> response.Response:
        """Get the list of conversations."""
        queryset = self.get_queryset()
        serializer = ConversationSerializer(
            queryset,
            many=True,
            context={"request": request},
        )
        return response.Response(serializer.data, status=status.HTTP_200_OK)
