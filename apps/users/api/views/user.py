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
