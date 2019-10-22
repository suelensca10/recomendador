from django.conf import settings
from django.db import models
from django.utils import timezone

class Book(models.Model):
    book_id = models.IntegerField()
    authors = models.CharField (max_length=500)
    year = models.IntegerField()
    title = models.CharField(max_length=500)
    average_rating = models.FloatField()
    ratings_count = models.FloatField()
    image_url = models.CharField(max_length=1000)

    def __str__(self):
        return self.title

class Rating(models.Model):
    user_id = models.IntegerField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()