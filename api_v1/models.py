from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import datetime


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    USER_ROLES = [
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
        ('user', 'Пользователь'),
    ]

    email = models.EmailField(
        unique=True,
        verbose_name='Почта')
    confirmation_code = models.CharField(
        max_length=36,
        null=True,
        unique=True,
        verbose_name='Код подтверждения'
    )
    role = models.CharField(
        max_length=36,
        choices=USER_ROLES,
        default='user',
        verbose_name='Роль'
    )
    bio = models.TextField(
        blank=True,
        default='user',
        verbose_name='Биография')

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_staff

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    def __str__(self):
        return self.role


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название произведения'
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=[MaxValueValidator(datetime.datetime.now().year)]
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        to='Genre', blank=True,
        related_name='title_genre',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        to='Category', on_delete=models.SET_NULL, blank=True, null=True,
        related_name='title_category',
        verbose_name='Категория'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название категории(русский)'
    )
    slug = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название категории(английский)'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название жанра(русский)')
    slug = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название жанра(русский)'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Review(models.Model):
    title = models.ForeignKey(
        to='Title',
        related_name='reviews',
        on_delete=models.CASCADE
    )
    text = models.TextField()
    author = models.ForeignKey(
        to='User',
        related_name='reviews',
        on_delete=models.CASCADE
    )
    score = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    review_id = models.ForeignKey(
        to='Review',
        related_name='comments',
        on_delete=models.CASCADE
    )
    text = models.TextField()
    author = models.ForeignKey(
        to='User',
        related_name='comments',
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(auto_now_add=True)
