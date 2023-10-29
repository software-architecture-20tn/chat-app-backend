INSTALLED_APPS = (
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.postgres",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "django_migrations_formatter.apps.MigrationsFormatter",
    "django_probes",
)

HEALTH_CHECK_APPS = (
    "health_check",                             # required
    "health_check.db",                          # stock Django health checkers
    "health_check.cache",
    "health_check.storage",
    "health_check.contrib.migrations",
    # "health_check.contrib.celery",              # requires celery
    # "health_check.contrib.celery_ping",         # requires celery
    # "health_check.contrib.psutil",              # disk and memory utilization; requires psutil
    # "health_check.contrib.s3boto3_storage",     # requires boto3 and S3BotoStorage backend
    # "health_check.contrib.rabbitmq",            # requires RabbitMQ broker
    # "health_check.contrib.redis",               # requires Redis broker
)

DEV_TOOLS = (
    "debug_toolbar",
)

DRF_PACKAGES = (
    "rest_framework",
    "drf_spectacular",
    "knox",
    # "django_filters",
    # "drf_standardized_errors",
    # "corsheaders",
)

THIRD_PARTY_APPS = (
    "imagekit",
    "corsheaders",
)

LOCAL_APPS = (
    "apps.core",
    "apps.users",
)

INSTALLED_APPS += DRF_PACKAGES + THIRD_PARTY_APPS + LOCAL_APPS + DEV_TOOLS + HEALTH_CHECK_APPS
