from mistune import Markdown

from .genericblock import parse_generic_block_close, parse_generic_block_open


SPOILER_OPEN_PATTERN = r"(\s+)?\[spoiler\](\s+)?"
SPOILER_CLOSE_PATTERN = r"(\s+)?\[\/spoiler\](\s+)?"


@parse_generic_block_open
def parse_spoiler_open_bbcode(parser, m, state: dict):
    return {"type": "spoiler_bbcode"}


@parse_generic_block_close
def parse_spoiler_close_bbcode(parser, m, state: dict):
    return {"type": "spoiler_bbcode"}


def plugin_spoiler_bbcode(markdown: Markdown):
    markdown.inline.register_rule(
        "spoiler_open_bbcode", SPOILER_OPEN_PATTERN, parse_spoiler_open_bbcode
    )
    markdown.inline.register_rule(
        "spoiler_close_bbcode", SPOILER_CLOSE_PATTERN, parse_spoiler_close_bbcode
    )
    markdown.inline.rules.append("spoiler_open_bbcode")
    markdown.inline.rules.append("spoiler_close_bbcode")
