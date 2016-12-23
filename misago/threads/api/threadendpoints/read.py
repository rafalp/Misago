from misago.categories.models import (
    PRIVATE_THREADS_ROOT_NAME, THREADS_ROOT_NAME, Category)
from misago.categories.permissions import allow_browse_category, allow_see_category
from misago.core.shortcuts import get_int_or_404, get_object_or_404
from misago.readtracker.categoriestracker import read_category

from ...threadtypes import trees_map


def read_threads(user, pk):
    user.lock()

    category_id = get_int_or_404(pk)
    threads_tree_id = trees_map.get_tree_id_for_root(THREADS_ROOT_NAME)

    category = get_object_or_404(Category,
        id=category_id,
        tree_id=threads_tree_id,
    )

    if category.level:
        allow_see_category(user, category)
        allow_browse_category(user, category)

    read_category(user, category)


def read_private_threads(user, category):
    pass
