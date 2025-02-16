from typing import TYPE_CHECKING, Iterable, Protocol, Union

from django.http import HttpRequest

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ...users.models import User


class DeleteUsersAttachmentsHookAction(Protocol):
    """
    A standard function used by Misago to delete attachments associated with
    specified users.

    # Arguments

    ## `users: Iterable[Union[User, int]]`

    An iterable of users or their IDs.

    ## `request: HttpRequest | None`

    The request object or `None`.

    # Return value

    An `int` with the number of attachments marked for deletion.
    """

    def __call__(
        self,
        users: Iterable[Union["User", int]],
        *,
        request: HttpRequest | None = None,
    ) -> int: ...


class DeleteUsersAttachmentsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: DeleteUsersAttachmentsHookAction`

    A standard function used by Misago to delete attachments associated with
    specified users.

    See the [action](#action) section for details.

    ## `users: Iterable[Union[User, int]]`

    An iterable of users or their IDs.

    ## `request: HttpRequest | None`

    The request object or `None`.

    # Return value

    An `int` with the number of attachments marked for deletion.
    """

    def __call__(
        self,
        action: DeleteUsersAttachmentsHookAction,
        users: Iterable[Union["User", int]],
        *,
        request: HttpRequest | None = None,
    ) -> int: ...


class DeleteUsersAttachmentsHook(
    FilterHook[
        DeleteUsersAttachmentsHookAction,
        DeleteUsersAttachmentsHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to delete
    attachments associated with specified users.

    # Example

    The code below implements a custom filter function that logs delete.

    ```python
    import logging
    from typing import Iterable, Protocol, Union

    from django.http import HttpRequest
    from misago.attachments.hooks import delete_users_attachments_hook
    from misago.users.models import User

    logger = logging.getLogger("attachments.delete")


    @delete_users_attachments_hook.append_filter
    def log_delete_users_attachments(
        action,
        users: Iterable[Union[User, int]],
        *,
        request: HttpRequest | None = None,
    ) -> int:
        deleted = action(users, request=request)

        if request and request.user.is_authenticated:
            user = f"#{request.user.id}: {request.user.username}"
        else:
            user = None

        logger.info(
            "Deleted users attachments: %s",
            str(deleted),
            extra={"user": user},
        )

        return deleted
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: DeleteUsersAttachmentsHookAction,
        users: Iterable[Union["User", int]],
        *,
        request: HttpRequest | None = None,
    ) -> int:
        return super().__call__(action, users, request=request)


delete_users_attachments_hook = DeleteUsersAttachmentsHook()
