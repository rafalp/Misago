import re

from markdown_it import MarkdownIt
from markdown_it.rules_block.state_block import StateBlock

from ..bbcode import BBCodeBlockRule, bbcode_block_end_rule, bbcode_block_start_rule


def quote_bbcode_plugin(md: MarkdownIt):
    md.block.ruler.before(
        "paragraph",
        "quote_bbcode",
        QuoteBBCodeBlockRule(
            name="quote_bbcode",
            element="misago-quote",
            start=quote_bbcode_start,
            end=quote_bbcode_end,
        ),
        {"alt": ["paragraph"]},
    )


class QuoteBBCodeBlockRule(BBCodeBlockRule):
    def get_meta(self, attrs: dict) -> dict | None:
        if attrs.get("post"):
            return {"post": attrs["post"]}

        return None


def quote_bbcode_start(
    state: StateBlock, line: int
) -> tuple[str, dict | None, int, int] | None:
    start = bbcode_block_start_rule("quote", state, line, args=True)
    if not start:
        return None

    markup, args_str, start, end = start

    if args_str:
        args = quote_bbcode_parse_args(args_str)
    else:
        args = None

    return markup, args, start, end


def quote_bbcode_parse_args(args_str: str) -> dict | None:
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


def quote_bbcode_end(state: StateBlock, line: int) -> tuple[str, int, int] | None:
    return bbcode_block_end_rule("quote", state, line)
