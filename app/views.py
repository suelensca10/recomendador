from django.shortcuts import render
from .models import Book, Rating
from .forms import RatingForm
from django.urls import reverse_lazy
from django.views import generic

# Create your views here.
def login(request):
    return render(request, 'app/login.html')

def book_list(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id', None)
        rating = request.POST.get('rating', None)

        novo_rating = Rating()
        novo_rating.book = Book.objects.get(pk=book_id)
        novo_rating.rating = rating
        novo_rating.user_id = request.user.id
        novo_rating.save()

    books = Book.objects.order_by('-average_rating').order_by('-ratings_count')[:25]

    return render(request, 'app/book_list.html', {
        'books': books,
        'form': RatingForm()
    })

def rating_new(request):
    form = RatingForm()
    return render(request, 'app/rating_edit.html', {'form': form})
