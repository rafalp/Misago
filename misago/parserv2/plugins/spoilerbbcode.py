import re

from markdown_it import MarkdownIt
from markdown_it.rules_block.state_block import StateBlock

from ..bbcode import BBCodeBlockRule


def spoiler_bbcode_plugin(md: MarkdownIt):
    md.block.ruler.before(
        "paragraph",
        "spoiler_bbcode",
        BBCodeBlockRule(
            name="spoiler_bbcode",
            element="misago-spoiler",
            start=spoiler_bbcode_start,
            end=spoiler_bbcode_end,
        ),
        {"alt": ["paragraph"]},
    )


def spoiler_bbcode_start(
    state: StateBlock, line: int
) -> tuple[str, dict | None, int, int] | None:
    start = state.bMarks[line] + state.tShift[line]
    maximum = state.eMarks[line]
    src = state.src[start:maximum]

    if src.lower()[:8] != "[spoiler":
        return None

    if "]" not in src[8:]:
        return None

    end = src.index("]", 0, maximum - start)
    if end == 8:
        return src[:9], None, start, start + end + 1

    if end and src[8] != "=":
        return None

    return src[: end + 1], spoiler_bbcode_parse_args(src[9:end]), start, end + 1


def spoiler_bbcode_parse_args(args_str: str) -> dict | None:
    if not args_str:
        return None

    if args_str[0] == '"' and args_str[-1] == '"':
        args_str = args_str[1:-1]
    elif args_str[0] == "'" and args_str[-1] == "'":
        args_str = args_str[1:-1]

    args_str = args_str.strip()

    if not args_str:
        return None

    return {"info": args_str}


def spoiler_bbcode_end(state: StateBlock, line: int) -> tuple[str, int, int] | None:
    start = state.bMarks[line] + state.tShift[line]
    maximum = state.eMarks[line]
    src = state.src[start:maximum]

    if src[:10].lower() == "[/spoiler]":
        return src[:10], start, start + 10

    return None
