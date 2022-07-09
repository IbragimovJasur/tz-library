from django.urls.conf import re_path, include

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

import apps.restapi.urls as restapi_urls


# Swagger&ReDoc view for client and author app views (version1)
schema_view_restapi_v1 = get_schema_view(
    openapi.Info(
        title="App REST API",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[re_path(r"api/v1/", include(restapi_urls))],
)


# A Swagger&ReDoc url representation of client and company app endpoints
urlpatterns_restapi = [
    re_path(
        r"^swagger/v1/$",
        schema_view_restapi_v1.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
