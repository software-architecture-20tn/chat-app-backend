from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Group(BaseModel):
    """Representation of a conversation group in database."""

    name = models.CharField(
        verbose_name=_("Group name"),
        max_length=30,
    )
    date_created = models.DateTimeField(
        verbose_name=_("Date created"),
        auto_now_add=True,
    )
    person_created = models.ForeignKey(
        to="users.User",
        on_delete=models.SET_NULL,
        related_name="created_groups",
        verbose_name=_("Person created"),
        null=True,
    )

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")

    def __str__(self) -> str:
        return f"{self.id} - {self.name}"
