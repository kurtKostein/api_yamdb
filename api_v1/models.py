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
        unique=True
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
    slug = models.CharField(max_length=200)


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)


class Review(models.Model):
    title_id = models.ForeignKey(
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
