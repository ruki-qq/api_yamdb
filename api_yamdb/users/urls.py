from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.views import RegistrationViewSet, UserModelViewSet

v1_router = SimpleRouter()

v1_router.register('users', UserModelViewSet)
v1_router.register('auth/signup', RegistrationViewSet)

urlpatterns = [
    path('', include(v1_router.urls)),
]
