from django.urls import path
from django.urls import include


# main path for clients and authors app endpoints
urlpatterns = [
    path("clients/", include("apps.restapi.clients.urls")),
    # path("authors/", include("apps.restapi.authors.urls")),
]
