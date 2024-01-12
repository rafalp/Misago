import re
from textwrap import dedent

from ..parser import Parser, Pattern


class QuoteBBCodeOpen(Pattern):
    pattern: str = r"\[quote(=.*?)?\]"

    def parse(self, parser: Parser, match: str) -> dict:
        args = parse_args(match[6:-1].strip("\"' ="))

        return {
            "type": "quote-bbcode-open",
            "author": args["author"],
            "post": args["post"],
        }


def parse_args(args: str) -> dict:
    if "post:" not in args:
        return {"author": args or None, "post": None}

    data = {"author": None, "post": None}
    post_pos = args.rfind("post:")
    data["author"] = args[:post_pos].rstrip("; ") or None
    try:
        post_id = int(args[post_pos + 5 :].strip())
        if post_id > 0:
            data["post"] = post_id
    except (TypeError, ValueError):
        pass

    return data


class QuoteBBCodeClose(Pattern):
    pattern: str = r"\[\/quote\]"

    def parse(self, parser: Parser, match: str) -> dict:
        return {
            "type": "quote-bbcode-close",
        }
