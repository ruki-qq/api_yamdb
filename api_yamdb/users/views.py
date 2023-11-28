from django.contrib.auth import get_user_model
from rest_framework import viewsets

from users.serializers import UserSerializer

User = get_user_model()

class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

