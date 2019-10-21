from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.book_list, name='book_list'),
    path('rating/', views.rating_new, name='rating_new'),
]