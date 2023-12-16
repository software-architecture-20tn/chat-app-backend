import re

from django.db.models import Q

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from apps.core.api.views import BaseViewSet, ReadOnlyViewSet
from apps.users.models import User

from ..serializers import UserSearchSerializer, UserSerializer


class UserViewSet(
    mixins.ListModelMixin,
    BaseViewSet,
):
    serializer_class = UserSerializer
    serializers_map = {
        "search": UserSearchSerializer,
        "default": UserSerializer,
    }
    permission_classes = (IsAuthenticated,)
    permissions_map = {
        "search": (IsAuthenticated,),
        "default": (IsAdminUser,),
    }
    queryset = User.objects.all()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="keyword",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Enter the keyword to search for",
                required=True,
            ),
        ]
    )
    @action(detail=False, methods=["get"])
    def search(self, request):
        """Search for users.

        Search for user by keyword in username, email, first_name, last_name.
        Each keyword is separated by comma, semicolon or space.

        """
        keyword = request.query_params.get("keyword", "")

        tokens = re.split("[,;\s]", keyword)

        # remove empty tokens
        tokens = [token for token in tokens if token]

        query = Q()
        for token in tokens:
            query |= (
                Q(username__icontains=token)
                | Q(email__icontains=token)
                | Q(first_name__icontains=token)
                | Q(last_name__icontains=token)
            )

        users = User.objects.filter(query)
        serializer = UserSearchSerializer(users, many=True)
        return Response(serializer.data)
