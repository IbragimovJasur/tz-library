from django.urls import include
from django.urls import path

from rest_framework.routers import SimpleRouter

from apps.restapi.clients.routers import ClientUserProfileRouter
from apps.restapi.clients.views import (
    ClientUserProfileView,
    BookModelView,
)


app_name = "clients"
client_user_profile_router = ClientUserProfileRouter(trailing_slash=True)
default_router = SimpleRouter()

# registering routes
client_user_profile_router.register(
    "profile", ClientUserProfileView, basename="profile"
)
default_router.register("books", BookModelView, basename="books")


urlpatterns = [
    path("", include(client_user_profile_router.urls)),
    path("", include(default_router.urls)),
]
