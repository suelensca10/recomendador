from django.contrib.auth.decorators import login_required
from django.shortcuts import render
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

@login_required
def result(request):

    #Código que estava no helper.py
    def get_most_rated_movies(user_movie_ratings, max_number_of_movies):
        # 1- Count
        user_movie_ratings = user_movie_ratings.append(user_movie_ratings.count(), ignore_index=True)
        # 2- sort
        user_movie_ratings_sorted = user_movie_ratings.sort_values(len(user_movie_ratings) - 1, axis=1, ascending=False)
        user_movie_ratings_sorted = user_movie_ratings_sorted.drop(user_movie_ratings_sorted.tail(1).index)
        # 3- slice
        most_rated_movies = user_movie_ratings_sorted.iloc[:, :max_number_of_movies]
        return most_rated_movies

    # Código que estava no helper.py
    def get_users_who_rate_the_most(most_rated_movies, max_number_of_movies):
        # Get most voting users
        # 1- Count
        most_rated_movies['counts'] = pd.Series(most_rated_movies.count(axis=1))
        # 2- Sort
        most_rated_movies_users = most_rated_movies.sort_values('counts', ascending=False)
        # 3- Slice
        most_rated_movies_users_selection = most_rated_movies_users.iloc[:max_number_of_movies, :]
        most_rated_movies_users_selection = most_rated_movies_users_selection.drop(['counts'], axis=1)
        return most_rated_movies_users_selection

    # Código que estava no helper.py
    def sort_by_rating_density(user_movie_ratings, n_movies, n_users):
        most_rated_movies = get_most_rated_movies(user_movie_ratings, n_movies)
        most_rated_movies = get_users_who_rate_the_most(most_rated_movies, n_users)
        return most_rated_movies

    #dados do usuário logado
    curr_user = request.user
    curr_user_id = curr_user.id
    curr_user_id = int(curr_user_id)

    #cria querysets de todos os registros das tabelas book e rating
    qs_Books = Book.objects.all()
    qs_Ratings1 = Rating.objects.values('user_id','book','rating').order_by('-user_id')[:444]
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

    # antes de resumir o dataframe guarda os rows ref ao usuário logado
    usu_atual = pd.DataFrame(user_book_ratings.loc[curr_user_id]).T

    # resume o dataframe por questões de performance
    #n_books = 1001
    #n_users = 1000
    #most_rated_books = sort_by_rating_density(user_book_ratings, n_books, n_users)
    most_rated_books = user_book_ratings

    # coloca de volta os rows referente ao usuário logado
    #most_rated_books = pd.merge(most_rated_books, usu_atual, how='outer')  # Comum em apenas uma delas

    # substitui nulls por zero
    most_rated_books = most_rated_books.fillna(0)

    kmeans = KMeans(n_clusters=5, init='k-means++')
    kmeans.fit(most_rated_books);

    # prediz em qual cluster cada usuário está inserido
    predictions = kmeans.predict(most_rated_books)

    # Cria uma coluna com o cluster correspondente a cada usuário
    most_rated_books['cluster'] = kmeans.labels_

    # descobre o número do cluster do usuário atual e filtra o dataframe para manter apenas quem é do mesmo cluster q ele
    cluster_number = most_rated_books.loc[curr_user_id, 'cluster']
    cluster = most_rated_books[most_rated_books.cluster == cluster_number].drop(['cluster'], axis=1) #acho q é aqui o problema

    # Retorna todas as ratings do usuário atual
    user_ratings = pd.DataFrame(most_rated_books.loc[curr_user_id])
    user_ratings.columns = ['rating']

    # Quais livros o usuário não leu (não pontou)?
    user_unrated_books = user_ratings[user_ratings['rating'] == 0]

    # Média das ratings dos membros desse cluster para os livros que o usuário ainda não leu
    avg_ratings = pd.DataFrame(pd.concat([user_unrated_books, cluster.mean()], axis=1, join='inner').loc[:, 0])
    avg_ratings.columns = ['mean_rate']

    # Ordena pela pontuação de maneira decrescente (as maiores ratings ficam por cima)
    avg_ratings = avg_ratings.sort_values(by='mean_rate', ascending=False)[:10]

    # retorna só os títulos dos livros - cria um novo dataframe com od indexes
    recomendations = avg_ratings.index

    recomendations = recomendations.values.tolist()

    books_result = []

    for title in recomendations:
        books_result.append(Book.objects.filter(title=title).first())

    #return render(request, 'app/result.html', {'recomendations': recomendations})
    return render(request, 'app/result.html', {'recomendations': books_result})

