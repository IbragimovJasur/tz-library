from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from apps.books.serializers import (
    BookListSerializer,
    BookRetrieveSerializer,
    BookCreateUpdateSerializer,
)
from apps.restapi.authors.permissions import (
    IsAuthorUser,
    IsUnAuthenticatedUser,
)
from apps.restapi.authors.utils.orm_utils import (
    get_author_users_all_books,
    get_author_users_book_using_pk,
)
from apps.restapi.utils import get_access_refresh_token_for_user
from apps.users.serializers import (
    AuthorUserCreateSerializer,
    AuthorUserUpdateSerializer,
)
from constants import (
    LIST_ACTION,
    RETRIEVE_ACTION,
)


class AuthorUserProfileViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    For performing create/retrieve/update/delete actions on 
    Author user model instance
    """
    http_method_names = ("get", "post", "patch", "put", "delete")

    def get_object(self):
        return self.request.user.author

    def get_permissions(self):
        if self.request.method == "POST":
            return (IsUnAuthenticatedUser(), )
        return (IsAuthenticated(), IsAuthorUser(), )

    def get_serializer_class(self):
        if self.request.method == "PUT" or self.request.method == "PATCH":
            return AuthorUserUpdateSerializer
        return AuthorUserCreateSerializer  # for POST request

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_client_user_instance = serializer.save()

        tokens = get_access_refresh_token_for_user(
            new_client_user_instance.user
        )
        return Response(
            data={"refresh": tokens["refresh"], "access": tokens["access"]},
            status=HTTP_201_CREATED,
        )

    def perform_destroy(self, instance):
        self.request.user.delete()  # deleting base user as well
        instance.delete()


class AuthorBooksViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAuthorUser)
    http_method_names = ("get", "post", "put", "patch", "delete")
    
    def get_serializer_class(self):
        if self.action == LIST_ACTION:
            return BookListSerializer
        elif self.action == RETRIEVE_ACTION:
            return BookRetrieveSerializer

        # in actions: create(), update()
        return BookCreateUpdateSerializer

    def get_queryset(self):
        return get_author_users_all_books(self.request.user.author)

    def get_object(self):
        return get_author_users_book_using_pk(
            self.request.user.author, self.kwargs.get("pk")
        )
