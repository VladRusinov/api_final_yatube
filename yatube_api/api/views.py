from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    PostSerializer,
    CommentSerializer,
    GroupSerializer,
    FollowSerializer
)
from posts.models import Post, Comment, Group, Follow


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet модели Post"""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
    )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Переопределение метода create"""
        return serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet модели Comment"""

    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
    )

    def get_post(self):
        """Получаем пост по id"""
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        """Получаем queryset с комментариями к определенному посту"""
        return Comment.objects.filter(post=self.get_post())

    def perform_create(self, serializer):
        """Переопределение метода create"""
        return serializer.save(
            author=self.request.user,
            post=self.get_post()
        )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet модели Group"""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class FollowWiewSet(viewsets.ModelViewSet):
    """ViewSet модели Follow"""

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (
        permissions.IsAuthenticated, IsAuthorOrReadOnly
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Получаем queryset с подписками пользователя"""
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Переопределение метода create"""
        return serializer.save(user=self.request.user,)
