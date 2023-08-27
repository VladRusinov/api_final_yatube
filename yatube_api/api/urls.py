from django.urls import include, path
from rest_framework import routers

from api.views import PostViewSet, CommentViewSet, GroupViewSet, FollowWiewSet

router_v1 = routers.DefaultRouter()
router_v1.register('posts', PostViewSet, basename='PostViewSet')
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='CommentViewSet'
)
router_v1.register('groups', GroupViewSet, basename='GroupViewSet')
router_v1.register('follow', FollowWiewSet, basename="FollowWiewSet")

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
