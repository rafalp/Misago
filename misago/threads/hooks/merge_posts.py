from typing import Iterable, Protocol

from django.db.models import Model
from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Post


class MergePostsHookAction(Protocol):
    """
    Misago function for merging posts.

    # Arguments

    ## `target: Post`

    The `Post` to merge `posts` into.

    ## `posts: Iterable[Post]`

    An iterable of `Post` instances to merge into `target`.

    These posts are deleted during the merge.

    ## `conflicts: dict[str, Model]`

    A `dict` with the conflict resolutions to use during the merge.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    The `Post` instance.
    """

    def __call__(
        self,
        target: Post,
        posts: Iterable[Post],
        conflicts: dict[str, Model],
        request: HttpRequest | None = None,
    ) -> Post: ...


class MergePostsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: MergePostsHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `target: Post`

    The `Post` to merge `posts` into.

    ## `posts: Iterable[Post]`

    An iterable of `Post` instances to merge into `target`.

    These posts are deleted during the merge.

    ## `conflicts: dict[str, Model]`

    A `dict` with the conflict resolutions to use during the merge.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    The `Post` instance.
    """

    def __call__(
        self,
        action: MergePostsHookAction,
        target: Post,
        posts: Iterable[Post],
        conflicts: dict[str, Model],
        request: HttpRequest | None = None,
    ) -> Post: ...


class MergePostsHook(
    FilterHook[
        MergePostsHookAction,
        MergePostsHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to merge posts.

    # Example

    Update `PluginModel` objects during the merge

    ```python
    from typing import Iterable

    from django.db.models import Model
    from django.http import HttpRequest
    from misago.posts.hooks import merge_posts_hook
    from misago.posts.models import Post
    from myplugin.models import PluginModel


    @merge_posts_hook.append_filter
    def get_plugin_merge_conflicts(
        action,
        target: Post,
        posts: Iterable[Post],
        conflicts: dict[str, Model],
        request: HttpRequest | None = None,
    ) -> Post:
        PluginModel.objects.filter(post__in=posts).update(
            category=target.category, post=target
        )

        return action(target, posts, conflicts, request)
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: MergePostsHookAction,
        target: Post,
        posts: Iterable[Post],
        conflicts: dict[str, Model],
        request: HttpRequest | None = None,
    ) -> Post:
        return super().__call__(action, target, posts, conflicts, request)


merge_posts_hook = MergePostsHook()
