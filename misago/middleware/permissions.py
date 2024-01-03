from ..permissions.proxy import UserPermissionsProxy


def permissions_middleware(get_response):
    def middleware(request):
        request.user_permissions = UserPermissionsProxy(
            request.user, request.cache_versions
        )

        return get_response(request)

    return middleware
