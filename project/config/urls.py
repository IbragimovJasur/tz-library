from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from config.drf_yasg import urlpatterns_restapi


urlpatterns = [
    path('admin/', admin.site.urls),

    # restapi
    path("api/v1/", include("apps.restapi.urls")),

    # jwt
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]


urlpatterns = (
    urlpatterns
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + urlpatterns_restapi   # swagger url
)


# adding debug toolbar urls
if settings.DEBUG:  # only in development mode
    toolbar_urlpatterns = [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    urlpatterns += toolbar_urlpatterns
