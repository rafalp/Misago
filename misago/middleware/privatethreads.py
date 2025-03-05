from typing import TYPE_CHECKING

from ..categories.enums import CategoryTree
from ..categories.models import Category
from ..readtracker.privatethreads import get_unread_private_threads
from ..readtracker.tracker import (
    categories_select_related_user_readcategory,
    get_category_read_time,
)

if TYPE_CHECKING:
    from ..users.models import User


def sync_user_unread_private_threads(get_response):
    def middleware(request):
        if request.user.is_authenticated and request.user.sync_unread_private_threads:
            user = request.user
            category = get_private_threads_category(user)
            read_time = get_category_read_time(category)
            queryset = get_unread_private_threads(request, category, read_time)
            update_user_unread_private_threads(user, queryset.count())

        return get_response(request)

    return middleware


def get_private_threads_category(user: "User") -> Category:
    return categories_select_related_user_readcategory(
        Category.objects.filter(tree_id=CategoryTree.PRIVATE_THREADS),
        user,
    ).first()


def update_user_unread_private_threads(user: "User", unread_count: int):
    user.unread_private_threads = unread_count
    user.sync_unread_private_threads = False
    user.save(
        update_fields=[
            "unread_private_threads",
            "sync_unread_private_threads",
        ],
    )
