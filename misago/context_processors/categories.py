from django.http import HttpRequest


def categories(request: HttpRequest) -> dict:
    request.frontend_context.update(
        {"categories_menu": request.categories.get_categories_menu()}
    )

    return {"categories": request.categories}
