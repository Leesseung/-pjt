from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    CommentSerializer,
)

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

# 게시글 리스트 & 생성 (ListCreate)
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by("-created_at")
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostListSerializer
        # POST 에는 DetailSerializer를 사용해야 content/image 필드를 받을 수 있습니다.
        return PostDetailSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# 게시글 상세/수정/삭제
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    serializer_class = PostDetailSerializer

# 댓글 리스트 & 생성
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs["post_pk"])
        return Comment.objects.filter(post=post, parent__isnull=True).order_by("created_at")

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs["post_pk"])
        serializer.save(author=self.request.user, post=post)

# 댓글 상세/수정/삭제
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

class MyPostListView(generics.ListAPIView):
    """
    로그인한 유저가 작성한 Post 만 리스트로 반환
    GET /community/posts/mine/
    """
    serializer_class   = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-created_at')
    
class UserPostListView(generics.ListAPIView):
    """
    GET /api/community/users/{username}/posts/
    -> 해당 username 유저가 쓴 Post 리스트
    """
    serializer_class   = PostListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        username = self.kwargs['username']
        return Post.objects.filter(author__username=username).order_by('-created_at')