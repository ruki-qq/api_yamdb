from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils.crypto import get_random_string


class UserManager(BaseUserManager):
    """Custom user manager."""

    def create_user(self, email, username, role=None, password=None):
        """Creates and saves a User.
        --------
        Fields: email, username, password, role.
        Also generates a confirmation code.
        """

        if not email:
            raise ValueError('У пользователя должен быть email адрес.')

        if password is None:
            password = self.make_random_password(16)

        email = self.normalize_email(email)
        conf_code = get_random_string(16)
        user = self.model(
            email=email,
            username=username,
            confirmation_code=conf_code,
            role=role,
        )
        user.set_password(password)
        user.save(using=self._db)

        send_mail(
            'Your confirmation code.',
            f'Your code to get JWT token is {conf_code}',
            'admin@yamdb.ru',
            [email],
        )
        return user


class User(AbstractUser):
    """Custom user model."""

    class UserRoles(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    email = models.EmailField('Email адрес', max_length=255, unique=True)
    confirmation_code = models.CharField('Код подтверждения', max_length=16)
    role = models.CharField(
        'Роль',
        max_length=50,
        choices=UserRoles.choices,
        default=UserRoles.USER,
    )

    objects = UserManager()
