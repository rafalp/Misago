from typing import Protocol

from django.template import Context

from ...plugins.hooks import FilterHook
from ...threads.models import Thread


class ReplaceRichTextTokensHookAction(Protocol):
    """
    Misago function used to replace rich-text tokens in pre-rendered
    HTML or the next filter from another plugin.

    # Arguments

    ## `html: str`

    An HTML string in which tokens will be replaced.

    ## `context: Context`

    Current template context.

    ## `data: dict`

    Data that can be embedded in HTML.

    ## `thread: Thread | None`

    Current `Thread` instance of `None`.

    # Return value

    A `str` with HTML that has its tokens replaced.
    """

    def __call__(
        self,
        html: str,
        context: Context,
        data: dict,
        thread: Thread | None,
    ) -> str: ...


class ReplaceRichTextTokensHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: ReplaceRichTextTokensHookAction`

    Misago function used to replace rich-text tokens in pre-rendered
    HTML or the next filter from another plugin.

    See the [action](#action) section for details.

    ## `html: str`

    An HTML string in which tokens will be replaced.

    ## `context: Context`

    Current template context.

    ## `data: dict`

    Data that can be embedded in HTML.

    ## `thread: Thread | None`

    Current `Thread` instance of `None`.

    # Return value

    A `str` with HTML that has its tokens replaced.
    """

    def __call__(
        self,
        action: ReplaceRichTextTokensHookAction,
        html: str,
        context: Context,
        data: dict,
        thread: Thread | None,
    ) -> str: ...


class ReplaceRichTextTokensHook(
    FilterHook[ReplaceRichTextTokensHookAction, ReplaceRichTextTokensHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to replace rich-text
    tokens in pre-rendered HTML or the next filter from another plugin.

    Tokens are pseudo-HTML elements like `<misago-attachment="..">` that are replaced
    with real HTML markup instead.

    # Example

    The code below implements a custom filter function that replaces `<you>`
    pseudo-HTML element with current user's username.

    ```python
    from django.template import Context
    from misago.parser.hooks import replace_rich_text_tokens_hook


    @replace_rich_text_tokens_hook.append_filter
    def replace_rich_text_user_name(
        action,
        html: str,
        context: Context,
        data: dict,
        thread: Thread | None,
    ) -> str:
        if "<you>" in html:
            username = user.username if user and user.is_authenticated else "Guest"
            html = html.replace("<you>", username)

        # Call the next function in chain
        return action(html, context, data, thread)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: ReplaceRichTextTokensHookAction,
        html: str,
        context: Context,
        data: dict,
        thread: Thread | None,
    ) -> str:
        return super().__call__(action, html, context, data, thread)


replace_rich_text_tokens_hook = ReplaceRichTextTokensHook()
