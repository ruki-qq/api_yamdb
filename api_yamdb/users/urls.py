from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import (
    RegistrationViewSet,
    TokenObtainView,
    UserModelViewSet,
)

v1_router = DefaultRouter()

v1_router.register('users', UserModelViewSet, basename='user')
v1_router.register('auth/signup', RegistrationViewSet, basename='auth')

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/token/', TokenObtainView.as_view()),
]
