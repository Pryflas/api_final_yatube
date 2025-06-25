from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework import viewsets, permissions, mixins, response, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from posts.models import Post, Comment, Follow, Group
from .serializers import (PostSerializer, CommentSerializer,
                          FollowSerializer, GroupSerializer)
from django.db import IntegrityError


User = get_user_model()
ERR_EDIT = 'У вас нет прав для редактирования этого комментария'


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return response.Response(
                {'detail': 'У вас нет прав для выполнения этого действия.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return response.Response(
                {'detail': 'У вас нет прав для выполнения этого действия.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return response.Response(
                {'detail': 'У вас нет прав для выполнения этого действия.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(
            author=self.request.user,
            post_id=post_id
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return response.Response(
                {'detail': ERR_EDIT},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return response.Response(
                {'detail': ERR_EDIT},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return response.Response(
                {'detail': 'У вас нет прав для удаления этого комментария'},
                status=status.HTTP_403_FORBIDDEN
            )
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['following__username']

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return response.Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except IntegrityError:
            return response.Response(
                {'error': 'Вы уже подписаны на этого пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# class GroupCreateView(generics.CreateAPIView):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAdminUser]
