from typing import Any

from django.contrib.auth import get_user_model
from django.db import transaction

from ..notifications.utils import delete_user_account, delete_user_data
from ..threads.delete import delete_user_threads
from ..threads.hide import hide_thread, hide_post
from ..threads.utils import remove_private_threads_without_members
from .anonymize import anonymize_user_data
from .avatars import delete_avatar
from .enums import DeleteUserContentAction
from .hooks import (
    delete_user_hook,
)

User = get_user_model()

__all__ = ["delete_user"]


def delete_user(
    user: User,
    content_action: DeleteUserContentAction,
    anonymous_username: str | None,
    *,
    context: dict[str, Any] | None = None,
):
    with transaction.atomic():
        user.lock()

        if anonymous_username:
            anonymize_user_data(
                user,
                anonymous_username,
                context = context
            )

        delete_user_hook(
            _delete_user_action,
            user,
            content_action,
            context = context,
        )


def _delete_user_action(
    user: User,
    content_action: DeleteUserContentAction,
    *,
    context: dict[str, Any] | None = None,
):
    if content_action == DeleteUserContentAction.DELETE:
        delete_user_content(user)
    elif content_action == DeleteUserContentAction.HIDE:
        hide_user_content(user)

    delete_avatar(user)
    delete_user_account(user)
    remove_private_threads_without_members(user)

    user.delete()



def delete_user_content(user: User):
    delete_user_data(user)
    delete_user_threads(user)


def hide_user_content(user: User):

    categories_to_sync = set()

    threads = profile.thread_set.select_related(
        "category", "first_post"
    ).filter(is_hidden=False)
    for thread in threads.iterator(chunk_size=50):
        categories_to_sync.add(thread.category_id)
        hide_thread(thread, user)

    posts = profile.post_set.select_related(
        "category", "thread", "thread__category"
    ).filter(is_hidden=False)
    for post in posts.iterator(chunk_size=50):
        categories_to_sync.add(post.category_id)
        hide_post(post, user, request=None)
        synchronize_thread(post.thread)

    categories = Category.objects.filter(id__in=categories_to_sync)
    for category in categories.iterator():
        synchronize_category(category)
