from functools import cache

from .models import Category


def get_category_tree_id(category_or_id: Category | int) -> int:
    if isinstance(category_or_id, Category):
        return _get_category_tree_id_from_db(category_or_id.id)
    if isinstance(category_or_id, int):
        return _get_category_tree_id_from_db(category_or_id)

    raise TypeError(type(category_or_id))


@cache
def _get_category_tree_id_from_db(category_id: int) -> int:
    return Category.objects.values_list("tree_id", flat=True).get(id=category_id)
