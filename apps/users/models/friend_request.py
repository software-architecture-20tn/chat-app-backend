from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class FriendRequest(BaseModel):
    sender = models.ForeignKey(
        verbose_name=_("Sender"),
        to="users.User",
        on_delete=models.CASCADE,
        related_name="friend_request_sent",
    )
    receiver = models.ForeignKey(
        verbose_name=_("Receiver"),
        to="users.User",
        on_delete=models.CASCADE,
        related_name="friend_request_received",
    )
    date_time_sent = models.DateTimeField(
        verbose_name=_("Date and time sent"),
        auto_now_add=True,
    )
    is_approved = models.BooleanField(
        verbose_name=_("Approved"),
        default=False,
    )

    class Meta:
        verbose_name = _("Friend request")
        verbose_name_plural = _("Friend requests")
        unique_together = ("sender", "receiver")

    def __str__(self) -> str:
        return f"Friend request from {self.sender} to {self.receiver}"
