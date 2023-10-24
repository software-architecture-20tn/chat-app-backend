# https://github.com/tfranzel/drf-spectacular/
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "knox.auth.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication"
    ),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Chat App API",
    "DESCRIPTION": "A Telegram Clone",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}