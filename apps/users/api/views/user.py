from rest_framework import mixins
from rest_framework.permissions import IsAdminUser

from apps.core.api.views import BaseViewSet, ReadOnlyViewSet
from apps.users.models import User
from django.db.models import Q

from ..serializers import UserSerializer


class UserViewSet(
    mixins.ListModelMixin,
    BaseViewSet,
):
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()


class FriendListView(ReadOnlyViewSet):
    serializer_class = UserSerializer
    serializers_map = {
        "list": UserSerializer,
        "retrieve": UserSerializer,
        "default": UserSerializer,
    }
    queryset = User.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            Q(friendship_user1__user2=self.request.user)
            | Q(friendship_user2__user1=self.request.user),
        )
