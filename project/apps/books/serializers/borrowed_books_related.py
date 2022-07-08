from rest_framework import serializers

from apps.books.models import BorrowedBook
from apps.books.serializers import BookListSerializer


class BorrowedBookCreateSerializer(serializers.ModelSerializer):
    """
    Is used to handle create() actions on BorrowedBooks endpoints of client app.
    """

    class Meta:
        model = BorrowedBook
        fields = ("book", )


class BorrowedBookSerializer(serializers.ModelSerializer):
    """
    Is used to handle list(), retrieve() actions on BorrowedBooks 
    endpoints of client app.
    """
    book = serializers.SerializerMethodField("get_book_field_data")
    status = serializers.SerializerMethodField("get_status_field_human_readable_value")

    class Meta:
        model = BorrowedBook
        exclude = ("client", "date_finished", "datetime_borred")

    def get_book_field_data(self, borrowed_book):
        """Retrieving detailed field records of book ForeignKey field"""

        return BookListSerializer(borrowed_book.book).data

    def get_status_field_human_readable_value(self, borrowed_book):
        return borrowed_book.get_status_display()


class BorrowedFinishedBookListSerializer(serializers.ModelSerializer):
    """
    Is used to handle list() actions on BorrowedBooks
    endpoints of client app where ?q='finished'.
    """
    book = serializers.SerializerMethodField("get_book_field_data")

    class Meta:
        model = BorrowedBook
        exclude = ("client", "datetime_borred")

    def get_book_field_data(self, borrowed_book):
        """Retrieving detailed field records of book ForeignKey field"""

        return BookListSerializer(borrowed_book.book).data


class BorrowedBookUpdateSerializer(serializers.ModelSerializer):
    """
    Is used to handle put() actions on BorrowedBook endpoints of client app.
    """

    class Meta:
        model = BorrowedBook
        fields = ("status", )
