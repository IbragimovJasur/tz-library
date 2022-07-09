from django.http import Http404

from apps.books.models import (
    Book,
    BorrowedBook,
)
from apps.users.models import (
    Author,
    Client,
)


def get_all_author_users():
    """Retrieves all author users"""
    all_author_users = Author.objects.select_related("user")
    return all_author_users


def get_all_books():
    """Retrieves all book model instances"""
    all_books = Book.objects.all()
    return all_books


def get_all_books_client_user_borrowed(client: Client):
    """Retrieves all books that client user borrowed"""

    all_books_client_user_borrowed = client.borrowed_books.select_related(
        "book"
    )
    return all_books_client_user_borrowed


def get_book_instance_using_pk(pk: int):
    """Retrieves book instance based on pk"""
    try:
        book = Book.objects.prefetch_related("authors").get(pk=pk)
        return book

    except Book.DoesNotExist:
        raise Http404   # when pk matching object doesn't exist


def get_client_user_borrowed_book_using_pk(client: Client, pk: int):
    """Retrieves client's borrowed book based on pk"""

    try:
        client_user_borrowed_book = client.borrowed_books.select_related(
            "book"
        ).get(pk=pk)
        return client_user_borrowed_book
    
    except BorrowedBook.DoesNotExist:
        raise Http404


def get_client_users_all_finished_borrowed_books(client: Client):
    """Retrieves all client user borrowed books that are finished reading"""

    finished_borrowed_books = client.borrowed_books.select_related(
        "book"
    ).filter(
        status=BorrowedBook.FINISHED_READING
    )
    return finished_borrowed_books


def get_client_users_all_still_reading_borrowed_books(client: Client):
    """Retrieves all client user borrowed books that are still being read"""

    still_reading_borrowed_books = client.borrowed_books.select_related(
        "book"
    ).filter(
        status=BorrowedBook.STILL_READING
    )
    return still_reading_borrowed_books


def search_author_using_full_name(name: str):
    """Searches author based on username"""
    query_corresponding_author_users = Author.objects.select_related(
        "user"
    ).filter(user__full_name__icontains=name)

    return query_corresponding_author_users


def search_book_using_name(name: str):
    """Searches book based on name&title"""
    books = Book.objects.filter(name__icontains=name)
    return books
