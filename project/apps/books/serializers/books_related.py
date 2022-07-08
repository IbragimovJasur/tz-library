from rest_framework import serializers

from apps.books.models import Book
from apps.users.serializers import AuthorUserRetrieveSerializer


class BookListSerializer(serializers.ModelSerializer):
    """
    Is used handle list() action of Book related endpoints of client app. 
    It will display minimal information about the book.
    """

    class Meta:
        model = Book
        fields = ("id", "name", "image", "published_in")


class BookRetrieveSerializer(serializers.ModelSerializer):
    """
    Is used to handle retrieve() action of Book related endpoints of 
    client app. It will display full information about the book.
    """
    authors = serializers.SerializerMethodField("get_authors_field_data")

    class Meta:
        model = Book
        exclude = ("id", "uploaded_at", )

    def get_authors_field_data(self, book):
        """Retrieving detailed field records of authors M2M field"""
        
        return AuthorUserRetrieveSerializer(book.authors, many=True).data
