from django.contrib.auth.models import AnonymousUser

from rest_framework import mixins

from apps.core.api.mixins import UpdateModelOnlyPutMixin
from apps.core.api.views import BaseViewSet
from apps.users.models import User

from ..serializers import UserProfileSerializer


class ProfileViewSet(
    mixins.RetrieveModelMixin,
    UpdateModelOnlyPutMixin,
    BaseViewSet,
):
    """ViewSet for user profile."""

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    search_fields = ()
    ordering_fields = ()

    def get_object(self) -> User | AnonymousUser:
        """Return the current user."""
        return self.request.user
