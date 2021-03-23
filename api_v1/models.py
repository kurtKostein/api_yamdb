from django.db import models


class Titles(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ForeignKey(
        Genres, models.SET_NULL, related_name='title_genre'
    )
    category = models.ForeignKey(
        Categories, models.SET_NULL, related_name='title_category'
    )


class Categories(models.Model):
    name = models.CharField(max_length=200)
    slug = model.CharField(max_length=200)


class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = model.CharField(max_length=200)


class Reviews(models.Model):
    pass


class Comments(models.Model):
    pass
