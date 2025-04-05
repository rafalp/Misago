from typing import TYPE_CHECKING, Protocol, Union

from django.contrib.auth.models import AnonymousUser

from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ...users.models import User


class ReplaceRichTextTokensHookAction(Protocol):
    """
    A standard Misago function used to replace rich-text tokens in pre-rendered
    HTML or the next filter from another plugin.

    # Arguments

    ## `html: str`

    An HTML string in which tokens will be replaced.

    ## `data: dict`

    Data that can be embedded in HTML.

    ## `user: AnonymousUser | User | None`

    `AnonymousUser`, authenticated `User` or `None`.

    ## `thread: Thread | None`

    Current `Thread` instance of `None`.

    # Return value

    A `str` with HTML that has its tokens replaced.
    """

    def __call__(
        self,
        html: str,
        data: dict,
        user: Union[AnonymousUser, "User", None],
        thread: Thread | None,
    ) -> str: ...


class ReplaceRichTextTokensHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: ReplaceRichTextTokensHookAction`

    A standard Misago function used to replace rich-text tokens in pre-rendered
    HTML or the next filter from another plugin.

    See the [action](#action) section for details.

    ## `html: str`

    An HTML string in which tokens will be replaced.

    ## `data: dict`

    Data that can be embedded in HTML.

    ## `user: AnonymousUser | User | None`

    `AnonymousUser`, authenticated `User` or `None`.

    ## `thread: Thread | None`

    Current `Thread` instance of `None`.

    # Return value

    A `str` with HTML that has its tokens replaced.
    """

    def __call__(
        self,
        action: ReplaceRichTextTokensHookAction,
        html: str,
        data: dict,
        user: Union[AnonymousUser, "User", None],
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
    from django.contrib.auth.models import AnonymousUser
    from misago.parser.hooks import replace_rich_text_tokens_hook
    from misago.users.models import User


    @replace_rich_text_tokens_hook.append_filter
    def replace_rich_text_user_name(
        action,
        html: str,
        data: dict,
        user: AnonymousUser | User | None,
        thread: Thread | None,
    ) -> str:
        if "<you>" in html:
            username = user.username if user and user.is_authenticated else "Guest"
            html = html.replace("<you>", username)

        # Call the next function in chain
        return action(html, data, user, thread)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: ReplaceRichTextTokensHookAction,
        html: str,
        data: dict,
        user: Union[AnonymousUser, "User", None],
        thread: Thread | None,
    ) -> str:
        return super().__call__(action, html, data, user, thread)


replace_rich_text_tokens_hook = ReplaceRichTextTokensHook()
