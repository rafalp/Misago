import re
from functools import cached_property

from django.utils.crypto import get_random_string

from ..parents import has_invalid_parent
from ..parser import Parser, Pattern

MAIL_RE = re.compile(r"^\w+[.-_+\w]*@[-\w]+(.\w+)+$")
URL_RE = re.compile(
    r"^(((https?)|(ftps?))://)?\w+(([-_\w])?\w+)*(\.\w+(([-_\w])?\w+))+[^\s]*$"
)


def clean_url(value: str) -> str | None:
    value = value.strip()
    if not value:
        return None

    if MAIL_RE.match(value):
        return f"mailto:{value}"

    if URL_RE.match(value):
        return value

    return None


BBCODE_CONTENTS = re.compile(
    r"\[[a-z]+(=(?P<arg>(.+)))?\](?P<content>((.|\n)*?))\[\/[a-z]+\]", re.IGNORECASE
)


class UrlBBCode(Pattern):
    pattern_type: str = "url-bbcode"
    pattern: str = r"((\[url=.+?\](.|\n)*?)|(\[url\].*?))\[\/url\]"
    invalid_parents: set[str] = {pattern_type, "url"}

    def parse(self, parser: Parser, match: str, parents: list[dict]) -> dict:
        contents = BBCODE_CONTENTS.match(match[1:-1]).groupdict()
        raise Exception(contents)
        arg = contents["arg"].strip(" \"'") if contents.get("arg") else None
        content = contents["content"]

        if arg:
            url = clean_url(arg)
        else:
            content = clean_url(content)

        if not url or has_invalid_parent(self.invalid_parents, parents):
            return {"type": "text", "text": match}

        return {"type": self.pattern_type, "href": url}


class ImgBBCode(UrlBBCode):
    pattern_type: str = "image-bbcode"
    pattern: str = r"((\[img=.+?\](.|\n)*?)|(\[img\].*?))\[\/img\]"
    invalid_parents: set[str] = {pattern_type, "image"}


INLINE_CODE_PATTERN = r"`(.|\n)*?`"

IMAGE_PATTERN = r"!(\[(.|\n)*?\])?\(.*?\)"
IMAGE_RE = re.compile(IMAGE_PATTERN)
URL_START_RE = re.compile(r"\[(.|\n)*?\]\(")


class UrlMarkdown(Pattern):
    pattern_type: str = "url"
    pattern: str = r"(?<!\!)\[.*\]\(.*\)"
    exclude_patterns: list[str] = [INLINE_CODE_PATTERN, IMAGE_PATTERN]

    def parse(self, parser: Parser, match: str, parents: list[dict]) -> list[dict]:
        clean_match, reserved_patterns = self.prepare_match_str(match)
        return self.parse_clean_match(parser, clean_match, reserved_patterns, parents)

    def parse_clean_match(
        self,
        parser: Parser,
        clean_match: str,
        reserved_patterns: dict[str, str],
        parents: list[dict],
    ) -> list[dict]:
        ast: list[dict] = []
        cursor = 0

        urls_starts = list(URL_START_RE.finditer(clean_match))
        urls_starts_last = len(urls_starts) - 1
        for i, m in enumerate(urls_starts):
            if m.start() > cursor:
                ast += parser.parse_inline(clean_match[cursor : m.start()], parents)

            text = m.group(0)[1:-2]
            if reserved_patterns:
                text = self.reverse_link_text(text, reserved_patterns)

            url_source_start = m.end() - 1
            if i < urls_starts_last:
                next_url_start = urls_starts[i + 1].start()
                url_source = clean_match[url_source_start:next_url_start]
            else:
                url_source = clean_match[url_source_start:]

            url, end = self.extract_url_from_source(url_source)
            cursor = m.end() - 1 + end

            ast.append(self.make_link_ast(parser, text, url, parents))

        if cursor < len(clean_match):
            ast += parser.parse_inline(clean_match[cursor:], parents)

        return ast

    def prepare_match_str(self, match: str) -> tuple[str, dict[str, str]]:
        clean_match: str = ""
        reserved_patterns = {}

        cursor = 0
        for m in self._exclude_patterns_re.finditer(match):
            if m.start() > cursor:
                clean_match += match[cursor : m.start()]

            pattern_id = f"%%{get_random_string(8)}%%"
            clean_match += pattern_id
            reserved_patterns[pattern_id] = m.group(0)
            cursor = m.end()

        if cursor < len(match):
            clean_match += match[cursor:]

        return clean_match, reserved_patterns

    def reverse_link_text(self, text: str, reserved_patterns: dict) -> str:
        for token, value in reserved_patterns.items():
            text = text.replace(token, value)
        return text

    def extract_url_from_source(self, source: str) -> tuple[str, int]:
        opening = source.count("(")
        closing = source.count(")")

        # Simplest case, one opening parenthesis matched by one closing
        if opening == closing and opening == 1:
            url = source[1 : source.find(")")].strip()
            return url, source.find(")") + 1

        # Walk the string to find pairs of parentheses
        nesting = 0
        length = 0
        for i, c in enumerate(source):
            if c == "(":
                nesting += 1
            elif c == ")":
                nesting -= 1
                if nesting >= 0:
                    length = i

        url = source[1:length].strip()
        return url, length + 1

    def make_link_ast(
        self, parser: Parser, text: str, url: str, parents: list[dict]
    ) -> dict:
        return {
            "type": self.pattern_type,
            "href": url,
            "children": parser.parse_inline(text, parents + [self.pattern_type]),
        }

    @cached_property
    def _exclude_patterns_re(self) -> re.Pattern:
        return re.compile("|".join(f"({p})" for p in self.exclude_patterns))


IMAGE_CONTENTS = re.compile(r"!(\[(?P<alt>(.|\n)*?)\])?\((?P<src>.*?)\)")


class ImgMarkdown(Pattern):
    pattern_type: str = "image"
    pattern: str = IMAGE_PATTERN

    def parse(self, parser: Parser, match: str, parents: list[dict]) -> list[dict]:
        contents = IMAGE_CONTENTS.match(match).groupdict()

        if contents["alt"]:
            alt = contents["alt"].strip() or None
        else:
            alt = None

        src = contents["src"].strip()
        if URL_RE.match(src):
            return {
                "type": "image",
                "alt": alt,
                "src": src,
            }

        return match


class AutolinkMarkdown(Pattern):
    pattern_type: str = "autolink"
    pattern: str = r"\<!?[^\s]*?\>"
    invalid_parents: set[str] = {UrlMarkdown.pattern_type, UrlBBCode.pattern_type}

    def parse(self, parser: Parser, match: str, parents: list[dict]) -> dict:
        url = match[1:-1]
        if url and url[0] == "!":
            url = url[1:]
            is_image = True
        else:
            is_image = False

        url = clean_url(url)

        if not url or has_invalid_parent(self.invalid_parents, parents):
            return {"type": "text", "text": match}

        return {"type": self.pattern_type, "href": url}


class AutoUrl(AutolinkMarkdown):
    pattern: str = r"(?<!\w)(https?://(www\.)?)|(www\.))\w+(-|\w)*(\.\w+(-|\w)*)+[^\s]*"

    def parse(self, parser: Parser, match: str, parents: list[dict]) -> dict:
        url = clean_url(match)
        if not url or has_invalid_parent(self.invalid_parents, parents):
            return {"type": "text", "text": match}

        return {"type": self.pattern_type, "href": url}
