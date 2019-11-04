from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from sklearn.cluster import KMeans
import pandas as pd
import helper
from django_pivot.pivot import pivot
from django_pivot.histogram import histogram

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

    #cria querysets de todos os registros das tabelas book e rating
    qs_Books = Book.objects.all()
    #qs_Ratings = Rating.objects.all()
    qs_Ratings = Rating.objects.order_by('-user_id')[:200]

    #cria pandas dataframes baseados nos querysets
    Books = qs_Books.to_dataframe()
    Ratings = qs_Ratings.to_dataframe()

    #transforma os dataframes para formato desejado (matrix uxers X books)
    #?? trocar o título do livro pelo id antes do merge???
    ratings_title = pd.merge(Ratings, Books[['book', 'title']], on='book')
    #user_book_ratings = pd.pivot_table(ratings_title, index='user_id', columns='title', values='rating')
    user_book_ratings = pivot(ratings_title, index='user_id', columns='title', values='rating')

    # antes de resumir o dataframe guarda o row ref ao usuário logado
    curr_user = request.user
    curr_user_id = curr_user.id
    usu_atual = user_book_ratings.loc[curr_user_id]

    # resume o dataframe por questões de performance
    n_books = 1001
    n_users = 1000
    most_rated_books = helper.sort_by_rating_density(user_book_ratings, n_books, n_users)

    # coloca de volta o row referente ao usuário logado
    most_rated_books = most_rated_books.append(usu_atual)

    # substitui nulls por zero
    most_rated_books = most_rated_books.fillna(0)

    kmeans = KMeans(n_clusters=4, init='k-means++')
    kmeans.fit(most_rated_books);

    # prediz em qual cluster cada usuário está inserido
    predictions = kmeans.predict(most_rated_books)

    # Cria uma coluna com o cluster correspondente a cada usuário
    most_rated_books['cluster'] = kmeans.labels_

    # descobre o número do cluster do usuário atual e filtra o dataframe para manter apenas quem é do mesmo cluster q ele
    cluster_number = most_rated_books.loc[curr_user_id, 'cluster']
    cluster = most_rated_books[most_rated_books.cluster == cluster_number].drop(['cluster'], axis=1)

    # Retorna todas as ratings do usuário atual
    user_ratings = pd.DataFrame(most_rated_books.loc[curr_user_id])
    user_ratings.columns = ['rating']
    user_ratings.shape

    # Quais livros o usuário não leu (não pontou)?
    user_unrated_books = user_ratings[user_ratings['rating'] == 0]

    # Média das ratings dos membros desse cluster para os livros que o usuário ainda não leu
    avg_ratings = pd.DataFrame(pd.concat([user_unrated_books, cluster.mean()], axis=1, join='inner').loc[:, 0])
    avg_ratings.columns = ['mean_rate']

    # Ordena pela pontuação de maneira decrescente (as maiores ratings ficam por cima)
    avg_ratings = avg_ratings.sort_values(by='mean_rate', ascending=False)[:10]

    # retorna só os títulos dos livros - cria um novo dataframe com od indexes
    recomendations = pd.DataFrame(avg_ratings.index)

    return render(request, 'app/result.html', {'recomendations': recomendations})

