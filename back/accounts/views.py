from rest_framework import generics, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .serializer import ProfileSerializer, PublicProfileSerializer, RegistrationSerializer
from .permissions import IsOwnerOrReadOnly

User = get_user_model()

class RegistrationView(generics.CreateAPIView):
    """
    POST /api/v1/accounts/registration/
    """
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/v1/accounts/profile/     -> 내 프로필 조회
    PATCH/PUT /api/v1/accounts/profile/ -> 내 프로필 수정 (본인만)
    """
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_object(self):
        return self.request.user


class UserDetailView(generics.RetrieveAPIView):
    """
    GET /api/v1/accounts/users/{username}/
    다른 유저 프로필 조회
    """
    queryset = User.objects.all()
    serializer_class = PublicProfileSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'username'


class FollowToggleView(generics.GenericAPIView):
    """
    POST /api/v1/accounts/users/{username}/follow-toggle/
    팔로우/언팔로우 토글
    """
    serializer_class = PublicProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'username'

    def post(self, request, username):
        target = get_object_or_404(User, username=username)
        me = request.user

        if target == me:
            return Response({'detail': '자기 자신은 팔로우할 수 없습니다.'}, status=400)

        if me.following.filter(pk=target.pk).exists():
            me.following.remove(target)
        else:
            me.following.add(target)

        serializer = self.get_serializer(target, context={'request': request})
        return Response(serializer.data)

class FollowersListView(generics.ListAPIView):
    """
    GET /api/v1/accounts/users/{username}/followers/
    해당 유저를 팔로우하는 사람들의 리스트 반환
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = PublicProfileSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        user = generics.get_object_or_404(User, username=username)
        return user.followers.all()


class FollowingListView(generics.ListAPIView):
    """
    GET /api/v1/accounts/users/{username}/following/
    해당 유저가 팔로우하고 있는 사람들의 리스트 반환
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = PublicProfileSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        user = generics.get_object_or_404(User, username=username)
        return user.following.all()