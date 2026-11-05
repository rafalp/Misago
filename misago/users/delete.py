from typing import Any

from django.contrib.auth import get_user_model
from django.db import transaction

from ..notifications.utils import delete_user_account, delete_user_data
from ..threads.delete import delete_user_threads
from ..threads.utils import remove_private_threads_without_members
from .anonymize import anonymize_user_data
from .avatars import delete_avatar
from .enums import DeleteUserContentAction
from .hooks import (
    anonymize_user_data_hook,
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
        if anonymous_username:
            anonymize_user_data_hook(
                _anonymize_user_data_action,
                user,
                anonymous_username,
            )
        else:
            raise ValueError("delete_user() requires 'anonymous_username' argument")

        # Execute user deletion through the hook.
        delete_user_hook(
            _delete_user_action,
            user,
            content_action,
            context=context,
        )


def _anonymize_user_data_action(
    user: User,
    anonymous_username: str,
):
    anonymize_user_data(user, anonymous_username)


def _delete_user_action(
    user: User,
    content_action: DeleteUserContentAction,
    *,
    context: dict[str, Any] | None = None,
):
    # 1. Handle user's content.

    if content_action == DeleteUserContentAction.DELETE:
        delete_user_content(user)
    elif content_action == DeleteUserContentAction.HIDE:
        hide_user_content(user)

    # 2. Delete user's avatar.

    delete_avatar(user)

    # 3. Delete user's account-related data.
    # user.pre_delete signal is received by notifications/threads handlers.

    delete_user_account(user)

    # According to #1952, this should happen after user.delete().
    # This behavior should be changed to meet the required criteria.

    remove_private_threads_without_members(user)

    # 4. Call Django's built-in model deletion method.

    user.delete()


def delete_user_content(user: User):
    delete_user_data(user)
    delete_user_threads(user)


def hide_user_content(user: User):
    # TODO: implement hide user content
    pass
