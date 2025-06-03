import re

from markdown_it import MarkdownIt
from markdown_it.common.utils import unescapeAll

from ..bbcode import BBCodeBlockRule


def quote_bbcode_plugin(md: MarkdownIt):
    md.block.ruler.before(
        "paragraph",
        "quote_bbcode",
        QuoteBBCodeBlockRule(
            name="quote_bbcode",
            bbcode="quote",
            element="misago-quote",
            args_parser=quote_bbcode_parse_args,
        ),
        {"alt": ["paragraph"]},
    )


class QuoteBBCodeBlockRule(BBCodeBlockRule):
    def get_meta(self, attrs: dict) -> dict | None:
        if attrs.get("post"):
            return {"post": attrs["post"]}

        return None


def quote_bbcode_parse_args(args_str: str) -> dict | None:
    if args := parse_user_post_args(args_str):
        return args

    return {"info": unescapeAll(args_str)}


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
