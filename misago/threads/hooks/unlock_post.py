from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Post


class UnlockPostHookAction(Protocol):
    """
    Misago function for unlocking a post.

    # Arguments

    ## `post: Post`

    A `Post` to unlock.

    ## `commit: bool = True`

    Whether the updated post instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `True` if the post was unlocked, `False` otherwise.
    """

    def __call__(
        self,
        post: Post,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool: ...


class UnlockPostHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: UnlockPostHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `post: Post`

    A `Post` to unlock.

    ## `commit: bool = True`

    Whether the updated post instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `True` if the post was unlocked, `False` otherwise.
    """

    def __call__(
        self,
        action: UnlockPostHookAction,
        post: Post,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool: ...


class UnlockPostHook(
    FilterHook[
        UnlockPostHookAction,
        UnlockPostHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to
    unlock a post.

    # Example

    Register user who unlocked the post.

    ```python
    from django.http import HttpRequest
    from misago.posts.hooks import unlock_post_hook
    from misago.posts.models import Post


    @unlock_post_hook.append_filter
    def register_user_that_unlocked_post(
        action,
        post: Post,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool:
        if not action(post, commit=False, request=request):
            return False

        if request:
            post.plugin_data["unlocked_by"] = request.user.id

        if commit:
            post.save()

        return True
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: UnlockPostHookAction,
        post: Post,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool:
        return super().__call__(
            action,
            post,
            commit,
            request,
        )


unlock_post_hook = UnlockPostHook()
