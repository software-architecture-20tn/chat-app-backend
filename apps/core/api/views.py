# https://github.com/defineimpossible/django-rest-batteries/blob/master/rest_batteries/viewsets.py
from collections.abc import Sequence
from typing import Iterable

from rest_framework import mixins
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import GenericViewSet

from . import mixins as custom_mixins


class BaseViewSet(GenericViewSet):
    """Provide a base viewset."""

    base_permission_classes = (IsAuthenticated,)
    permission_classes: Sequence[type[BasePermission]] = ()
    permissions_map: dict[
        str, type[BasePermission] | Iterable[type[BasePermission]]
    ] | None = None
    serializer_class = None
    serializers_map: dict[str, type[BaseSerializer]] | None = None

    def get_viewset_permissions(self) -> list[BasePermission]:
        """Combine `base_permission_classes` and `permission_classes`."""
        if hasattr(self, "permission_classes"):
            permission_classes = self.permission_classes
            extra_permission_classes = tuple(
                permission_class
                for permission_class in permission_classes
                if permission_class not in self.base_permission_classes
            )

        permission_classes = (
            self.base_permission_classes + extra_permission_classes
        )
        return [permission() for permission in permission_classes]

    def get_permissions_from_action(
        self,
        action: str,
    ) -> list[BasePermission]:
        """Return permission classes from action name."""
        return [permission() for permission in self.permissions_map.get(action)]

    def get_permissions(self):
        permissions = super().get_permissions()
        if hasattr(self, "get_viewset_permissions"):
            permissions = self.get_viewset_permissions()

        if not isinstance(self.permissions_map, dict):
            return permissions

        if self.action in self.permissions_map:
            return self.get_permissions_from_action(self.action)

        if self.action == "partial_update" and "update" in self.permissions_map:
            return self.get_permissions_from_action("update")

        if "default" in self.permissions_map:
            return self.get_permissions_from_action("default")

        return permissions

    def get_serializer_class(self):
        """Return serializer class."""
        serializer_class = super().get_serializer_class()

        if not isinstance(self.serializers_map, dict):
            return serializer_class

        if self.action in self.serializers_map:
            return self.serializers_map.get(self.action)

        if self.action == "partial_update" and "update" in self.serializers_map:
            return self.serializers_map.get("update")

        if "default" in self.serializers_map:
            return self.serializers_map.get("default")

        return serializer_class


class CRUDViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    custom_mixins.UpdateModelOnlyPutMixin,
    mixins.DestroyModelMixin,
    BaseViewSet,
):
    """Provide a CRUD viewset."""


class ReadOnlyViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    BaseViewSet,
):
    """Provide a read-only viewset."""
