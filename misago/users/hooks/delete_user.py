from typing import Any, Protocol

from ...plugins.hooks import FilterHook
from ..enums import DeleteUserContentAction
from ..models import User


class DeleteUserHookAction(Protocol):
    """
    Standard function used by Misago to delete a user.

    Arguments:

    user:
        User instance that will be deleted.

    content_action:
        Action determining what happens to user's content.

    context:
        Additional context passed to the deletion action.
    """

    def __call__(
        self,
        user: User,
        content_action: DeleteUserContentAction,
        *,
        context: dict[str, Any] | None = None,
    ) -> None: ...


class DeleteUserHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered
    in this hook.
    """

    def __call__(
        self,
        action: DeleteUserHookAction,
        user: User,
        content_action: DeleteUserContentAction,
        *,
        context: dict[str, Any] | None = None,
    ) -> None: ...


class DeleteUserHook(
    FilterHook[
        DeleteUserHookAction,
        DeleteUserHookFilter,
    ]
):
    """
    Hook that wraps the standard function used by Misago
    to delete a user.

    Plugins can execute custom logic before and after deletion,
    modify arguments, or prevent the original action.
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: DeleteUserHookAction,
        user: User,
        content_action: DeleteUserContentAction,
        *,
        context: dict[str, Any] | None = None,
    ) -> None:
        return super().__call__(
            action,
            user,
            content_action,
            context=context,
        )


delete_user_hook = DeleteUserHook()
