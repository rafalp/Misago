from typing import Any, Callable, Iterable, Mapping, Protocol

from markdown_it import MarkdownIt
from markdown_it.utils import PresetType

from ...plugins.hooks import FilterHook


class CreateParserHookAction(Protocol):
    """
    Misago function used to create a configured MarkdownIt instance
    or the next filter function from another plugin.

    # Arguments

    ## `config: str | PresetType`

    A `str` with the name of the preset to use, or a `PresetType` instance.

    ## `options_update: Mapping[str, Any] | None = None`

    A `Mapping` with preset's options overrides.

    ## `enable: str | Iterable[str] | None = None`

    Argument to call the `MarkdownIt.enable(...)` method with.
    If empty or `None`, `enable()` will not be called.

    ## `disable: str | Iterable[str] | None = None`

    Argument to call the `MarkdownIt.disable(...)` method with.
    If empty or `None`, `disable()` will not be called.

    ## `plugins: Iterable[Callable[[MarkdownIt], None]] | None = None`

    A list of `MarkdownIt` plugins. Each plugin must be a callable that accepts
    a single argument: the `MarkdownIt` instance.

    # Return value

    An instance of the `MarkdownIt` class.
    """

    def __call__(
        self,
        *,
        config: str | PresetType,
        options_update: Mapping[str, Any] | None = None,
        enable: str | Iterable[str] | None = None,
        disable: str | Iterable[str] | None = None,
        plugins: Iterable[Callable[[MarkdownIt], None]] | None = None,
    ) -> MarkdownIt: ...


class CreateParserHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CreateParserHookAction`

    Misago function used to create a configured MarkdownIt instance
    or the next filter function from another plugin.

    See the [action](#action) section for details.

    ## `config: str | PresetType`

    A `str` with the name of the preset to use, or a `PresetType` instance.

    ## `options_update: Mapping[str, Any] | None = None`

    A `Mapping` with preset's options overrides.

    ## `enable: str | Iterable[str] | None = None`

    Argument to call the `MarkdownIt.enable(...)` method with.
    If empty or `None`, `enable()` will not be called.

    ## `disable: str | Iterable[str] | None = None`

    Argument to call the `MarkdownIt.disable(...)` method with.
    If empty or `None`, `disable()` will not be called.

    ## `plugins: Iterable[Callable[[MarkdownIt], None]] | None = None`

    A list of `MarkdownIt` plugins. Each plugin must be a callable that accepts
    a single argument: the `MarkdownIt` instance.

    # Return value

    An instance of the `MarkdownIt` class.
    """

    def __call__(
        self,
        action: CreateParserHookAction,
        *,
        config: str | PresetType,
        options_update: Mapping[str, Any] | None = None,
        enable: str | Iterable[str] | None = None,
        disable: str | Iterable[str] | None = None,
        plugins: Iterable[Callable[[MarkdownIt], None]] | None = None,
    ) -> MarkdownIt: ...


class CreateParserHook(FilterHook[CreateParserHookAction, CreateParserHookFilter]):
    """
    This hook wraps the standard function that Misago uses to create a configured
    MarkdownIt instance.

    # Example

    The code below implements a custom filter function that disables automatic
    linkification in parsed messages:

    ```python
    from typing import Any, Callable, Iterable, Mapping

    from markdown_it import MarkdownIt
    from markdown_it.utils import PresetType
    from misago.parser.hooks import create_parser_hook


    @create_parser_hook.append_filter
    def create_customized_parser(
        action,
        *,
        config: str | PresetType,
        options_update: Mapping[str, Any] | None = None,
        enable: str | Iterable[str] | None = None,
        disable: str | Iterable[str] | None = None,
        plugins: Iterable[Callable[[MarkdownIt], None]] | None = None,
    ) -> Parser:
        options_update["linkify"] = False

        return action(
            config=config,
            options_update=options_update,
            enable=enable,
            disable=disable,
            plugins=plugins,
        )
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CreateParserHookAction,
        *,
        config: str | PresetType,
        options_update: Mapping[str, Any] | None = None,
        enable: str | Iterable[str] | None = None,
        disable: str | Iterable[str] | None = None,
        plugins: Iterable[Callable[[MarkdownIt], None]] | None = None,
    ) -> MarkdownIt:
        return super().__call__(
            action,
            config=config,
            options_update=options_update,
            enable=enable,
            disable=disable,
            plugins=plugins,
        )


create_parser_hook = CreateParserHook()
