from typing import Protocol

from ...plugins.hooks import FilterHook


class FilterAstHookAction(Protocol):
    """
    A standard Misago function used to process and clean an abstract syntax tree
    returned by the parser or next filter function from another plugin.

    # Arguments

    ## `ast: list`

    A list of Python `dict`s with AST returned by the parser.

    ## `content_type: str | None = None`

    A `str` with the name of the content type (e.g., `post` or `signature`)
    or `None` if not provided.

    # Return value

    A list of Python `dict`s with an AST for parsed markup.
    """

    def __call__(
        self,
        ast: list,
        content_type: str | None = None,
    ) -> list:
        ...


class FilterAstHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: FilterAstHookAction`

    A standard Misago function used to process and clean an abstract syntax tree
    returned by the parser or next filter function from another plugin.

    See the [action](#action) section for details.

    # Arguments

    ## `ast: list`

    A list of Python `dict`s with AST returned by the parser.

    ## `content_type: str | None = None`

    A `str` with the name of the content type (e.g., `post` or `signature`)
    or `None` if not provided.

    # Return value

    A list of Python `dict`s with an AST for parsed markup.
    """

    def __call__(
        self,
        action: FilterAstHookAction,
        ast: list,
        content_type: str | None = None,
    ) -> list:
        ...


class FilterAstHook(FilterHook[FilterAstHookAction, FilterAstHookFilter]):
    """
    This hook wraps the standard function that Misago uses to filter an abstract
    syntax tree representing the contents of parsed markup.

    # Example

    The code below implements a custom filter function that adds the table Mistune
    plugin to the parser:

    ```python
    from typing import Callable, Protocol

    from django.contrib.auth import get_user_model
    from django.http import HttpRequest
    from mistune import BlockParser, InlineParser, Markdown
    from mistune.plugins.table import table

    User = get_user_model()

    @create_markdown_hook.append_filter
    def register_custom_markdown_plugin(
        action: FilterAstHookAction, *, plugins, **kwargs
    ) -> None:
        plugins.append(table)

        # Call the next function in chain
        return action(plugins=plugins, **kwargs)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: FilterAstHookAction,
        ast: list,
        content_type: str | None = None,
    ) -> list:
        return super().__call__(
            action,
            ast=ast,
            content_type=content_type,
        )


filter_ast_hook = FilterAstHook()
