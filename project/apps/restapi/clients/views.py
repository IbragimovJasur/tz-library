from django.http import Http404

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from apps.books.models import (
    Book,
    BorrowedBook,
)
from apps.books.serializers import (
    BookListSerializer,
    BookRetrieveSerializer,
    BorrowedBookSerializer,
    BorrowedFinishedBookListSerializer,
    BorrowedBookCreateSerializer,
    BorrowedBookUpdateSerializer,
)
from apps.restapi.clients.permissions import (
    IsClientUser,
    IsUnAuthenticatedUser,
)
from apps.restapi.clients.utils.db_utils import (
    get_all_books_client_user_borrowed,
    get_client_users_all_finished_borrowed_books,
    get_client_users_all_still_reading_borrowed_books,
    get_client_user_borrowed_book_using_pk,
)
from apps.restapi.utils import get_access_refresh_token_for_user
from apps.users.serializers import (
    ClientUserCreateSerializer,
    ClientUserUpdateSerializer,
)
from constants import (
    CREATE_ACTION,
    FINISHED_BOOK_STATUS,
    LIST_ACTION,
    UPDATE_ACTION,
    STILL_READING_BOOK_STATUS,
)


class ClientUserProfileViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    For performing create/retrieve/update/delete method on Client
    (regular user) model instances
    """

    http_method_names = ("get", "post", "patch", "put", "delete")

    def get_object(self):
        return self.request.user.client

    def get_permissions(self):
        if self.request.method == "POST":
            return (IsUnAuthenticatedUser(), )

        return (
            IsAuthenticated(),
            IsClientUser(),
        )

    def get_serializer_class(self):
        if self.request.method == "PUT" or self.request.method == "PATCH":
            return ClientUserUpdateSerializer

        return ClientUserCreateSerializer

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


class BookViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """For handling GET requests for books model by client users"""
    permission_classes = (IsAuthenticated, IsClientUser)
    http_method_names = ("get", )

    def get_serializer_class(self):
        if self.action == LIST_ACTION:
            return BookListSerializer

        return BookRetrieveSerializer  # for retrieve method

    def get_queryset(self):
        query_param = self.request.query_params.get("name")
        if query_param:
            books = Book.objects.filter(name__icontains=query_param)
            return books

        return Book.objects.all()

    def get_object(self):
        try:
            book = Book.objects.prefetch_related(
                "authors"
            ).get(pk=self.kwargs.get("pk"))
            return book

        except Book.DoesNotExist:
            raise Http404   # when pk matching object doesn't exist


class BorrowedBookViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsClientUser)

    http_method_names = ("get", "post", "put", "patch", "delete")

    def get_serializer_class(self):
        query_param = self.request.query_params.get("status", False)
        if self.action == CREATE_ACTION:
            return BorrowedBookCreateSerializer

        elif self.action == UPDATE_ACTION:
            return BorrowedBookUpdateSerializer

        else:  # list(), retrieve()
            if query_param == FINISHED_BOOK_STATUS:
                # in case there's a query request for finished borrowed books
                return BorrowedFinishedBookListSerializer

            return BorrowedBookSerializer

    def get_queryset(self):
        query_param = self.request.query_params.get("status", False)
        client_user = self.request.user.client
        if query_param:
            if query_param == FINISHED_BOOK_STATUS:
                return get_client_users_all_finished_borrowed_books(
                    client_user
                )
            elif query_param == STILL_READING_BOOK_STATUS:
                return get_client_users_all_still_reading_borrowed_books(
                    client_user
                )
            else:  # if irrelevant query params
                return BorrowedBook.objects.none()

        return get_all_books_client_user_borrowed(client_user)

    def get_object(self):
        return get_client_user_borrowed_book_using_pk(
            self.request.user.client, self.kwargs.get("pk")
        )
        
    def perform_create(self, serializer):
        serializer.save(client=self.request.user.client)
