import os

from dotenv import load_dotenv

load_dotenv()

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DATABASE_NAME", "my-database"),
        "USER": os.getenv("DATABASE_USER", "my-user"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD", "my-password"),
        "HOST": os.getenv("DATABASE_HOST", "localhost"),
        "PORT": os.getenv("DATABASE_PORT", "5432"),
    }
}

SAFE_DELETE_FIELD_NAME = "deleted_at"
