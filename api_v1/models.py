from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    EMAIL_FIELD = 'email'
    USER_FIELDS = []  # 'username'
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

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_staff

    @property
    def is_moderator(self):
        return self.role == 'moderator'


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ForeignKey(
        to='Genre', models.SET_NULL, related_name='title_genre'
    )
    category = models.ForeignKey(
        to='Category', models.SET_NULL, related_name='title_category'
    )


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)



class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)


class Review(models.Model):
    title_id = models.ForeignKey(to='Title',
                                 related_name='reviews',
                                 on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(to='User',
                               related_name='reviews',
                               on_delete=models.CASCADE)
    score = models.PositiveIntegerField(null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    review_id = models.ForeignKey(to='Review',
                                  related_name='reviews',
                                  on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(to='User',
                               related_name='reviews',
                               on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
