from typing import Iterable, Protocol, Union

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Attachment


class DeleteAttachmentsHookAction(Protocol):
    """
    A standard function used by Misago to delete specified attachments.

    # Arguments

    ## `attachments: Iterable[Union[Attachment, int]]`

    An iterable of attachments or their IDs.

    ## `request: HttpRequest | None`

    The request object or `None`.

    # Return value

    An `int` with the number of attachments marked for deletion.
    """

    def __call__(
        self,
        attachments: Iterable[Union[Attachment, int]],
        *,
        request: HttpRequest | None = None,
    ) -> int: ...


class DeleteAttachmentsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: DeleteAttachmentsHookAction`

    A standard function used by Misago to delete specified attachments.

    See the [action](#action) section for details.

    ## `attachments: Iterable[Union[Attachment, int]]`

    An iterable of attachments or their IDs.

    ## `request: HttpRequest | None`

    The request object or `None`.

    # Return value

    An `int` with the number of attachments marked for deletion.
    """

    def __call__(
        self,
        action: DeleteAttachmentsHookAction,
        attachments: Iterable[Union[Attachment, int]],
        *,
        request: HttpRequest | None = None,
    ) -> int: ...


class DeleteAttachmentsHook(
    FilterHook[
        DeleteAttachmentsHookAction,
        DeleteAttachmentsHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to delete
    specified attachments.

    # Example

    The code below implements a custom filter function that logs delete.

    ```python
    import logging
    from typing import Iterable, Protocol, Union

    from django.http import HttpRequest
    from misago.attachments.hooks import delete_attachments_hook
    from misago.attachments.models import Attachment

    logger = logging.getLogger("attachments.delete")


    @delete_attachments_hook.append_filter
    def log_delete_attachments(
        action,
        attachments: Iterable[Union[Attachment, int]],
        *,
        request: HttpRequest | None = None,
    ) -> int:
        deleted = action(attachments, request=request)

        if request and request.user.is_authenticated:
            user = f"#{request.user.id}: {request.user.username}"
        else:
            user = None

        logger.info(
            "Deleted attachments: %s",
            str(deleted),
            extra={"user": user},
        )

        return deleted
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: DeleteAttachmentsHookAction,
        attachments: Iterable[Union[Attachment, int]],
        *,
        request: HttpRequest | None = None,
    ) -> int:
        return super().__call__(action, attachments, request=request)


delete_attachments_hook = DeleteAttachmentsHook()
