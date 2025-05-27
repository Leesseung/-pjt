from django.urls import path
from .views import (
    RegistrationView,
    ProfileView,
    UserDetailView,
    FollowToggleView,
    FollowersListView,     # 추가
    FollowingListView,     # 추가
    
)

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/',      ProfileView.as_view(),      name='profile'),
    path('users/<str:username>/',               UserDetailView.as_view(),    name='user-detail'),
    path('users/<str:username>/follow-toggle/', FollowToggleView.as_view(), name='follow-toggle'),
    path('users/<str:username>/followers/',     FollowersListView.as_view(), name='user-followers'),
    path('users/<str:username>/following/',     FollowingListView.as_view(), name='user-following'),
]
