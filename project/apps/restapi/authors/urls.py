from django.urls import path
from django.urls import include

from rest_framework.routers import SimpleRouter

from apps.restapi.authors.views import (
    AuthorUserProfileViewSet,
    AuthorBooksViewSet,
)
from apps.restapi.routers import AuthorClientUsersProfileRouter


app_name = "authors"
author_user_profile_router = AuthorClientUsersProfileRouter(
    trailing_slash=True
)
default_router = SimpleRouter()


# route registration
author_user_profile_router.register(
    "profile", AuthorUserProfileViewSet, basename="profile"
)
default_router.register(
    "mybooks", AuthorBooksViewSet, basename="borrowed-books"
)


urlpatterns = [
    path("", include(author_user_profile_router.urls)),
    path("", include(default_router.urls)),
]
