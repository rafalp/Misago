import re

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

    if args := parse_user_post_args(args_str):
        return args

    return {"info": args_str}


USER_POST = re.compile(r"^(?P<user>[a-zA-Z0-9]+) *[;,] *post: *(?P<post>[0-9]+) *$")


def parse_user_post_args(args: str) -> dict | None:
    match = USER_POST.match(args)
    if not match:
        return None

    user = match.group("user")
    post = match.group("post")

    try:
        post = int(post)
        if post < 1:
            return None
    except (TypeError, ValueError):
        return None

    if user and post:
        return {"user": user, "post": post}

    return None


def quote_bbcode_end(src: str) -> str | None:
    if src.lower().startswith("[/quote]"):
        return src

    return None
