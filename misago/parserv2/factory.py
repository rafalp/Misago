from typing import Any, Iterable, Mapping

from markdown_it import MarkdownIt
from markdown_it.utils import PresetType

from .hooks import create_parser_hook
from .bbcode import formatting_bbcode_plugin


def create_parser() -> MarkdownIt:
    return create_parser_hook(
        _create_parser_action,
        config="js-default",
        options_update={"typographer": True},
        enable=["replacements", "smartquotes"],
    )


def _create_parser_action(
    *,
    config: str | PresetType,
    options_update: Mapping[str, Any] | None = None,
    enable: str | Iterable[str] | None = None,
    disable: str | Iterable[str] | None = None,
) -> MarkdownIt:
    md = MarkdownIt(config, options_update)

    formatting_bbcode_plugin(md)

    if enable:
        md.enable(enable)
    if disable:
        md.disable(disable)

    return md
