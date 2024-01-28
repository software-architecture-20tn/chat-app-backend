from typing import Any

from django.contrib import admin
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _


# pylint: disable=no-member
class BaseAdmin(admin.ModelAdmin):
    """Base Admin for model management."""

    def get_fieldsets(  # type: ignore
        self,
        request: HttpRequest,
        obj: Any | None = ...,
    ) -> list[tuple[str | None, dict]]:
        """Add created_at and updated_at to fieldsets."""
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets += (  # type: ignore
            (
                _("Updated history"),
                {
                    "fields": (
                        "created_at",
                        "updated_at",
                    ),
                },
            ),
        )
        return fieldsets  # type: ignore

    def get_readonly_fields(
        self,
        request: HttpRequest,
        obj: Any | None = ...,
    ) -> list[str] | tuple[Any, ...]:
        read_only_fields = super().get_readonly_fields(request, obj)
        read_only_fields += (
            "created_at",
            "updated_at",
        )

        if (
            not hasattr(self, "create_only_fields")
            or not self.create_only_fields
            or not obj
        ):
            return read_only_fields

        return read_only_fields + self.create_only_fields
