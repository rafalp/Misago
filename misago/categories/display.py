from typing import Sequence

from .models import Category
from .proxy import CategoryProxy


def get_categories_with_branches(
    categories: Sequence[Category | CategoryProxy],
) -> list[tuple[str, Category | CategoryProxy]]:
    if not categories:
        return []

    root_level = min(category.level for category in categories)

    tree: list[tuple[str, Category | CategoryProxy]] = []
    for category in categories:
        if category.level != root_level:
            continue

        tree.append(("", category))
        tree += _get_category_branch(categories, category, "")

    return tree


def _get_category_branch(
    categories: Sequence[Category | CategoryProxy],
    parent: Category | CategoryProxy,
    branch: str,
) -> list[tuple[str, Category | CategoryProxy]]:
    children: list[Category | CategoryProxy] = [
        category for category in categories if category.parent_id == parent.id
    ]
    if not children:
        return []

    last_index = len(children) - 1

    tree: list[tuple[str, Category | CategoryProxy]] = []
    for index, category in enumerate(children):
        is_last = index == last_index

        tree.append((branch + ("L" if is_last else "T"), category))
        tree += _get_category_branch(
            categories, category, branch + ("S" if is_last else "I")
        )

    return tree
