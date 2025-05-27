# backend/community/urls.py

from django.urls import path
from .views import (
    PostListCreateView,
    PostDetailView,
    CommentListCreateView,
    CommentDetailView,
    MyPostListView,
    UserPostListView, 
)

app_name = "community"

urlpatterns = [
    path("posts/",                       PostListCreateView.as_view(),    name="post-list"),
    path('posts/mine/',         MyPostListView.as_view(),       name='my-post-list'),  # ← 추가
    path("posts/<int:pk>/",              PostDetailView.as_view(),        name="post-detail"),
    path("posts/<int:post_pk>/comments/", CommentListCreateView.as_view(), name="comment-list"),
    path("comments/<int:pk>/",           CommentDetailView.as_view(),     name="comment-detail"),
    path('users/<str:username>/posts/', UserPostListView.as_view(), name='user-post-list'),  # ← 추가
]
