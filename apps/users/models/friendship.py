from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Friendship(BaseModel):
    user1 = models.ForeignKey(
        verbose_name=_("User 1"),
        to="users.User",
        on_delete=models.CASCADE,
        related_name="friendship_user1",
    )
    user2 = models.ForeignKey(
        verbose_name=_("User 2"),
        to="users.User",
        on_delete=models.CASCADE,
        related_name="friendship_user2",
    )
    date = models.DateField(auto_now_add=True)
    is_close = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Friendship")
        verbose_name_plural = _("Friendships")
        unique_together = ("user1", "user2")

    def __str__(self) -> str:
        return f"Friendship between {self.user1} and {self.user2}"
