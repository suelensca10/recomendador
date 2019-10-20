from django.shortcuts import render
from .models import Book

# Create your views here.
def book_list(request):
    books = Book.objects.order_by('-average_rating').order_by('-ratings_count')[:25]
    return render(request, 'app/book_list.html', {'books': books})