from django.urls import path
from rest_framework import routers

from . import views
from .auth.urls import urlpatterns as auth_urls

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)

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

urlpatterns += [
    path(
        "me/friends/",
        view=views.FriendListView.as_view(
            {"get": "list"}
        ),
    )
]

urlpatterns += [
    path(
        "me/friends/<int:pk>/",
        view=views.FriendListView.as_view(
            {"get": "retrieve"}
        ),
    )
]
