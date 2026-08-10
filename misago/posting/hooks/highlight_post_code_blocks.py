from typing import Protocol

from ...plugins.hooks import FilterHook
from ...threads.models import Post


class HighlightPostCodeBlocksHookAction(Protocol):
    """
    Misago function used to highlight a post's code blocks after it has been saved.

    # Arguments

    ## `post: Post`

    The `Post` instance to update.
    """

    def __call__(self, post: Post): ...


class HighlightPostCodeBlocksHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    The next function registered in this hook, either a custom function or
    Misago's default.

    See the [action](#action) section for details.

    ## `post: Post`

    The `Post` instance to update.
    """

    def __call__(self, action: HighlightPostCodeBlocksHookAction, post: Post): ...


class HighlightPostCodeBlocksHook(
    FilterHook[HighlightPostCodeBlocksHookAction, HighlightPostCodeBlocksHookFilter]
):
    """
    This hook wraps a standard Misago function used to highlight a post's
    code blocks after it has been saved.

    The standard code highlighting feature runs in a Celery task because Pygments
    can get stuck in an infinite loop due to unknown bugs or malicious input.

    # Example

    The code below implements a custom filter function that highlights code using
    a custom implementation:

    ```python
    from misago.posting.hooks import highlight_post_code_blocks_hook
    from misago.threads.models import Post


    @highlight_post_code_blocks_hook.append_filter
    def plugin_highlight_post_code_blocks(action, post: Post):
        if post.metadata.get("highlight_code"):
            post.content_parsed = custom_highlight_code_util(post.content_parsed)
            post.metadata.pop("highlight_code")
            post.save(update_fields=["parsed", "metadata"])
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: HighlightPostCodeBlocksHookAction,
        post: Post,
    ):
        return super().__call__(action, post)


highlight_post_code_blocks_hook = HighlightPostCodeBlocksHook()
