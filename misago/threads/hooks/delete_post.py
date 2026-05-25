from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Post


class DeletePostHookAction(Protocol):
    """
    Misago function for deleting a post.

    # Arguments

    ## `post: Post`

    A `Post` to delete.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.
    """

    def __call__(
        self,
        post: Post,
        request: HttpRequest | None = None,
    ) -> None: ...


class DeletePostHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: DeletePostHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `post: Post`

    A `Post` to delete.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `True` if the post was hidden, `False` otherwise.
    """

    def __call__(
        self,
        action: DeletePostHookAction,
        post: Post,
        request: HttpRequest | None = None,
    ) -> None: ...


class DeletePostHook(
    FilterHook[
        DeletePostHookAction,
        DeletePostHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to
    delete a post.

    # Example

    Delete plugin objects related to this post.

    ```python
    from django.http import HttpRequest
    from misago.postgres.delete import delete_all
    from misago.posts.hooks import delete_post_hook
    from misago.posts.models import Post
    from my_plugin.models import PostBoost


    @delete_post_hook.append_filter
    def delete_post_boosts(
        action,
        post: Post,
        request: HttpRequest | None = None,
    ) -> None:
        # Skip Django's delete collector logic
        delete_all(PostBoost, post_id=post.id)
        action(post, request)
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: DeletePostHookAction,
        post: Post,
        request: HttpRequest | None = None,
    ) -> None:
        return super().__call__(action, post, request)


delete_post_hook = DeletePostHook()
