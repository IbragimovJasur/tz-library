from rest_framework import serializers

from apps.books.models import Book
from apps.users.models import Author
from apps.users.serializers import AuthorUserRetrieveSerializer


class BookListSerializer(serializers.ModelSerializer):
    """
    Is used handle list() actions to Book model endpoints 
    in client and author user app.
    """

    class Meta:
        model = Book
        fields = ("id", "name", "image", "published_in")


class BookRetrieveSerializer(serializers.ModelSerializer):
    """
    Is used to handle retrieve() actions to Book model endpoints in 
    client and author user apps.
    """
    authors = serializers.SerializerMethodField("get_authors_field_data")

    class Meta:
        model = Book
        exclude = ("id", "uploaded_at", )

    def get_authors_field_data(self, book):
        """Retrieving detailed field records of authors M2M field"""
        return AuthorUserRetrieveSerializer(book.authors, many=True).data


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Is used to handle create(), updated() actions to Book model endpoints in 
    author user app
    """
    authors = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Author.objects.select_related("user")
    )
    
    class Meta:
        model = Book
        fields = (
            "authors",
            "name",
            "image",
            "published_in",
            "description",
        )
    
    def validate_authors(self, value):
        if not value:  # if not inputed values to M2M field
            raise serializers.ValidationError(
                detail={"authors": "Authors field cannot be empty"}
            )
        return value
