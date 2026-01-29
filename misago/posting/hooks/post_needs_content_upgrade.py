from typing import Protocol

from ...plugins.hooks import FilterHook
from ...threads.models import Post


class PostNeedsContentUpgradeHookAction(Protocol):
    """
    Misago function used to check if post content needs an upgrade.

    # Arguments

    ## `post: Post`

    The `Post` instance to check.

    # Return value

    Returns `bool` with `True` if post content needs upgrade.
    """

    def __call__(self, post: Post) -> bool: ...


class PostNeedsContentUpgradeHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    The next function registered in this hook, either a custom function or
    Misago's default.

    See the [action](#action) section for details.

    ## `post: Post`

    The `Post` instance to update.

    # Return value

    Returns `bool` with `True` if post content needs upgrade.
    """

    def __call__(
        self,
        action: PostNeedsContentUpgradeHookAction,
        post: Post,
    ) -> bool: ...


class PostNeedsContentUpgradeHook(
    FilterHook[PostNeedsContentUpgradeHookAction, PostNeedsContentUpgradeHookFilter]
):
    """
    This hook wraps a standard Misago function used to check if post content
    needs an upgrade.

    If `True` is returned, a Celery task will be scheduled to upgrade the post content.

    # Example

    The code below implements a custom filter function that returns `True`
    if the post contains HTML markup that requires an upgrade.

    ```python
    from misago.posting.hooks import post_needs_content_upgrade_hook
    from misago.threads.models import Post


    @post_needs_content_upgrade_hook.append_filter
    def post_needs_plugin_content_upgrade(action, post: Post) -> bool:
        if "<plugin-html" in post.parsed:
            return True

        return action(post)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: PostNeedsContentUpgradeHookAction,
        post: Post,
    ) -> bool:
        return super().__call__(action, post)


post_needs_content_upgrade_hook = PostNeedsContentUpgradeHook()
