from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.conversations.api.serializers import (
    GroupCreationSerializer,
    GroupSerializer,
)
from apps.conversations.models import Group
from apps.core.api.mixins import UpdateModelOnlyPutMixin
from apps.core.api.views import BaseViewSet


class GroupViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    UpdateModelOnlyPutMixin,
    BaseViewSet,
):
    """ViewSet for group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    serializers_map = {
        "create": GroupCreationSerializer,
        "update": GroupSerializer,
        "default": GroupSerializer,
    }
    search_fields = ()
    ordering_fields = ()

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                members__member=self.request.user,
            )
        )

    def update(self, request, *args, **kwargs):
        """Allow only the creator of a group to update it."""
        group = self.get_object()
        if group.person_created != request.user:
            return Response(
                {"message": "You are not the creator of this group"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Allow only the creator of a group to delete it."""
        group = self.get_object()
        if group.person_created != request.user:
            return Response(
                {"message": "You are not the creator of this group"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().destroy(request, *args, **kwargs)
