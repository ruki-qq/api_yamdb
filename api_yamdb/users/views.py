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
    def set_confirmation_code_and(user):
        conf_code = default_token_generator.make_token(user)
        send_mail(
            'Your confirmation code.',
            f'Your code to get JWT token is {conf_code}',
            'admin@yamdb.ru',
            [user.email],
        )

    existing_user = User.objects.filter(
        username=request.data.get('username')
    ).first()
    if existing_user:
        if existing_user.email == request.data.get('email'):
            set_confirmation_code_and(existing_user)
            return Response(
                'User exists, sending email with confirmation code.',
                status=status.HTTP_200_OK,
            )

    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = User.objects.create(**serializer.data)
    set_confirmation_code_and(user)
    return Response(serializer.data)


@api_view(['POST'])
def token_obtain(request):
    serializer = MyTokenObtainSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=serializer.data.get('username'))
    if default_token_generator.check_token(
        user, serializer.data.get('confirmation_code')
    ):
        token = str(AccessToken.for_user(user))
        return Response({'token': token})
    return Response(
        'Wrong confirmation code.', status=status.HTTP_400_BAD_REQUEST
    )
