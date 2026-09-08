from django.http import HttpRequest

from ..menus.categories import get_categories_menu_data


def categories(request: HttpRequest) -> dict:
    request.frontend_context.update(
        {"categories_menu": get_categories_menu_data(request.categories)}
    )

    return {}
