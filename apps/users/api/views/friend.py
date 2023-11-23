from apps.core.api.views import ReadOnlyViewSet
from apps.users.models import User
from django.db.models import Q

from ..serializers import UserSerializer, FriendSerializer


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
