from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import (
    filters,
    generics,
    permissions,
    status,
    viewsets,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.permissions import IsAdmin
from users.serializers import (
    MyTokenObtainSerializer,
    RegistrationSerializer,
    UserSerializer,
)

User = get_user_model()


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, *args, **kwargs):
        user = get_object_or_404(User, username=pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def get_object(self):
        user = get_object_or_404(User, username=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, user)
        return user

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=[permissions.IsAuthenticated],
    )
    def get_myself_user(self, request):
        data = request.data.copy()
        if 'role' in data.keys():
            data.pop('role')
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class RegistrationViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        existing_user = User.objects.filter(
            username=self.request.data.get('username')
        ).first()
        if existing_user:
            if existing_user.email == self.request.data.get('email'):
                existing_user.set_confirmation_code()
                return Response(
                    'User exists, sending email with confirmation code.',
                    status=status.HTTP_200_OK,
                )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_confirmation_code()
        user.save()
        return Response(serializer.data)


class TokenObtainView(generics.GenericAPIView):
    serializer_class = MyTokenObtainSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=self.request.data.get('username')
        )
        token = str(AccessToken.for_user(user))
        return Response({'token': token})
