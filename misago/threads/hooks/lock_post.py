from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Post


class LockPostHookAction(Protocol):
    """
    Misago function for locking a post.

    # Arguments

    ## `post: Post`

    A `Post` to lock.

    ## `commit: bool = True`

    Whether the updated post instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `True` if the post was locked, `False` otherwise.
    """

    def __call__(
        self,
        post: Post,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool: ...


class LockPostHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: LockPostHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `post: Post`

    A `Post` to lock.

    ## `commit: bool = True`

    Whether the updated post instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `True` if the post was locked, `False` otherwise.
    """

    def __call__(
        self,
        action: LockPostHookAction,
        post: Post,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool: ...


class LockPostHook(
    FilterHook[
        LockPostHookAction,
        LockPostHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to
    lock a post.

    # Example

    Register user who locked the post.

    ```python
    from django.http import HttpRequest
    from misago.posts.hooks import lock_post_hook
    from misago.posts.models import Post


    @lock_post_hook.append_filter
    def register_user_that_locked_post(
        action,
        post: Post,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool:
        if not action(post, commit=False, request=request):
            return False

        if request:
            post.plugin_data["locked_by"] = request.user.id

        if commit:
            post.save()

        return True
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: LockPostHookAction,
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


lock_post_hook = LockPostHook()
