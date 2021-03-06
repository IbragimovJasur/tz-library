from django.urls import include
from django.urls import path

from rest_framework.routers import SimpleRouter

from apps.restapi.clients.views import (
    AuthorViewSet,
    BookViewSet,
    BorrowedBookViewSet,
    ClientUserProfileViewSet,
)
from apps.restapi.routers import AuthorClientUsersProfileRouter


app_name = "clients"
client_user_profile_router = AuthorClientUsersProfileRouter(
    trailing_slash=True
)
default_router = SimpleRouter()

# registering routes
client_user_profile_router.register(
    "profile", ClientUserProfileViewSet, basename="profile"
)
default_router.register(
    "mybooks", BorrowedBookViewSet, basename="borrowed-books"
)
default_router.register("books", BookViewSet, basename="books")
default_router.register("authors", AuthorViewSet, basename="authors")


urlpatterns = [
    path("", include(client_user_profile_router.urls)),
    path("", include(default_router.urls)),
]
