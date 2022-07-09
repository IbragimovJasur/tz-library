from django.db.models import Prefetch
from django.http import Http404

from apps.books.models import Book
from apps.users.models import Author


def get_author_users_all_books(author_user: Author):
    """Returns all books that requesting author user has published"""
    authors_users_all_books = author_user.books.all()
    return authors_users_all_books


def get_author_users_book_using_pk(author_user: Author, pk: int):
    try:
        author_users_book = author_user.books.prefetch_related(
            Prefetch(
                "authors", queryset=Author.objects.select_related("user")
            )
        ).get(pk=pk)
        return author_users_book

    except Book.DoesNotExist:
        raise Http404
