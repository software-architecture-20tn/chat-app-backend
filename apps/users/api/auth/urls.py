from django.urls import path

from rest_framework.routers import DefaultRouter

from django_rest_passwordreset.urls import add_reset_password_urls_to_router

from . import views

router = DefaultRouter()
add_reset_password_urls_to_router(router, base_path="api/auth/passwordreset")

urlpatterns = router.urls + [
    path(
        "register/",
        views.RegisterAPIView.as_view(),
        name="register",
    ),
    path(
        "login/",
        views.LoginAPIView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        views.LogoutAPIView.as_view(),
        name="logout",
    ),
    path(
        "change-password/",
        views.PasswordChangeAPIView.as_view(),
        name="change-password",
    ),
]
