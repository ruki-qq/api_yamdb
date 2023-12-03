from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserModelViewSet, token_obtain, user_registration


v1_router = DefaultRouter()

v1_router.register('users', UserModelViewSet, basename='user')

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/signup/', user_registration),
    path('auth/token/', token_obtain),
]
