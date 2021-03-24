from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class Titles(models.Model):
    pass


class Categories(models.Model):
    pass


class Genres(models.Model):
    pass


class Reviews(models.Model):
    pass


class Comments(models.Model):
    pass

class User(AbstractUser):

# ПОЛЯ
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
        blank=True,
        null=True,
        unique=True
    )
    role = models.CharField(
        max_length=20,
        choices=USER_ROLES,
        default='user')
    bio = models.TextField(blank=True)

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_staff

    @property
    def is_moderator(self):
        return self.role == 'moderator'

