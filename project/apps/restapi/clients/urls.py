from django.urls import include
from django.urls import path

from apps.restapi.clients.routers import ClientUserProfileRouter
from apps.restapi.clients.views import (
    ClientUserProfileView,
)


app_name = "clients"
client_user_profile_router = ClientUserProfileRouter(trailing_slash=True)

# registering routes
client_user_profile_router.register(
    "profile", ClientUserProfileView, basename="profile"
)


urlpatterns = [
    path("", include(client_user_profile_router.urls)),
]
