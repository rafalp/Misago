from collections import defaultdict

from django.urls import reverse

from ..categories.proxy import CategoriesProxy, CategoryProxy


def get_categories_menu_data(categories: CategoriesProxy) -> list[dict]:
    top_categories: list[CategoryProxy] = []
    children: dict[int, list[dict]] = defaultdict(list)

    for category in categories.values():
        if category.level == 0:
            top_categories.append(category)
        elif category.level == 1:
            children[category.parent_id].append(serialize_menu_item(category))

    menu_items: list[dict] = []
    for category in top_categories:
        if category.is_vanilla and not children.get(category.id):
            continue

        menu_items.append(serialize_menu_item(category))

        if category_children := children.get(category.id):
            menu_items += category_children

        menu_items[-1]["last"] = True

    if menu_items:
        del menu_items[-1]["last"]

    return menu_items


def serialize_menu_item(category: CategoryProxy) -> dict:
    return {
        "id": category.id,
        "name": category.name,
        "shortName": category.short_name,
        "color": category.color,
        "url": reverse(
            "misago:category-thread-list",
            kwargs={"category_id": category.id, "slug": category.slug},
        ),
    }
