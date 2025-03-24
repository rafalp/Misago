from typing import Any, Callable, Iterable, Mapping

from markdown_it import MarkdownIt
from markdown_it.utils import PresetType

from .hooks import create_parser_hook
from .plugins import (
    attachment_plugin,
    formatting_bbcode_plugin,
    link_target_blank_plugin,
    quote_bbcode_plugin,
)


def create_parser() -> MarkdownIt:
    return create_parser_hook(
        _create_parser_action,
        config="js-default",
        options_update={"typographer": True, "linkify": True},
        enable=["replacements", "smartquotes"],
        plugins=[
            attachment_plugin,
            formatting_bbcode_plugin,
            link_target_blank_plugin,
            quote_bbcode_plugin,
        ],
    )


def _create_parser_action(
    *,
    config: str | PresetType,
    options_update: Mapping[str, Any] | None = None,
    enable: str | Iterable[str] | None = None,
    disable: str | Iterable[str] | None = None,
    plugins: Iterable[Callable[[MarkdownIt], None]] | None = None,
) -> MarkdownIt:
    md = MarkdownIt(config, options_update)

    if plugins:
        for plugin in plugins:
            plugin(md)

    if enable:
        md.enable(enable)
    if disable:
        md.disable(disable)

    return md
