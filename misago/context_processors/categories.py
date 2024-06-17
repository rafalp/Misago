from django.http import HttpRequest


def categories(request: HttpRequest) -> dict:
    request.frontend_context.update(
        {
            "categoriesMap": request.categories.top_categories_list,
        }
    )

    return {"categories": request.categories}
