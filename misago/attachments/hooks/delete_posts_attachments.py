from typing import Iterable, Protocol, Union

from django.http import HttpRequest

from ...threads.models import Post
from ...plugins.hooks import FilterHook


class DeletePostsAttachmentsHookAction(Protocol):
    """
    A standard function used by Misago to delete attachments associated with
    specified posts.

    # Arguments

    ## `posts: Iterable[Union[Post, int]]`

    An iterable of posts or their IDs.

    ## `request: HttpRequest | None`

    The request object or `None`.

    # Return value

    An `int` with the number of attachments marked for deletion.
    """

    def __call__(
        self,
        posts: Iterable[Union[Post, int]],
        *,
        request: HttpRequest | None = None,
    ) -> int: ...


class DeletePostsAttachmentsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: DeletePostsAttachmentsHookAction`

    A standard function used by Misago to delete attachments associated with
    specified posts.

    See the [action](#action) section for details.

    ## `posts: Iterable[Union[Post, int]]`

    An iterable of posts or their IDs.

    ## `request: HttpRequest | None`

    The request object or `None`.

    # Return value

    An `int` with the number of attachments marked for deletion.
    """

    def __call__(
        self,
        action: DeletePostsAttachmentsHookAction,
        posts: Iterable[Union[Post, int]],
        *,
        request: HttpRequest | None = None,
    ) -> int: ...


class DeletePostsAttachmentsHook(
    FilterHook[
        DeletePostsAttachmentsHookAction,
        DeletePostsAttachmentsHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to delete
    attachments associated with specified posts.

    # Example

    The code below implements a custom filter function that logs delete.

    ```python
    import logging
    from typing import Iterable, Protocol, Union

    from django.http import HttpRequest
    from misago.attachments.hooks import delete_posts_attachments_hook
    from misago.threads.models import Post

    logger = logging.getLogger("attachments.delete")


    @delete_posts_attachments_hook.append_filter
    def log_delete_posts_attachments(
        action,
        posts: Iterable[Union[Post, int]],
        *,
        request: HttpRequest | None = None,
    ) -> int:
        deleted = action(posts, request=request)

        if request and request.user.is_authenticated:
            user = f"#{request.user.id}: {request.user.username}"
        else:
            user = None

        logger.info(
            "Deleted posts attachments: %s",
            str(deleted),
            extra={"user": user},
        )

        return deleted
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: DeletePostsAttachmentsHookAction,
        posts: Iterable[Union[Post, int]],
        *,
        request: HttpRequest | None = None,
    ) -> int:
        return super().__call__(action, posts, request=request)


delete_posts_attachments_hook = DeletePostsAttachmentsHook()
