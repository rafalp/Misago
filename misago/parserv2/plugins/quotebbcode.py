from markdown_it import MarkdownIt
from markdown_it.rules_block.state_block import StateBlock

from ..bbcode import BBCodeBlockRule


def quote_bbcode_plugin(md: MarkdownIt):
    md.block.ruler.before(
        "paragraph",
        "quote_bbcode",
        BBCodeBlockRule(
            name="quote_bbcode",
            element="misago-quote",
            start=quote_bbcode_start,
            end=quote_bbcode_end,
        ),
    )


def quote_bbcode_start(src: str) -> tuple[str, dict | None] | None:
    if not src.lower().startswith("[quote") or "]" not in src:
        return None

    end = src.index("]")
    if end > 6 and src[6] != "=":
        return None

    return src, quote_bbcode_parse_args(src[7:end])


def quote_bbcode_parse_args(args_str: str) -> dict | None:
    if not args_str:
        return None

    if args_str[0] == '"' and args_str[-1] == '"':
        args_str = args_str[1:-1]
    elif args_str[0] == "'" and args_str[-1] == "'":
        args_str = args_str[1:-1]

    if not args_str:
        return None

    return {"info": args_str}


def quote_bbcode_end(src: str) -> str | None:
    if src.lower().startswith("[/quote]"):
        return src

    return None
