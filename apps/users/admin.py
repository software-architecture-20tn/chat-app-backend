from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from ..core.admin import BaseAdmin
from .models import Friendship, User, FriendRequest


@admin.register(Friendship)
class FriendshipAdmin(BaseAdmin):
    ordering = ("id",)
    list_display = (
        "id",
        "user1_id",
        "user2_id",
    )


@admin.register(FriendRequest)
class FriendRequestAdmin(BaseAdmin):
    ordering = ("id",)
    list_display = (
        "id",
        "sender_id",
        "receiver_id",
        "is_approved",
    )


@admin.register(User)
class UserAdmin(BaseAdmin, BaseUserAdmin):
    """UI for User model."""

    ordering = ("id",)
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
    )
    list_display_links = (
        "email",
    )
    search_fields = (
        "first_name",
        "last_name",
        "email",
    )
    add_fieldsets = (
        (
            None, {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )
    fieldsets = (
        (
            None, {
                "fields": (
                    "email",
                    "password",
                ),
            },
        ),
        (
            _("Personal info"), {
                "fields": (
                    "first_name",
                    "last_name",
                    "avatar",
                ),
            },
        ),
        (
            _("Permissions"), {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
