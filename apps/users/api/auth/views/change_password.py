# https://studygyaan.com/django/django-rest-framework-tutorial-change-password-and-reset-password
from django.contrib.auth import update_session_auth_hash

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..serializers import PasswordChangeSerializer


class PasswordChangeAPIView(GenericAPIView):
    """API view for password change."""

    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request) -> Response:
        """Handle POST request."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if user.check_password(serializer.data.get("old_password")):
            user.set_password(serializer.data.get("new_password"))
            user.save()
            update_session_auth_hash(request, user)
            return Response()
        return Response(
            {
                "old_password": "Wrong current password."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
