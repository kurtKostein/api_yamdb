from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

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
    EMAIL_FIELD = 'email'
    USER_FIELDS = [] # 'username'
    USER_ROLES = [
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
        ('user', 'Пользователь'),
    ]

    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(
        max_length=36,
        blank=True,
        unique=True
    )
    role = models.CharField(
        max_length=36,
        choices=USER_ROLES,
        default='user'
    )
    bio = models.TextField(max_length=300, blank=True)
    #
    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_staff

    @property
    def is_moderator(self):
        return self.role == 'moderator'
