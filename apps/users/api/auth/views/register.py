# https://www.section.io/engineering-education/api-authentication-with-django-knox-and-postman-testing/
from rest_framework import generics, permissions
from rest_framework.response import Response

from ..serializers import UserRegisterSerializer


class RegisterAPIView(generics.GenericAPIView):
    """API view for registering a new user."""

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs) -> Response:
        """Handle the registration of a new user."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(
            {
                "user": serializer.data,
            }
        )
