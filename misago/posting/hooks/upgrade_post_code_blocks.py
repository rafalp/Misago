from typing import Protocol

from ...plugins.hooks import FilterHook
from ...threads.models import Post


class UpgradePostCodeBlocksHookAction(Protocol):
    """
    Misago function used to upgrade a post's code blocks or the next
    filter function from another plugin.

    # Arguments

    ## `post: Post`

    The `Post` instance to update.
    """

    def __call__(self, post: Post): ...


class UpgradePostCodeBlocksHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    The next function registered in this hook, either a custom function or
    Misago's default.

    See the [action](#action) section for details.

    ## `post: Post`

    The `Post` instance to update.
    """

    def __call__(self, action: UpgradePostCodeBlocksHookAction, post: Post): ...


class UpgradePostCodeBlocksHook(
    FilterHook[UpgradePostCodeBlocksHookAction, UpgradePostCodeBlocksHookFilter]
):
    """
    This hook wraps a standard Misago function used to upgrade a post's
    code blocks after it has been posted.

    The standard code highlighting feature runs in a Celery task because Pygments
    can get stuck in an infinite loop due to unknown bugs or malicious input.

    # Example

    The code below implements a custom filter function that highlights code using
    custom implementation:

    ```python
    from misago.posting.hooks import upgrade_post_code_blocks_hook
    from misago.threads.models import Post


    @upgrade_post_code_blocks_hook.append_filter
    def plugin_upgrade_post_code_blocks(action, post: Post):
        if post.metadata.get("highlight_code"):
            post.parsed = custom_highlight_code_util(post.parsed)
            post.metadata.pop("highlight_code")
            post.save(update_fields=["parsed", "metadata"])
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: UpgradePostCodeBlocksHookAction,
        post: Post,
    ):
        return super().__call__(action, post)


upgrade_post_code_blocks_hook = UpgradePostCodeBlocksHook()
