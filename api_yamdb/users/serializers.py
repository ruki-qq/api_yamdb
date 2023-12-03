from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.validators import validate_forbidden_usernames

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.USERNAME_MAX_LEN,
        validators=[
            UnicodeUsernameValidator(),
            validate_forbidden_usernames,
            UniqueValidator(queryset=User.objects.all()),
        ],
    )
    email = serializers.EmailField(
        max_length=settings.EMAIL_MAX_LEN,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )


class UserSerializer(serializers.ModelSerializer, RegistrationSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        ]


class MyTokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.USERNAME_MAX_LEN,
        validators=[UnicodeUsernameValidator(), validate_forbidden_usernames],
    )
    confirmation_code = serializers.CharField()
