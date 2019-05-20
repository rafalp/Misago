from rest_framework.routers import DefaultRouter, DynamicRoute, Route


class MisagoApiRouter(DefaultRouter):
    include_root_view = False
    include_format_suffixes = False

    routes = [
        # List route.
        Route(
            url=r"^{prefix}{trailing_slash}$",
            mapping={"get": "list", "post": "create"},
            name="{basename}-list",
            initkwargs={"suffix": "List"},
            detail=False,
        ),
        # Dynamically generated list routes.
        # Generated using @list_route decorator
        # on methods of the viewset.
        DynamicRoute(
            url=r"^{prefix}/{url_path}{trailing_slash}$",
            name="{basename}-{url_name}",
            initkwargs={},
            detail=False,
        ),
        # Detail route.
        Route(
            url=r"^{prefix}/{lookup}{trailing_slash}$",
            mapping={
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            },
            name="{basename}-detail",
            initkwargs={"suffix": "Instance"},
            detail=True,
        ),
        # Dynamically generated detail routes.
        # Generated using @detail_route decorator on methods of the viewset.
        DynamicRoute(
            url=r"^{prefix}/{lookup}/{url_path}{trailing_slash}$",
            name="{basename}-{url_name}",
            initkwargs={},
            detail=True,
        ),
    ]
