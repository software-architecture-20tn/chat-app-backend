from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"groups", views.GroupViewSet)

urlpatterns = router.urls

urlpatterns += [
    path(
        "conversations/",
        view=views.ConversationListAPIView.as_view(),
        name="conversation-list",
    ),
    path(
        "direct-messages/<int:receiver_id>/",
        view=views.DirectMessageListAPIView.as_view(),
        name="direct-message-list",
    ),
    path(
        "direct-messages/create/",
        view=views.DirectMessageCreateAPIView.as_view(),
        name="direct-message-create",
    ),
    path(
        "group-messages/<int:group_id>/",
        view=views.GroupMessageListAPIView.as_view(),
    ),
    path(
        "group-messages/create/",
        view=views.GroupMessageCreateAPIView.as_view(),
    ),
]
