from typing import Iterable, List

from .models import Category


def aggregate_category_stats(categories: Iterable[Category]) -> List[Category]:
    """Returns copy of categories list with childs stats aggregated to parents."""
    mutated = [category.replace() for category in categories]
    categories_map = {category.id: category for category in mutated}
    for category in reversed(mutated):
        if not category.parent_id:
            continue

        parent = categories_map[category.parent_id]
        parent.threads += category.threads
        parent.posts += category.posts

    return mutated
