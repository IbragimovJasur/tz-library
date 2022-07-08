from rest_framework.serializers import ValidationError

from apps.users.models import Client
from constants import BOOK_IMAGE_UPLOAD_PATH


def get_book_image_upload_path(instance, filename):
    """
    For generating a path from media root for uploading a book image
    Ex. books/book_name/filename
    """
    return "{}/{}/{}".format(
        BOOK_IMAGE_UPLOAD_PATH, 
        instance.name, 
        filename   # image name
    )


def check_if_client_user_has_inputed_book_in_booklist(
    client_user: Client, book
):
    """Raises an exception if client user already borrowed inputed book"""

    is_inputed_book_in_client_booklist = client_user.borrowed_books.filter(
        book=book
    ).exists()
    if is_inputed_book_in_client_booklist:
        raise ValidationError(
            detail={"book": "You alredy have this book in your book-list"}
        )
    return book
