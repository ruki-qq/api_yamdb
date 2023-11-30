from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils.crypto import get_random_string


class UserManager(BaseUserManager):
    """Custom user manager."""

    def create_user(
        self,
        email,
        username,
        bio=None,
        role='user',
        password=None,
        **extra_fields,
    ):
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
            bio=bio,
            role=role,
            **extra_fields,
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

    def create_superuser(
        self,
        email,
        username,
        role,
        bio=None,
        password=None,
        **extra_fields,
    ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(
            email, username, bio, 'admin', password, **extra_fields
        )


class User(AbstractUser):
    """Custom user model."""

    class UserRoles(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    email = models.EmailField('Email адрес', max_length=254, unique=True)
    confirmation_code = models.CharField('Код подтверждения', max_length=16)
    bio = models.TextField('Биография', blank=True, null=True)
    role = models.CharField(
        'Роль',
        max_length=50,
        choices=UserRoles.choices,
        default=UserRoles.USER,
    )

    objects = UserManager()
