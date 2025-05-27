from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        # post, author 필드는 view의 perform_create에서 할당되므로 읽기 전용으로 설정
        fields = (
            "id",
            "post",
            "author",
            "author_username",
            "parent",
            "content",
            "replies",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "post",
            "author",
            "author_username",
            "created_at",
            "updated_at",
            "replies",
        )

    def get_replies(self, obj):
        qs = obj.replies.all()
        return CommentSerializer(qs, many=True, context=self.context).data


class PostListSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)
    comment_count = serializers.IntegerField(source="comments.count", read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "author_username",
            "created_at",
            "image",
            "comment_count",
        )
        read_only_fields = (
            "id",
            "author_username",
            "created_at",
            "image",
            "comment_count",
        )


class PostDetailSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)
    author_profile_image = serializers.ImageField(source="author.profile_image", read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "author",
            "author_username",
            "author_profile_image",
            "image",
            "created_at",
            "updated_at",
            "comments",
        )
        read_only_fields = (
            "id",
            "author",
            "author_username",
            "created_at",
            "updated_at",
            "comments",
        )
