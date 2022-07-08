from django.http import Http404

from apps.books.models import BorrowedBook

from apps.users.models import Client


def get_all_books_client_user_borrowed(client: Client):
    """Retrieves all books that client user borrowed"""

    all_books_client_user_borrowed = client.borrowed_books.select_related(
        "book"
    )
    return all_books_client_user_borrowed


def get_client_user_borrowed_book_using_pk(client: Client, pk: int):
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
