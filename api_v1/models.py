from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    """
    следует определить __str__ по всем моделям.
    Также советую обратить внимание на Django coding style в плане размещения методов в модели
    https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/#model-style
    Надо исправить
    """
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    USER_ROLES = [
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
        ('user', 'Пользователь'),
    ]
    """
    Было бы лучше сделать отдельный класс с Choice, который бы унаследовался от models.TextChoices, так будет удобнее.
    https://docs.djangoproject.com/en/3.1/ref/models/fields/#enumeration-types
    """

    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(
        max_length=36,
        null=True,
        blank=True,
        unique=True,
    )
    """
    для CharFiled и TextFiled в джанге обычно не ставят одновременно blank=True, null=True. 
    https://stackoverflow.com/questions/8609192/what-is-the-difference-between-null-true-and-blank-true-in-django
    Можно лучше
    """
    role = models.CharField(
        max_length=36,
        choices=USER_ROLES,
        default='user'
    )
    """
    вот как раз тут должна быть константа в дефаулт
    Надо исправить
    """
    bio = models.TextField(blank=True)

    @property  # Здорово!
    def is_admin(self):
        return self.role == 'admin' or self.is_staff

    @property
    def is_moderator(self):
        return self.role == 'moderator'


class Title(models.Model):
    """
    Для всех моделей  нужно сразу прописывать:
    1) verbose_name для полей
    2) в class Meta verbose_name и verbose_name_plural
    Надо исправить
    """
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    """
    нужно валидировать Title.year на предмет того, что год не больше текущего
    Надо исправить
    """
    description = models.TextField(blank=True, null=True)
    """
    charfiled/texfield и blank/null=True
    Можно лучше
    """
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
        on_delete=models.CASCADE
    )
    text = models.TextField()
    author = models.ForeignKey(
        to='User',
        related_name='reviews',
        on_delete=models.CASCADE
    )
    score = models.PositiveSmallIntegerField(  # верное решение
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
