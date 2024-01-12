# from django.contrib.auth.models import AnonymousUser

from rest_framework import mixins, status
from rest_framework.response import Response

from apps.core.api.mixins import UpdateModelOnlyPutMixin
from apps.core.api.views import CRUDViewSet
from apps.core.api.views import BaseViewSet
from apps.conversations.models import Group, GroupMember
from apps.conversations.api.serializers import GroupSerializer, GroupCreationSerializer
from apps.users.models import User

from rest_framework.permissions import IsAuthenticated


class GroupViewSet(
    # mixins.ListModelMixin,
    # mixins.CreateModelMixin,
    # # mixins.RetrieveModelMixin,
    # mixins.DestroyModelMixin,
    # UpdateModelOnlyPutMixin,
    CRUDViewSet,
    BaseViewSet,
):
    """ViewSet for group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    serializers_map = {
        "create": GroupCreationSerializer,
        "update": GroupSerializer,
        "destroy": GroupSerializer,
        "default": GroupSerializer,
    }
    # search_fields = ()
    # ordering_fields = ()

    def create(self, request, *args, **kwargs):
        """Create a new group with the current user and specified friends."""
        friend_ids = request.data.get("friend_ids")
        if not friend_ids:
            return Response(
                {"message": "You must specify friends to create a new group"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        friends = User.objects.filter(id__in=friend_ids, friends=request.user)
        if len(friends) != len(friend_ids):
            return Response(
                {"message": "Some users are not your friends"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        group = Group.objects.create(name=request.data.get("name"))
        # Add the current user to the GroupMember table
        GroupMember.objects.create(member=request.user, group=group)

        # Add each friend to the GroupMember table
        for friend in friends:
            GroupMember.objects.create(member=friend, group=group)
        
        serializer = self.get_serializer(group)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
        if group.creator != request.user:
            return Response(
                {"message": "You are not the creator of this group"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().destroy(request, *args, **kwargs)
