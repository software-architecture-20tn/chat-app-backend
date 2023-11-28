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
)

DEV_TOOLS = (
    "debug_toolbar",
)

DRF_PACKAGES = (
    "rest_framework",
    "drf_spectacular",
    "knox",
    "django_rest_passwordreset",
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

INSTALLED_APPS += (
    DRF_PACKAGES
    + THIRD_PARTY_APPS
    + LOCAL_APPS
    + DEV_TOOLS
    + HEALTH_CHECK_APPS
)
