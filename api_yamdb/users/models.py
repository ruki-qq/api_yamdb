from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model."""

    class UserRoles(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    email = models.EmailField('Email адрес')
    role = models.CharField(
        'Роль',
        max_length=50,
        choices=UserRoles.choices,
        default=UserRoles.USER,
    )
