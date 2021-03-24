from django.db import models


class Title(models.Model):
    pass


class Category(models.Model):
    pass


class Genre(models.Model):
    pass


class Review(models.Model):  # TODO
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
