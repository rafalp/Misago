import re
from typing import Optional


CODE_BBCODE_PATTERN = re.compile(r"\[code(=[a-zA-Z0-9]+)?\](.*?)\[\/code\]")


def parse_code_bbcode(parser, m, state):
    info = m.group(1)
    if info:
        info = info[1:].strip()

    return {
        "type": "code_bbcode",
        "text": "",
        "params": (info or None, m.group(2)),
    }


def render_ast_code_bbcode(_, info: Optional[str], raw: str):
    return {
        "type": "block_code",
        "info": info,
        "text": raw,
    }


def plugin_code_bbcode(markdown):
    markdown.block.register_rule("code_bbcode", CODE_BBCODE_PATTERN, parse_code_bbcode)
    markdown.block.rules.append("code_bbcode")

    if markdown.renderer.NAME == "ast":
        markdown.renderer.register("code_bbcode", render_ast_code_bbcode)
