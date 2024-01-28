# https://github.com/cookiecutter/cookiecutter-django/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/%7B%7Bcookiecutter.project_slug%7D%7D/users/managers.py
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as DjangoUserManager


# pylint: disable=arguments-differ,arguments-renamed
class UserManager(DjangoUserManager):
    """Custom manager for the User model."""

    def _create_user(
        self,
        username: str,
        email: str | None = None,
        password: str | None = None,
        **extra_fields,
    ):
        """Create and save a user with email, username, and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.password = make_password(password)  # type: ignore
        user.save(using=self._db)
        return user

    def create_user(
        self,
        username: str,
        email: str | None = None,
        password: str | None = None,
        **extra_fields,
    ):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(
            email=email,
            username=username,
            password=password,
            **extra_fields,
        )

    def create_superuser(  # type: ignore
        self,
        email: str,
        password: str | None = None,
        **extra_fields,
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        username = email
        return self._create_user(
            email=email,
            password=password,
            username=username,
            **extra_fields,
        )
