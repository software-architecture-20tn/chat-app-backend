from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from knox.models import AuthToken
from knox.settings import CONSTANTS


class LogoutAPIView(APIView):
    """API view for a user to log out."""

    permission_classes = (IsAuthenticated,)
    serializer_class = None

    def post(self, request) -> Response:
        """Logout a user.

        Get the token from the request header, get the first 8 characters
            (CONSTANTS.TOKEN_KEY_LENGTH) of the token, and delete the token.

        """
        token = request.META.get("HTTP_AUTHORIZATION", "").split()[1]
        short_token_key = token[:CONSTANTS.TOKEN_KEY_LENGTH]
        AuthToken.objects.filter(
            token_key=short_token_key,
            user=request.user,
        ).delete()
        return Response()
