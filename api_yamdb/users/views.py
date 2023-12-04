from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import (
    filters,
    permissions,
    status,
    viewsets,
)
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.v1.permissions import IsAdmin
from users.serializers import (
    MyTokenObtainSerializer,
    RegistrationSerializer,
    UserSerializer,
)


User = get_user_model()


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=[permissions.IsAuthenticated],
    )
    def get_myself_user(self, request):
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


@api_view(['POST'])
def user_registration(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    for field, value in serializer.data.items():
        existing_user = User.objects.filter(**{field: value}).first()
        if existing_user:
            remaining_data = serializer.data.copy()
            remaining_data.pop(field)
            for name in remaining_data:
                if getattr(existing_user, name) != remaining_data[name]:
                    return Response(
                        f'"field_name": [{field}]',
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            break
    user, created = User.objects.get_or_create(**serializer.data)
    conf_code = default_token_generator.make_token(user)
    send_mail(
        'Your confirmation code.',
        f'Your code to get JWT token is {conf_code}',
        'admin@yamdb.ru',
        [user.email],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def token_obtain(request):
    serializer = MyTokenObtainSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=serializer.data.get('username'))
    if not default_token_generator.check_token(
        user, serializer.data.get('confirmation_code')
    ):
        return Response(
            'Wrong confirmation code.', status=status.HTTP_400_BAD_REQUEST
        )
    token = str(AccessToken.for_user(user))
    return Response({'token': token})
