from enum import StrEnum
from typing import Any

from ..notifications.utils import delete_user_account
from ..threads.utils import remove_private_threads_without_members
from .avatars import delete_avatar
from .models import User

__all__ = ["delete_user", "UserContentAction"]


class UserContentAction(StrEnum):
    DELETE = "DELETE"
    HIDE = "HIDE"
    LEAVE = "LEAVE"


def delete_user(
    user: User,
    content_action: UserContentAction,
    anonymous_username: str | None,
    *,
    context: dict[str, Any] | None = None,
):
    # called functions based on code / signals
    # 1. user.delete()
    # extracted from user.delete()
    if content_action == UserContentAction.DELETE:
        user.delete_content()

    if anonymous_username:
        user.anonymize_data(anonymous_username)
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
