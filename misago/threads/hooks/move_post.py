from typing import Protocol

from django.http import HttpRequest

from ...categories.models import Category
from ...plugins.hooks import FilterHook
from ..models import Post, Thread


class MovePostHookAction(Protocol):
    """
    Misago function for moving a post to a new thread.

    # Arguments

    ## `post: Post`

    A `Post` to move.

    ## `new_thread: Thread`

    The `Thread` to move the post to.

    ## `commit: bool = True`

    Whether the updated post instance should be saved to the database.

    Defaults to `True`.

    The post's related objects are always updated,
    even if this option is set to `False`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `True` if the post was moved, `False` otherwise.
    """

    def __call__(
        self,
        post: Post,
        new_thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool: ...


class MovePostHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: MovePostHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `post: Post`

    A `Post` to move.

    ## `new_thread: Thread`

    The `Thread` to move the post to.

    ## `commit: bool = True`

    Whether the updated post instance should be saved to the database.

    Defaults to `True`.

    The post's related objects are always updated,
    even if this option is set to `False`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `True` if the post was moved, `False` otherwise.
    """

    def __call__(
        self,
        action: MovePostHookAction,
        post: Post,
        new_thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool: ...


class MovePostHook(
    FilterHook[
        MovePostHookAction,
        MovePostHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to
    move a thread to a new category.

    # Example

    Move plugin models associated with the thread along with it:

    ```python
    from django.http import HttpRequest
    from misago.threads.hooks import move_post_hook
    from misago.threads.models import Post, Thread

    from .models import PluginModel


    @move_post_hook.append_filter
    def move_plugin_models_to_new_thread(
        action,
        post: Post,
        new_thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ):
        if not action(post, new_thread, commit, request):
            return False

        PluginModel.objects.filter(
            post=post
        ).update(thread=new_thread, category=new_thread.category)

        return True
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: MovePostHookAction,
        post: Post,
        new_thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool:
        return super().__call__(
            action,
            post,
            new_thread,
            commit,
            request,
        )


move_post_hook = MovePostHook()
