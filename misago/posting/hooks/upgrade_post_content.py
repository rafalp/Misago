from typing import Protocol

from ...plugins.hooks import FilterHook
from ...threads.models import Post


class UpgradePostContentHookAction(Protocol):
    """
    A standard Misago function used to upgrade post content or the next filter
    function from another plugin.

    # Arguments

    ## `post: Post`

    The `Post` instance to update.
    """

    def __call__(self, post: Post): ...


class UpgradePostContentHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    A standard Misago function used to upgrade post content or the next filter
    function from another plugin.

    See the [action](#action) section for details.

    ## `post: Post`

    The `Post` instance to update.
    """

    def __call__(self, action: UpgradePostContentHookAction, post: Post): ...


class UpgradePostContentHook(
    FilterHook[UpgradePostContentHookAction, UpgradePostContentHookFilter]
):
    """
    This hook wraps the standard Misago function used to upgrade post content
    after it has been posted.

    The upgrade process runs in a Celery task scheduled after the post is created,
    allowing slow and costly operations, such as embedding previews of linked
    sites, to be performed without slowing down the posting process.

    # Example

    The code below implements a custom filter function that replaces custom
    plugin's HTML with new version:

    ```python
    from misago.posting.hooks import upgrade_post_content_hook
    from misago.threads.models import Post


    @upgrade_post_content_hook.append_filter
    def upgrade_post_plugin_html(action, post: Post):
        if "<plugin-html" in post.parsed:
            post.parsed = very_costful_html_change_operation(post.parsed)
            post.save(update_fields=["parsed"])

        action(post)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: UpgradePostContentHookAction,
        post: Post,
    ):
        return super().__call__(action, post)


upgrade_post_content_hook = UpgradePostContentHook()
