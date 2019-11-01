from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import helper
import sqlite3

from .forms import RatingForm
from .models import Book, Rating

# Create your views here.
def login(request):
    return render(request, 'app/login.html')

@login_required
def book_list(request):
    if request.method == 'POST':
        book = request.POST.get('book', None)
        rating = request.POST.get('rating', None)

        novo_rating = Rating()
        novo_rating.book = Book.objects.get(pk=book)
        novo_rating.rating = rating
        novo_rating.user_id = request.user.id
        novo_rating.save()

    books = Book.objects.order_by('-average_rating').order_by('-ratings_count')[:200]

    return render(request, 'app/book_list.html', {
        'books': books,
        'form': RatingForm()
    })

@login_required
def rating_new(request):
    form = RatingForm()
    return render(request, 'app/rating_edit.html', {'form': form})

#def get_recommendations(user_id)
    #ler tabelas do banco de dados
    #Books = Book.objects
    #Ratings = Ratings.objects
    #ratings_title = pd.merge(Ratings, Books[['book_id', 'title']], on='book_id')
 #   return list_of_recommended_books

@login_required
def result(request):
    Books = Book.objects
    Ratings = Rating.objects
    return render(request, 'app/result.html')

