# https://github.com/tfranzel/drf-spectacular/
# https://django-filter.readthedocs.io/en/latest/guide/rest_framework.html
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "knox.auth.TokenAuthentication",
        # "rest_framework.authentication.SessionAuthentication"
    ),
    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.LimitOffsetPagination"
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Connect API",
    "DESCRIPTION": "A modern messaging application.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
