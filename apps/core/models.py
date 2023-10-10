from django.db import models


# https://thetldr.tech/how-to-use-base-model-inheritance-in-django/
class BaseModel(models.Model):
    """A model with created_at and updated_at fields."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
