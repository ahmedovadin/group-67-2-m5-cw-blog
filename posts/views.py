from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from posts.models import Post, Comment
from posts.serializers import (
    PostListSerializer,
    PostDetailSerializer,
    CommentSerializer,
)

class CustomPagination(PageNumberPagination):
    page_size = 5

    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })

class PostViewSet(ModelViewSet):
    queryset = Post.objects.filter(is_published=True).select_related('author')
    serializer_class = PostDetailSerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostDetailSerializer

    def create(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={'error': 'Требуется авторизация'}
            )
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={'error': 'Требуется авторизация'}
            )
        post = self.get_object()
        if post.author != request.user:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={'error': 'Только автор может редактировать пост'}
            )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={'error': 'Требуется авторизация'}
            )
        post = self.get_object()
        if post.author != request.user:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={'error': 'Только автор может редактировать пост'}
            )
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={'error': 'Требуется авторизация'}
            )
        post = self.get_object()
        if post.author != request.user:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={'error': 'Только автор может удалить пост'}
            )
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentListCreateAPIView(ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['id']
        return Comment.objects.filter(post_id=post_id, is_approved=True).select_related('author')

    def create(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={'error': 'Требуется авторизация'}
            )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        post_id = self.kwargs['id']
        post = Post.objects.get(id=post_id)
        serializer.save(author=self.request.user, post=post)


class CommentDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={'error': 'Требуется авторизация'}
            )
        comment = self.get_object()
        if comment.author != request.user:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={'error': 'Только автор может редактировать комментарий'}
            )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={'error': 'Требуется авторизация'}
            )
        comment = self.get_object()
        if comment.author != request.user:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={'error': 'Только автор может редактировать комментарий'}
            )
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={'error': 'Требуется авторизация'}
            )
        comment = self.get_object()
        if comment.author != request.user:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={'error': 'Только автор может удалить комментарий'}
            )
        return super().destroy(request, *args, **kwargs)