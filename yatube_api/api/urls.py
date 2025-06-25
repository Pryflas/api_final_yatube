from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (PostViewSet, CommentViewSet,
                    FollowViewSet, RegisterView,
                    GroupViewSet)

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('follow', FollowViewSet, basename='follow')
router.register('groups', GroupViewSet, basename='groups')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/register/', RegisterView.as_view(), name='register'),
    path('v1/posts/<int:post_id>/comments/',
         CommentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('v1/posts/<int:post_id>/comments/<int:pk>/',
         CommentViewSet.as_view({
             'get': 'retrieve',
             'put': 'update',
             'patch': 'partial_update',
             'delete': 'destroy'
         })),
]
