# https://github.com/tfranzel/drf-spectacular/issues/264
from drf_spectacular.extensions import OpenApiAuthenticationExtension


class KnoxTokenScheme(OpenApiAuthenticationExtension):
    target_class = "knox.auth.TokenAuthentication"
    name = "knoxTokenAuth"

    def get_security_definition(self, auto_schema) -> dict:
        return {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": (
                "Token-based authentication with required prefix 'Token'"
            ),
        }
