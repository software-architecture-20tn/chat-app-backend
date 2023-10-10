from rest_framework import routers

from . import views
from .auth.urls import urlpatterns as auth_urls

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)

urlpatterns = router.urls


urlpatterns += auth_urls
