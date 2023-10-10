from rest_framework import mixins
from rest_framework.response import Response


class UpdateModelOnlyPutMixin(mixins.UpdateModelMixin):
    """A mixin for updating model, but only with PUT method."""

    def update(self, request, *args, **kwargs) -> Response:
        """Update model, but only with PUT method."""
        if request.method == "PUT":
            return super().update(request, *args, **kwargs)
        return Response(status=405)
