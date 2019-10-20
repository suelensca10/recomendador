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
    ratings_1 = models.FloatField()
    ratings_2 = models.FloatField()
    ratings_3 = models.FloatField()
    ratings_4 = models.FloatField()
    ratings_5 = models.FloatField()
    image_url = models.TextField()
    small_image_url = models.TextField()

    def __str__(self):
        return self.title

class Rating(models.Model):
    user_id = models.IntegerField()
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()