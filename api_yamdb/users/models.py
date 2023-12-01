from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils.crypto import get_random_string

from users.utils import send_conf_code_mail


class User(AbstractUser):
    """Custom user model."""

    class UserRoles(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    email = models.EmailField('Email адрес', max_length=254, unique=True)
    confirmation_code = models.CharField(
        'Код подтверждения', max_length=16, blank=True, null=True
    )
    bio = models.TextField('Биография', blank=True, null=True)
    role = models.CharField(
        'Роль',
        max_length=50,
        choices=UserRoles.choices,
        default=UserRoles.USER,
    )

    class Meta:
        ordering = ['username']

    def set_confirmation_code(self):
        conf_code = get_random_string(16)
        self.confirmation_code = make_password(conf_code)
        send_mail(
            'Your confirmation code.',
            f'Your code to get JWT token is {conf_code}',
            'admin@yamdb.ru',
            [self.email],
        )
