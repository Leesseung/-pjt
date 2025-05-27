from django.urls import path
from .views import RecommendChatView

urlpatterns = [
    path("recommend/", RecommendChatView.as_view(), name="chat-recommend"),
]
