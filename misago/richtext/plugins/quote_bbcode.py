import re
from typing import Optional


QUOTE_OPEN_PATTERN = re.compile(r"\[quote(=([\w\-_]*)(:\d+)?)?\]", re.IGNORECASE)
QUOTE_CLOSE_PATTERN = re.compile(r"\[\/quote\]", re.IGNORECASE)


def parse_quote_open_bbcode(parser, m, state):
    author = m.group(2) or ""

    try:
        post = int((m.group(3) or "").lstrip(":").strip())
    except (TypeError, ValueError):
        post = None

    return {
        "type": "block_open",
        "params": (
            {
                "type": "quote_bbcode",
                "author": author or None,
                "post": post if post and post > 0 else None,
            },
        ),
    }


def parse_quote_close_bbcode(parser, m, state):
    return {
        "type": "block_close",
        "params": ({"type": "quote_bbcode"},),
    }


def render_ast_quote_open_bbcode(children, data):
    return {"type": "block_open", "data": data}


def render_ast_quote_close_bbcode(children):
    return {"type": "block_close"}


def plugin_quote_bbcode(markdown):
    markdown.block.register_rule(
        "quote_open_bbcode", QUOTE_OPEN_PATTERN, parse_quote_open_bbcode
    )
    markdown.block.register_rule(
        "quote_close_bbcode", QUOTE_CLOSE_PATTERN, parse_quote_close_bbcode
    )
    markdown.block.rules.append("quote_open_bbcode")
    markdown.block.rules.append("quote_close_bbcode")

    if markdown.renderer.NAME == "ast":
        markdown.renderer.register("quote_open_bbcode", render_ast_quote_open_bbcode)
        markdown.renderer.register("quote_close_bbcode", render_ast_quote_close_bbcode)
