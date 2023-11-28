from django.urls import path
from rest_framework import routers

from . import views
from .auth.urls import urlpatterns as auth_urls

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"friends", views.FriendViewSet)
router.register(r"friend-requests", views.FriendRequestViewSet)

urlpatterns = router.urls


urlpatterns += auth_urls

urlpatterns += [
    path(
        "me/",
        view=views.ProfileViewSet.as_view(
            {"get": "retrieve", "put": "update"}
        ),
        name="user-profile",
    )
]
