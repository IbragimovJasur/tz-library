from django.urls import path
from django.urls import include

from apps.restapi.authors.views import (
    AuthorUserProfileViewSet,
)
from apps.restapi.routers import AuthorClientUsersProfileRouter


app_name = "authors"
author_user_profile_router = AuthorClientUsersProfileRouter(
    trailing_slash=True
)

# route registration
author_user_profile_router.register(
    "profile", AuthorUserProfileViewSet, basename="profile"
)


urlpatterns = [
    path("", include(author_user_profile_router.urls)),
]
