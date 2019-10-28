from django.contrib import admin
from .models import Rating, Book


class RatingAdmin(admin.ModelAdmin):
    list_display = ('book', 'user_id', 'rating',)

admin.site.register(Rating, RatingAdmin)
admin.site.register(Book)