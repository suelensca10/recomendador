from django.shortcuts import render
from .models import Book
from .forms import RatingForm

# Create your views here.
def book_list(request):
    books = Book.objects.order_by('-average_rating').order_by('-ratings_count')[:25]
    return render(request, 'app/book_list.html', {'books': books})

def rating_new(request):
    form = RatingForm()
    return render(request, 'app/rating_edit.html', {'form': form})