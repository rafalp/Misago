from markdown_it import MarkdownIt
from markdown_it.rules_block.state_block import StateBlock

from ..bbcode import BBCodeBlockRule, bbcode_block_end_rule, bbcode_block_start_rule


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
    start = bbcode_block_start_rule("spoiler", state, line, args=True)
    if not start:
        return None

    markup, args_str, start, end = start

    if args_str:
        args = {"info": args_str}
    else:
        args = None

    return markup, args, start, end


def spoiler_bbcode_end(state: StateBlock, line: int) -> tuple[str, int, int] | None:
    return bbcode_block_end_rule("spoiler", state, line)
