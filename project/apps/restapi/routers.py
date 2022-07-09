from rest_framework.routers import Route
from rest_framework.routers import SimpleRouter


class AuthorClientUsersProfileRouter(SimpleRouter):
    """A router for performing CRUD in Client user model"""

    routes = [
        # Detail route.
        Route(
            url=r"^{prefix}{trailing_slash}$",
            mapping={
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            },
            name="{basename}-detail",
            detail=True,
            initkwargs={"suffix": "Instance"},
        ),
        # Create route.
        Route(
            url=r"^{prefix}/create{trailing_slash}$",
            mapping={"post": "create"},
            name="{basename}-create",
            detail=False,
            initkwargs={"suffix": "Create"},
        ),
    ]
    