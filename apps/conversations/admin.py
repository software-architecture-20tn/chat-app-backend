from django.contrib import admin

from apps.core.admin import BaseAdmin

from .models import Group, GroupAdmin, GroupMember, Message


@admin.register(GroupAdmin)
class GroupAdminManager(BaseAdmin):
    """Admin UI for `GroupAdmin` model."""

    list_display = (
        "group",
        "admin",
    )
    list_display_links = (
        "group",
        "admin",
    )
    search_fields = (
        "group__name",
        "admin__email",
    )


@admin.register(GroupMember)
class GroupMemberManager(BaseAdmin):
    """Admin UI for `GroupMember` model."""

    list_display = (
        "group",
        "member",
    )
    list_display_links = (
        "group",
        "member",
    )
    search_fields = (
        "group__name",
        "member__email",
    )


@admin.register(Group)
class GroupManager(BaseAdmin):
    """Admin UI for `Group` model."""

    list_display = (
        "name",
        "created_at",
        "person_created",
    )
    list_display_links = (
        "name",
        "created_at",
        "person_created",
    )
    search_fields = (
        "name",
        "person_created__email",
    )


@admin.register(Message)
class MessageManager(BaseAdmin):
    """Admin UI for `Message` model."""

    list_display = (
        "id",
        "content",
        "time",
        "sender",
        "receiver",
        "group",
    )
    list_display_links = ("id",)
    search_fields = (
        "content",
        "sender__email",
        "receiver__email",
    )
