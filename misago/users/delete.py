from typing import Any

from ..notifications.utils import delete_user_account, delete_user_data
from ..threads.delete import delete_user_threads
from ..threads.utils import remove_private_threads_without_members
from .anonymize import anonymize_user_data
from .avatars import delete_avatar
from .enums import DeleteUserContentAction
from .models import User

__all__ = ["delete_user"]


def delete_user(
    user: User,
    content_action: DeleteUserContentAction,
    anonymous_username: str | None,
    *,
    context: dict[str, Any] | None = None,
):
    # called functions based on code / signals
    # 1. user.delete()
    # extracted from user.delete()
    if content_action == DeleteUserContentAction.DELETE:
        delete_user_content(user)
    elif content_action == DeleteUserContentAction.HIDE:
        hide_user_content(user)

    if anonymous_username:
        anonymize_user_data(user, anonymous_username)
    else:
        raise ValueError("delete_user() requires 'anonymous_username' argument")

    delete_avatar(user)

    # 2. user.pre_delete signal is received by notifications/threads handlers
    delete_user_account(user)
    # according to #1952 it should be after user.delete()
    # and should be changed to meet criteria
    remove_private_threads_without_members(user)

    # calls Dj build-in model method
    user.delete()


def delete_user_content(user: User):
    delete_user_data(user)
    delete_user_threads(user)


def hide_user_content(user: User):
    # TODO: implement hide user content
    pass
