from .categories_map import get_categories_map


def preload_categories_json(request):
    if not request.include_frontend_context:
        return {}

    request.frontend_context.update({"categoriesMap": get_categories_map(request)})

    return {}
