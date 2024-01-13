from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.conversations.api.serializers import (
    GroupAddMemberSerializer,
    GroupCreationSerializer,
    GroupRemoveMemberSerializer,
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
    """ViewSet for managing Group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    serializers_map = {
        "create": GroupCreationSerializer,
        "update": GroupSerializer,
        "add_members": GroupAddMemberSerializer,
        "remove_members": GroupRemoveMemberSerializer,
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

    @action(detail=True, methods=["post"], url_path="add-members")
    def add_members(self, request, *args, **kwargs):
        """Add members to a group."""
        group = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(instance=group)
        return Response(
            {"message": "Members added successfully"},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="remove-members")
    def remove_members(self, request, *args, **kwargs):
        """Remove members from a group."""
        group = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(instance=group)
        return Response(
            {"message": "Members removed successfully"},
            status=status.HTTP_200_OK,
        )
