from typing import TYPE_CHECKING

from django.http import HttpRequest

from ..categories.enums import CategoryTree
from ..categories.models import Category
from ..readtracker.privatethreads import get_unread_private_threads
from ..readtracker.tracker import annotate_categories_read_time

if TYPE_CHECKING:
    from ..users.models import User


def sync_user_unread_private_threads(get_response):
    def middleware(request):
        if request.user.is_authenticated and request.user.sync_unread_private_threads:
            user = request.user
            category = get_private_threads_category(user)
            queryset = get_unread_private_threads(request, category, category.read_time)
            update_user_unread_private_threads(user, queryset.count())

        return get_response(request)

    return middleware


def get_private_threads_category(user: "User") -> Category:
    return annotate_categories_read_time(
        user,
        Category.objects.filter(tree_id=CategoryTree.PRIVATE_THREADS),
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
