from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from posts.models import Post, Comment
from users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False)

    class Meta:
        model = Comment
        fields = 'id post author body created_at updated_at is_approved'.split()


class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False)

    class Meta:
        model = Post
        fields = 'id author title created_at is_published'.split()


class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False)
    comments = CommentSerializer(many=True)


    class Meta:
        model = Post
        fields = 'id author title body created_at updated_at is_published comments'.split()
        depth = 1

class PostValidator(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=255, min_length=1)
    body = serializers.CharField(required=True)
    is_published = serializers.BooleanField(default=True)


class CommentValidator(serializers.Serializer):
    body = serializers.CharField(required=True)
    post_id = serializers.IntegerField()
    is_approved = serializers.BooleanField(default=True)

    def validate_post_id(self, post_id):
        try:
            Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise ValidationError('Post does not exist!')
        return post_id