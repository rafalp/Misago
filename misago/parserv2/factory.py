from typing import Any, Callable, Iterable, Mapping

from markdown_it import MarkdownIt
from markdown_it.utils import PresetType

from .hooks import create_parser_hook
from .bbcode import formatting_bbcode_plugin
from .rules import set_link_target_blank_rule


def create_parser() -> MarkdownIt:
    return create_parser_hook(
        _create_parser_action,
        config="js-default",
        options_update={"typographer": True, "linkify": True},
        enable=["replacements", "smartquotes"],
        render_rules=[
            ("link_open", set_link_target_blank_rule),
        ],
    )


def _create_parser_action(
    *,
    config: str | PresetType,
    options_update: Mapping[str, Any] | None = None,
    enable: str | Iterable[str] | None = None,
    disable: str | Iterable[str] | None = None,
    render_rules: Iterable[tuple[str, Callable]] | None = None,
) -> MarkdownIt:
    md = MarkdownIt(config, options_update)

    if render_rules:
        for rule_name, rule_func in render_rules:
            md.add_render_rule(rule_name, rule_func)

    formatting_bbcode_plugin(md)

    if enable:
        md.enable(enable)
    if disable:
        md.disable(disable)

    return md
