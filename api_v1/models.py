from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    USER_ROLES = [
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
        ('user', 'Пользователь'),
    ]

    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(
        max_length=36,
        null=True,
        blank=True,
        unique=True,
    )
    role = models.CharField(
        max_length=36,
        choices=USER_ROLES,
        default='user'
    )
    bio = models.TextField(blank=True)

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_staff

    @property
    def is_moderator(self):
        return self.role == 'moderator'


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(
        to='Genre', blank=True,
        related_name='title_genre'
    )
    category = models.ForeignKey(
        to='Category', on_delete=models.SET_NULL, blank=True, null=True,
        related_name='title_category'
    )


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)


class Review(models.Model):
    title = models.ForeignKey(
        to='Title',
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    text = models.TextField(
        verbose_name='Ревью',
    )
    author = models.ForeignKey(
        to='User',
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв к произведению {self.title.name}'


class Comment(models.Model):
    review = models.ForeignKey(
        to='Review',
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )
    text = models.TextField(
        verbose_name='Комментарий к отзыву',
    )
    author = models.ForeignKey(
        to='User',
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return (f'Комментарий пользователя {self.author.username}, '
                f'к отзыву на произведение {self.review.title.name}')
