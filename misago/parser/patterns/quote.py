import re

from ..parser import Parser, Pattern


class QuoteMarkdown(Pattern):
    pattern_type: str = "quote"
    pattern: str = r"(^|\n) {0,3}>.*(\n{0,3}>.*)*"

    def parse(
        self, parser: Parser, match: str, parents: list[str]
    ) -> dict | list[dict]:
        content = self.strip_quote_prefix(match)
        if not content.strip():
            return []

        return {
            "type": self.pattern_type,
            "children": parser.parse_blocks(content, parents + [self.pattern_type]),
        }

    def strip_quote_prefix(self, match: str) -> str:
        return "\n".join(line.lstrip()[1:] for line in match.splitlines())


class QuoteBBCodeOpen(Pattern):
    pattern_type: str = "quote-bbcode-open"
    pattern: str = r"\[quote(=.*?)?\]"
    user_post_pattern = re.compile(
        r"^(?P<user>[a-zA-Z0-9]+) *[;,] +post: *(?P<post>[0-9]+) *$"
    )

    def parse(self, parser: Parser, match: str, parents: list[str]) -> dict:
        match = match[6:-1]
        if match and match[0] == "=":
            match = match[1:]

        match = match.strip("\"' ")
        if args := self.parse_user_post_args(parser, match):
            return {
                "type": self.pattern_type,
                "user": parser.unescape(args["user"]) or None,
                "post": parser.unescape(args["post"]) or None,
                "info": None,
            }

        if info := match.strip():
            return {
                "type": self.pattern_type,
                "user": None,
                "post": None,
                "info": parser.parse_inline(info, parents + ["quote-info"]) or [],
            }

        return {
            "type": self.pattern_type,
            "user": None,
            "post": None,
            "info": None,
        }

    def parse_user_post_args(self, parser: Parser, args: str) -> dict | None:
        match = self.user_post_pattern.match(args)
        if not match:
            return None

        user = parser.unescape(match.group("user"))
        post = match.group("post")

        try:
            post = int(post)
            if post < 1:
                return None
        except (TypeError, ValueError):
            return None

        return {"user": user, "post": post}


def parse_args(args: str) -> dict:
    if "post:" not in args:
        return {"user": args or None, "post": None}

    data = {"user": None, "post": None}
    post_pos = args.rfind("post:")
    data["user"] = args[:post_pos].rstrip("; ") or None
    try:
        post_id = int(args[post_pos + 5 :].strip())
        if post_id > 0:
            data["post"] = post_id
    except (TypeError, ValueError):
        pass

    return data


class QuoteBBCodeClose(Pattern):
    pattern_type: str = "quote-bbcode-close"
    pattern: str = r"\[\/quote\]"

    def parse(self, parser: Parser, match: str, parents: list[str]) -> dict:
        return {"type": self.pattern_type}
