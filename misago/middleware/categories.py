from ..categories.proxy import CategoriesProxy


def categories_middleware(get_response):
    def middleware(request):
        request.categories = CategoriesProxy(
            request.user_permissions, request.cache_versions
        )

        return get_response(request)

    return middleware
