from ..categories.models import Category
from ..threads.models import Post, Thread
from .proxy import UserPermissionsProxy


def check_like_post_permission(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    post: Post,
):
    pass


def check_see_post_likes_permission(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    post: Post,
):
    pass
