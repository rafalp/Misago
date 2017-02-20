from django.shortcuts import get_object_or_404

from misago.categories import THREADS_ROOT_NAME
from misago.categories.models import Category
from misago.categories.permissions import allow_browse_category, allow_see_category
from misago.core.shortcuts import get_int_or_404
from misago.readtracker.categoriestracker import read_category
from misago.threads.threadtypes import trees_map


def read_threads(user, pk):
    user.lock()

    category_id = get_int_or_404(pk)
    threads_tree_id = trees_map.get_tree_id_for_root(THREADS_ROOT_NAME)

    category = get_object_or_404(
        Category,
        id=category_id,
        tree_id=threads_tree_id,
    )

    if category.level:
        allow_see_category(user, category)
        allow_browse_category(user, category)

    read_category(user, category)


def read_private_threads(user):
    category = Category.objects.private_threads()
    read_category(user, category)

    user.sync_unread_private_threads = False
    user.unread_private_threads = 0
    user.save(update_fields=['sync_unread_private_threads', 'unread_private_threads'])
