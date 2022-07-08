from rest_framework import serializers

from apps.books.models import Book
from apps.users.serializers import AuthorUserRetrieveSerializer


class BookListSerializer(serializers.ModelSerializer):
    """
    Is used in list() method of ModelViewSet to display 
    minimal information about the book.
    """

    class Meta:
        model = Book
        fields = ("id", "name", "image", "published_in")


class BookRetrieveSerializer(serializers.ModelSerializer):
    """
    Is used in retrieve() method of ModelViewSet to display 
    full information about the book.
    """
    authors = serializers.SerializerMethodField("get_authors_data")

    class Meta:
        model = Book
        exclude = ("id", "uploaded_at", )

    def get_authors_data(self, book):
        """Retrieving Author user's data fields"""
        
        return AuthorUserRetrieveSerializer(book.authors, many=True).data
