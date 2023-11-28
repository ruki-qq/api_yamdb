from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import GenreViewSet, CategoryViewSet, TitleViewSet, ReviewViewSet, CommentViewSet

v1_router = SimpleRouter()

v1_router.register('genres', GenreViewSet)
v1_router.register('categories', CategoryViewSet)
v1_router.register('titles', TitleViewSet)
v1_router.register('reviews', ReviewViewSet)
v1_router.register('comments', CommentViewSet)

urlpatterns = [
#    path('v1/', include('djoser.urls')),
#    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(v1_router.urls)), ]

