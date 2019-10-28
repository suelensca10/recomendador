import sys, os
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recomendador.settings")

import django
django.setup()

from app.models import Rating, Book

def get_book(rating_row):
    try:
        Book.objects.get(book_id=rating_row[1])
        return True
    except Book.DoesNotExist:
        return False

def save_rating_from_row(rating_row):
    if get_book(rating_row):
        rating = Rating()
        rating.book_id = Book.objects.get(book_id=rating_row[1]).id
        rating.user_id = rating_row[0]
        rating.rating = rating_row[2]
        rating.save()

if __name__ == "__main__":

    if len(sys.argv) == 2:
        print ("Lendo do arquivo " + str(sys.argv[1]))
        rating_df = pd.read_csv(sys.argv[1])
        print(rating_df.tail)

        rating_df.apply(
            save_rating_from_row,
            axis=1
        )

        print("Existem {} ratings no banco da dados".format(Rating.objects.count()))

    else:
        print("Por favor, forneça o caminho do arquivo de avaliações.")




