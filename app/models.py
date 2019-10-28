from django.conf import settings
from django.db import models
from django.core.files import File
import os
from urllib.request import urlopen
from django.core.files.temp import NamedTemporaryFile
#import requests

class Book(models.Model):
    book_id = models.IntegerField()
    authors = models.CharField (max_length=500)
    year = models.IntegerField()
    title = models.CharField(max_length=500)
    average_rating = models.FloatField()
    ratings_count = models.FloatField()
    image_url = models.URLField()
    #image_file = models.ImageField(upload_to='images/', null = True, blank=True)

   # def save_image_from_url(model):
   #     r = requests.get(model.image_url)
   #     img_temp = NamedTemporaryFile(delete=True)
   #     img_temp.write(r.content)
   #     img_temp.flush()
   #     model.image_file.save("image.jpg", File(img_temp), save=True)

    #se for pra usar, é esse aqui
    #def get_remote_image(self):
    #    if self.image_url and not self.image_file:
    #        result = urllib.urlretrieve(self.image_url)
    #        self.image_file.save(
    #            os.path.basename(self.image_url),
    #            File(open(result[0]))
    #        )
    #        self.save()

    #def get_remote_image(self):
    #    if self.image_url and not self.image_file:
    #        img_temp = NamedTemporaryFile(delete=True)
    #        img_temp.write(urlopen(self.image_url).read())
    #        img_temp.flush()
    #        self.image_file.save(f"image_{self.pk}", File(img_temp))
    #    self.save()"

    def __str__(self):
        return self.title

class Rating(models.Model):
    user_id = models.IntegerField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()