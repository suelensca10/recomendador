import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from sklearn.cluster import KMeans
import pandas as pd
#import helper
#from django_pivot.pivot import pivot
#from django_pivot.histogram import histogram

from .forms import RatingForm
from .models import Book, Rating

# Create your views here.
def login(request):
    return render(request, 'app/login.html')

@login_required
def book_list(request):
    if request.method == 'POST':
        ratings = request.POST.get('ratings')
        ratings = json.loads(ratings)
        for rate in ratings:
            book = int(rate['book'])
            rating = int(rate['rating'])

            novo_rating = Rating()
            novo_rating.book = Book.objects.get(pk=book)
            novo_rating.rating = rating
            novo_rating.user_id = request.user.id
            novo_rating.save()
        return HttpResponse("Ok")
            

    #books = Book.objects.order_by('-average_rating').order_by('-ratings_count')[:200]
    books = Book.objects.order_by('-average_rating').order_by('-ratings_count')[:333]

    return render(request, 'app/book_list.html', {
        'books': books,
        'form': RatingForm()
    })

@login_required
def rating_new(request):
    form = RatingForm()
    return render(request, 'app/rating_edit.html', {'form': form})

@login_required
def result(request):
    #dados do usuário logado
    curr_user = request.user
    curr_user_id = curr_user.id
    curr_user_id = int(curr_user_id)

    #cria querysets de todos os registros das tabelas book e rating
    qs_Books = Book.objects.all()
    qs_Ratings1 = Rating.objects.values('user_id','book','rating').order_by('user_id')[:500]
    qs_Ratings2 = Rating.objects.values('user_id', 'book', 'rating').order_by('-rating')[:666]
    qs_Ratings_usu_atual = Rating.objects.values('user_id', 'book', 'rating').filter(user_id=curr_user_id)

    #cria pandas dataframes baseados nos querysets
    Books = qs_Books.to_dataframe()
    Ratings1 = qs_Ratings1.to_dataframe()
    Ratings2 = qs_Ratings2.to_dataframe()
    Ratings_usu_atual = qs_Ratings_usu_atual.to_dataframe()

    #junta os ratings gerais com os ratings do user_id -> concatena os dataframes
    frames = [Ratings1, Ratings2, Ratings_usu_atual]
    Ratings = pd.concat(frames)

    #transforma os dataframes para formato desejado (matriz users X books)
    Ratings.columns = ['user_id','title','rating'] #renomeia as colunas de ratings (book vira title)
    ratings_title = pd.merge(Ratings, Books[['book', 'title']], on='title')
    user_book_ratings = pd.pivot_table(ratings_title, index='user_id', columns='title', values='rating') #pandas puro

    # substitui nulls por zero
    user_book_ratings = user_book_ratings.fillna(0)
    kmeans = KMeans(n_clusters=6, init='k-means++')
    kmeans.fit(user_book_ratings)

    # Cria uma coluna com o cluster correspondente a cada usuário
    user_book_ratings['cluster'] = kmeans.labels_

    # descobre o número do cluster do usuário atual e filtra o dataframe para manter apenas quem é do mesmo cluster q ele
    cluster_number = user_book_ratings.loc[curr_user_id, 'cluster']
    cluster = user_book_ratings[user_book_ratings.cluster == cluster_number].drop(['cluster'], axis=1)

    # Retorna todas as ratings do usuário atual
    user_ratings = pd.DataFrame(user_book_ratings.loc[curr_user_id])
    user_ratings.columns = ['rating']

    # Quais livros o usuário não leu (não pontou)?
    user_unrated_books = user_ratings[user_ratings['rating'] == 0]

    # Média das ratings dos membros desse cluster para os livros que o usuário ainda não leu
    avg_ratings = pd.DataFrame(pd.concat([user_unrated_books, cluster.mean()], axis=1, join='inner').loc[:, 0])
    avg_ratings.columns = ['mean_rate']

    # Ordena pela pontuação de maneira decrescente (as maiores ratings ficam por cima)
    avg_ratings = avg_ratings.sort_values(by='mean_rate', ascending=False)[:12]

    # retorna só os títulos dos livros - cria um novo dataframe com os indexes
    recomendations = avg_ratings.index
    recomendations = recomendations.values.tolist()
    books_result = []

    #vai incrementando a lista de resultados (book_result)1
    for title in recomendations:
        books_result.append(Book.objects.filter(title=title).first())

    #retorna resultado para a template de result
    return render(request, 'app/result.html', {'recomendations': books_result})

