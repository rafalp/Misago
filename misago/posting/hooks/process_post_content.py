from typing import Protocol

from ...plugins.hooks import FilterHook
from ...threads.models import Post


class ProcessPostContentHookAction(Protocol):
    """
    Misago function used to process post content or the next filter
    function from another plugin.

    # Arguments

    ## `post: Post`

    The `Post` instance to update.
    """

    def __call__(self, post: Post): ...


class ProcessPostContentHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    The next function registered in this hook, either a custom function or
    Misago's default.

    See the [action](#action) section for details.

    ## `post: Post`

    The `Post` instance to update.
    """

    def __call__(self, action: ProcessPostContentHookAction, post: Post): ...


class ProcessPostContentHook(
    FilterHook[ProcessPostContentHookAction, ProcessPostContentHookFilter]
):
    """
    This hook wraps a standard Misago function used to process post content
    after saving.

    The process runs in a Celery task scheduled after the post is created or updated,
    allowing slow and costly operations, such as embedding previews of linked
    sites, to be performed without slowing down the posting process.

    # Example

    The code below implements a custom filter function that replaces a custom
    plugin's HTML with a new version:

    ```python
    from misago.posting.hooks import process_post_content_hook
    from misago.threads.models import Post


    @process_post_content_hook.append_filter
    def enrich_post_plugin_html(action, post: Post):
        if "<plugin-html" in post.content_parsed:
            post.content_parsed = very_costful_html_change_operation(post.content_parsed)
            post.save(update_fields=["parsed"])

        action(post)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: ProcessPostContentHookAction,
        post: Post,
    ):
        return super().__call__(action, post)


process_post_content_hook = ProcessPostContentHook()
