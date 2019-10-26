import sys, os
import pandas as pd
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recomendador.settings")

import django
django.setup()

from app.models import Book

def save_book_from_row(book_row):
    book = Book()
    book.book_id = book_row[0]
    book.authors = book_row[1]
    book.year = book_row[2]
    book.title = book_row[3]
    book.average_rating = book_row[4]
    book.ratings_count = book_row[5]
    book.image_url = book_row[11]
    book.save()

    book.save_image_from_url()

if __name__ == "__main__":

    if len(sys.argv) == 2:
        print("Lendo do arquivo " + str(sys.argv[1]))
        books_df = pd.read_csv(sys.argv[1])
        print(books_df.tail)

        books_df.apply(
            save_book_from_row,
            axis=1
        )

        print("Existem {} livros no banco da dados".format(Book.objects.count()))

    else:
        print("Por favor, forneça o caminho do arquivo de livros.")




