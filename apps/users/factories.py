import uuid

import factory
from django.conf import settings

from .models import User


class UserFactory(factory.django.DjangoModelFactory):
    """Generate an instance of the User model."""

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    avatar = factory.django.ImageField()
    # https://www.appsloveworld.com/django/100/124/unknown-password-hashing-algorithm-password-hashers-setting-using-factory-boy
    password = factory.PostGenerationMethodCall(
        "set_password",
        "P455W0rd",
    )

    class Meta:
        model = User

    # https://www.appsloveworld.com/django/100/20/how-to-use-lazy-attribute-with-faker-in-factory-boy
    @factory.lazy_attribute
    def email(self) -> str:
        """Fake a uuid4 email."""
        return f"{uuid.uuid4()}@example.com"


class SuperUserFactory(UserFactory):
    """Generate an instance of the User model with superuser permissions."""

    is_staff = True
    is_superuser = True

    class Meta:
        model = User
