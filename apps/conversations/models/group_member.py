from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class GroupMember(BaseModel):
    """Represent the relation between a group and a member."""

    group = models.ForeignKey(
        to="conversations.Group",
        on_delete=models.CASCADE,
        related_name="members",
        verbose_name=_("Group"),
    )
    member = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        related_name="joined_groups",
        verbose_name=_("Member"),
    )

    class Meta:
        verbose_name = _("Group member")
        verbose_name_plural = _("Group members")
        unique_together = ("group", "member")

    def __str__(self) -> str:
        return f"{self.group} - {self.member}"
