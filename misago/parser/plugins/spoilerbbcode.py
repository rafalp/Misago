from markdown_it import MarkdownIt
from markdown_it.common.utils import unescapeAll

from ..bbcode import BBCodeBlockRule


def spoiler_bbcode_plugin(md: MarkdownIt):
    md.block.ruler.before(
        "paragraph",
        "spoiler_bbcode",
        BBCodeBlockRule(
            name="spoiler_bbcode",
            bbcode="spoiler",
            element="misago-spoiler",
            args_parser=spoiler_bbcode_parse_args,
        ),
        {"alt": ["paragraph"]},
    )


def spoiler_bbcode_parse_args(args_str: str) -> dict:
    return {"info": unescapeAll(args_str)}
