from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.db import models


User = get_user_model()


class Genre(models.Model):
    name = models.CharField('Название', max_length=settings.CHAR_FIELD_MAX_LEN)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        ordering = ['slug']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Название', max_length=settings.CHAR_FIELD_MAX_LEN)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        ordering = ['slug']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


def validate_year(value):
    if value > int(datetime.now().year):
        raise ValidationError(
            'Год не может быть в будущем'
        )


class Title(models.Model):
    name = models.CharField('Название', max_length=settings.CHAR_FIELD_MAX_LEN)
    year = models.SmallIntegerField(
        'Год выпуска', validators=[validate_year]
    )
    description = models.TextField('Описание', blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles', null=True
    )
    genre = models.ManyToManyField(
        'Genre', related_name='titles', blank=True, verbose_name='Жанры'
    )

    class Meta:
        ordering = ['year', 'name',]
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(settings.RATING_MIN,
                                      message='Ниже допустимого'),
                    MaxValueValidator(settings.RATING_MAX,
                    message='Выше допустимого')]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)
        constraints = (models.UniqueConstraint(fields=('title', 'author'),
                                               name='author_title_uniq'),)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:settings.TEXT_PREVIEW_LEN]


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:settings.TEXT_PREVIEW_LEN]
