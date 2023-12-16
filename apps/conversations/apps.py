from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MessagesAppConfig(AppConfig):
    """Default configuration for Messages app."""

    name = "apps.conversations"
    verbose_name = _("Messages")
