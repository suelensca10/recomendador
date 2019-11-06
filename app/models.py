from django.conf import settings
from django.db import models
from django_pandas.managers import DataFrameManager

class Book(models.Model):
    book = models.IntegerField()
    authors = models.CharField (max_length=500)
    year = models.IntegerField()
    title = models.CharField(max_length=500)
    average_rating = models.FloatField()
    ratings_count = models.FloatField()
    image_url = models.URLField()

    objects = DataFrameManager()

    #def get_remote_image(self):
    #    if self.image_url and not self.image_file:
    #        result = urllib.urlretrieve(self.image_url)
    #        self.image_file.save(
    #            os.path.basename(self.image_url),
    #            File(open(result[0]))
    #        )
    #        self.save()

    def __str__(self):
        return self.title

class Rating(models.Model):
    user_id = models.IntegerField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()

    objects = DataFrameManager()
