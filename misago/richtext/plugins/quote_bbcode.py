import re
from typing import Optional


QUOTE_PATTERN = re.compile(r"\[quote(=([\w\-_]*)(:\d+)?)?\](.*)\[\/quote\]")


def parse_quote_bbcode(parser, m, state):
    author = m.group(2) or ""

    try:
        post = int((m.group(3) or "").lstrip(":").strip())
    except (TypeError, ValueError):
        post = None

    return {
        "type": "quote_bbcode",
        "children": parser.parse(m.group(4), state),
        "params": (author.strip(), post),
    }


def render_ast_quote_bbcode(
    children, author: Optional[str] = None, post: Optional[int] = None
):
    return {
        "type": "quote_bbcode",
        "author": author or None,
        "post": post if post and post > 0 else None,
        "children": children,
    }


def plugin_quote_bbcode(markdown):
    markdown.block.register_rule("quote_bbcode", QUOTE_PATTERN, parse_quote_bbcode)
    markdown.block.rules.append("quote_bbcode")

    if markdown.renderer.NAME == "ast":
        markdown.renderer.register("quote_bbcode", render_ast_quote_bbcode)
