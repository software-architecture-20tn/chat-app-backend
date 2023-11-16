from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, Group, Permission,
                                        PermissionsMixin)
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit import models as imagekitmodels
from imagekit.processors import ResizeToFill, Transpose

from apps.core.models import BaseModel

from ..managers import UserManager


class User(
    AbstractBaseUser,
    PermissionsMixin,
    BaseModel,
):
    """Custom user model with username.

    Attrs:
        first_name: first name of the user
        last_name: last name of the user
        email: email of the user, must be unique
        phone_number: phone number of the user, must be unique
        date_of_birth: date of birth of the user

    """

    username = models.CharField(
        verbose_name=_("Username"),
        max_length=30,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name=_("First name"),
        max_length=30,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name=_("Last name"),
        max_length=30,
        blank=True,
    )
    email = models.EmailField(
        verbose_name=_("Email address"),
        max_length=254,  # to be compliant with RFCs 3696 and 5321
        unique=True,
    )
    date_of_birth = models.DateField(
        verbose_name=_("Date of birth"),
        null=True,
    )
    is_staff = models.BooleanField(
        verbose_name=_("Staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site.",
        ),
    )
    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active.",
        ),
    )
    avatar = imagekitmodels.ProcessedImageField(
        verbose_name=_("Avatar"),
        blank=True,
        null=True,
        upload_to=settings.DEFAULT_MEDIA_FILE_PATH,
        max_length=512,
        processors=[Transpose()],
        options={
            "quality": 100,
        },
    )
    avatar_thumbnail = imagekitmodels.ImageSpecField(
        source="avatar",
        processors=[
            ResizeToFill(50, 50),
        ],
    )
    bio = models.TextField(
        verbose_name=_("Bio"),
        blank=True,
        null=True,
    )
    groups = models.ManyToManyField(
        verbose_name=_("groups"),
        related_name="custom_users",
        blank=True,
        help_text=_("The groups this user belongs to."),
        related_query_name="custom_user",
        to=Group,
    )
    user_permissions = models.ManyToManyField(
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="users_user_permissions",
        related_query_name="users_user_permission",
        to=Permission,
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self) -> str:
        # pylint: disable=invalid-str-returned
        return self.email
