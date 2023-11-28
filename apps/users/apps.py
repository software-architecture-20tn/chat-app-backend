# pylint: disable=unused-import
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersAppConfig(AppConfig):
    """Default configuration for Users app."""

    name = "apps.users"
    verbose_name = _("Users")

    def ready(self) -> None:
        from . import signals
        from .api.auth import scheme  # noqa: F401
