from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class GroupAdmin(BaseModel):
    """Represent the relation between a group and an admin."""

    group = models.ForeignKey(
        to="conversations.Group",
        on_delete=models.CASCADE,
        related_name="admins",
        verbose_name=_("Group"),
    )
    admin = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        related_name="managed_groups",
        verbose_name=_("Admin"),
    )

    class Meta:
        verbose_name = _("Group admin")
        verbose_name_plural = _("Group admins")
        unique_together = ("group", "admin")

    def __str__(self) -> str:
        return f"{self.group} - {self.admin}"
