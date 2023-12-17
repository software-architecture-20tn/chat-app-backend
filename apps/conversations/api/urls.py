from django.urls import path

from . import views

urlpatterns = [
    path(
        "conversations/",
        view=views.ConversationListAPIView.as_view(),
        name="conversation-list",
    )
]
