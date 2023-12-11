from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Message(BaseModel):
    """Representation of a message in database."""

    sender = models.ForeignKey(
        to="users.User",
        on_delete=models.SET_NULL,
        related_name="sent_messages",
        verbose_name=_("Sender"),
        null=True,
    )
    receiver = models.ForeignKey(
        to="users.User",
        on_delete=models.SET_NULL,
        related_name="received_messages",
        verbose_name=_("Receiver"),
        null=True,
    )
    group = models.ForeignKey(
        to="conversations.Group",
        on_delete=models.SET_NULL,
        related_name="messages",
        verbose_name=_("Group"),
        null=True,
    )
    date = models.DateTimeField(
        verbose_name=_("Date"),
        auto_now_add=True,
    )
    content = models.TextField(
        verbose_name=_("Content"),
        blank=True,
    )
    media = models.FileField(
        verbose_name=_("Media"),
        upload_to=settings.DEFAULT_MEDIA_FILE_PATH,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def __str__(self) -> str:
        return f"{self.id} - {self.sender} - {self.receiver} - {self.group}"

    def clean(self) -> None:
        """Clean the model.

        Verify that the message has a receiver or a group.
        Verify that the message has a content or a media.

        """
        if not self.receiver and not self.group:
            raise models.ValidationError(
                _("A message must have a receiver or a group.")
            )
        if not self.content and not self.media:
            raise models.ValidationError(
                _("A message must have a content or a media.")
            )
        return super().clean()
