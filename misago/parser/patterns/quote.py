from ..parser import Parser, Pattern


class QuoteMarkdown(Pattern):
    pattern_type: str = "quote"
    pattern: str = r"(\n|^) ? ? ?>.*(\n ? ? ?>.*)*"

    def parse(
        self, parser: Parser, match: str, parents: list[str]
    ) -> dict | list[dict]:
        content = clean_quote_markdown_content(match)

        if not content.strip():
            return []

        return {
            "type": self.pattern_type,
            "children": parser.parse_blocks(content, parents + [self.pattern_type]),
        }


def clean_quote_markdown_content(match: str) -> str:
    return "\n".join(line.lstrip()[1:] for line in match.splitlines())


class QuoteBBCodeOpen(Pattern):
    pattern_type: str = "quote-bbcode-open"
    pattern: str = r"\[quote(=.*?)?\]"

    def parse(self, parser: Parser, match: str, parents: list[str]) -> dict:
        args = parse_args(
            parser.reverse_reservations(match[6:-1].strip("\"' =")),
        )

        return {
            "type": self.pattern_type,
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
    pattern_type: str = "quote-bbcode-close"
    pattern: str = r"\[\/quote\]"

    def parse(self, parser: Parser, match: str, parents: list[str]) -> dict:
        return {"type": self.pattern_type}
