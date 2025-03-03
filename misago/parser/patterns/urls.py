import re
from functools import cached_property

from ..parents import has_invalid_parent
from ..parser import Parser, Pattern

MAIL_RE = re.compile(r"^\w+[.-_+\w]*@[-\w]+(.\w+)+$")
URL_RE = re.compile(
    r"^(((https?)|(ftps?)|(wss?)):\/\/)?"  # http/ftp/ws(s) prefix
    r"("  # start hostnames
    r"(localhost)"  # localhost
    r"|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})"  # IP address
    r"|((\w+([-_]\w+)*\.)+[a-z]+)"  # Other hostname
    r")"  # end hostnames
    r"(:[1-9][0-9]*)?"
    r"(\/+[^\s\|]*)?$"
)


def clean_url(value: str) -> str | None:
    value = value.strip()
    if not value:
        return None

    if MAIL_RE.match(value):
        return f"mailto:{value}"

    if URL_RE.match(value):
        return value

    if value.startswith("/"):
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
        contents = BBCODE_CONTENTS.match(match).groupdict()

        arg = (
            parser.unescape(contents["arg"].strip(" \"'")) if contents["arg"] else None
        )
        content = parser.unescape(contents["content"])

        if arg:
            url = clean_url(arg)
        elif content:
            url = clean_url(content.strip())
            content = None
        else:
            url = None

        if (
            not url
            or not contents["content"].strip()
            or has_invalid_parent(self.invalid_parents, parents)
        ):
            return parser.text_ast(match)

        return self.make_ast(parser, match, url, content, parents)

    def make_ast(
        self,
        parser: Parser,
        match: str,
        url: str | None,
        content: str,
        parents: list[dict],
    ) -> dict:
        if content:
            children = parser.parse_inline(content, parents + [self.pattern_type])
        else:
            children = []

        return {
            "type": self.pattern_type,
            "href": url,
            "children": children,
        }


class ImgBBCode(UrlBBCode):
    pattern_type: str = "image-bbcode"
    pattern: str = r"((\[img=.+?\](.|\n)*?)|(\[img\].*?))\[\/img\]"
    invalid_parents: set[str] = {pattern_type, "image"}

    def make_ast(
        self,
        parser: Parser,
        match: str,
        url: str | None,
        alt_text: str | None,
        parents: list[dict],
    ) -> dict:
        if url.startswith("mailto:"):
            return parser.text_ast(match)

        if alt_text:
            alt_text = parser.unescape(alt_text.strip())

        return {
            "type": self.pattern_type,
            "alt": alt_text or None,
            "src": url,
        }


INLINE_CODE_PATTERN = r"(?<!\\)`(.|\n)*?(?<!\\)`"

IMAGE_PATTERN = r"!(\[(.|\n)*?\])?\(.*?\)"
IMAGE_RE = re.compile(IMAGE_PATTERN)
URL_START_RE = re.compile(r"\[(.|\n)*?\]\(")


class UrlMarkdown(Pattern):
    pattern_type: str = "url"
    pattern: str = r"(?<!\!)\[.*\]\(.*\)"
    exclude_patterns: list[str] = [INLINE_CODE_PATTERN, IMAGE_PATTERN]

    def parse(self, parser: Parser, match: str, parents: list[dict]) -> list[dict]:
        clean_match, placeholders = self.prepare_match_str(parser, match)
        return self.parse_clean_match(parser, clean_match, placeholders, parents)

    def prepare_match_str(
        self, parser: Parser, match: str
    ) -> tuple[str, dict[str, str]]:
        clean_match: str = ""
        placeholders = {}

        cursor = 0
        for m in self._exclude_patterns_re.finditer(match):
            if m.start() > cursor:
                clean_match += match[cursor : m.start()]

            placeholder = parser.get_unique_placeholder(match)
            clean_match += placeholder
            placeholders[placeholder] = m.group(0)
            cursor = m.end()

        if cursor < len(match):
            clean_match += match[cursor:]

        return clean_match, placeholders

    def parse_clean_match(
        self,
        parser: Parser,
        clean_match: str,
        placeholders: dict[str, str],
        parents: list[dict],
    ) -> list[dict]:
        ast: list[dict] = []
        cursor = 0

        urls_starts = list(URL_START_RE.finditer(clean_match))
        urls_starts_last = len(urls_starts) - 1
        for i, m in enumerate(urls_starts):
            if m.start() > cursor:
                markup = clean_match[cursor : m.start()]
                if placeholders:
                    markup = self.reverse_placeholders(markup, placeholders)
                ast += parser.parse_inline(markup, parents)

            text = m.group(0)[1:-2]
            if placeholders:
                text = self.reverse_placeholders(text, placeholders)

            url_source_start = m.end() - 1
            if i < urls_starts_last:
                next_url_start = urls_starts[i + 1].start()
                url_source = clean_match[url_source_start:next_url_start]
            else:
                url_source = clean_match[url_source_start:]

            title = None
            url, end = self.extract_url_from_source(url_source)

            if url:
                url, title = self.split_url_and_title(url)
                url = clean_url(parser.unescape(url))

            if text and url:
                ast.append(
                    {
                        "type": self.pattern_type,
                        "href": url,
                        "title": parser.unescape(title) or None,
                        "children": parser.parse_inline(
                            text, parents + [self.pattern_type]
                        ),
                    }
                )
                cursor = m.end() - 1 + end

            else:
                markup = self.reverse_placeholders(m.group(0), placeholders)
                for ast_node in parser.parse_inline(markup, parents):
                    if ast_node["type"] == "text" and ast and ast[-1]["type"] == "text":
                        ast[-1]["text"] += ast_node["text"]
                    else:
                        ast.append(ast_node)

                cursor = m.end()

        if cursor < len(clean_match):
            markup = clean_match[cursor:]
            if placeholders:
                markup = self.reverse_placeholders(markup, placeholders)
            ast += parser.parse_inline(markup, parents)

        return ast

    def reverse_placeholders(self, text: str, placeholders: dict) -> str:
        for placeholder, value in placeholders.items():
            text = text.replace(placeholder, value)
        return text

    def extract_url_from_source(self, source: str) -> tuple[str, int]:
        opening = source.count("(")
        closing = source.count(")")

        # Simplest case, one opening parenthesis matched by one closing
        if opening == closing and opening == 1:
            url = source[1 : source.find(")")].strip()
            return url, source.find(")") + 1

        if not closing:
            return "", 0

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
                if nesting == 0:
                    break

        url = source[1:length].strip()
        return url, length + 1

    def split_url_and_title(self, value: str) -> tuple[str | None, str | None]:
        if ' "' not in value:
            return value, None

        url, title = [v.strip() for v in value.split('"', 1)]
        return url or None, title.strip('" ') or None

    @cached_property
    def _exclude_patterns_re(self) -> re.Pattern:
        return re.compile("|".join(f"({p})" for p in self.exclude_patterns))


IMAGE_CONTENTS = re.compile(
    r"!(\[(?P<alt>(.|\n)*?)\])?\((?P<src>.*?)(?P<title>\s*\".*?\"\s*?)?\)"
)


class ImgMarkdown(Pattern):
    pattern_type: str = "image"
    pattern: str = IMAGE_PATTERN

    def parse(self, parser: Parser, match: str, parents: list[dict]) -> list[dict]:
        contents = IMAGE_CONTENTS.match(match).groupdict()

        if contents["alt"]:
            alt = parser.unescape(contents["alt"].strip()) or None
        else:
            alt = None

        if contents["title"]:
            title = parser.unescape(contents["title"].strip('" ')) or None
        else:
            title = None

        src = parser.unescape(contents["src"]).strip()
        if src.startswith("/") or URL_RE.match(src):
            return {
                "type": "image",
                "alt": alt,
                "title": title,
                "src": src,
            }

        return parser.text_ast(match)


class AutolinkMarkdown(Pattern):
    pattern_type: str = "auto-link"
    pattern: str = r"\<!?[^\s]+?\>"
    invalid_parents: set[str] = {UrlMarkdown.pattern_type, UrlBBCode.pattern_type}

    def parse(self, parser: Parser, match: str, parents: list[dict]) -> dict:
        url = match[1:-1]
        if url and url[0] == "!":
            url = url[1:]
            is_image = True
        else:
            is_image = False

        url = clean_url(parser.unescape(url))

        if (
            not url
            or (is_image and url.startswith("mailto:"))
            or has_invalid_parent(self.invalid_parents, parents)
        ):
            return parser.text_ast(match)

        return {"type": self.pattern_type, "image": is_image, "href": url}


class AutoUrl(AutolinkMarkdown):
    pattern_type: str = "auto-url"
    pattern: str = (
        r"(?<!\w)"
        r"(((https?)|(ftps?)|(wss?)):\/\/)?"  # http/ftp/ws(s) prefix
        r"("  # start hostnames
        r"("  # start ther hostname
        r"(\w+((-|_)\w+)*\w+\.)+"  # word-word.
        r"((com)|(gov)|(net)|(org)|(info)|(edu)|(io)|(cn)|(hk)|(in)|(us)|(id)|(pk)|(ng)|(br)|(bd)|(ru)|(mx)|(ja)|(ph)|(tr)|(ca)|(uk)|(ie)|(de)|(fr)|(es)|(pt)|(it)|(pl)|(cz)|(sk)|(hu)|(se)|(no)|(is)|(fi))(\.[a-z]{2})?"
        r")"  # end other hostname
        r"|(localhost)"  # localhost
        r"|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})"  # IP address
        r")"  # end hostnames
        r"(:[1-9][0-9]*)?"
        r"(\/+[^\s\|]*)?"
    )

    def parse(self, parser: Parser, match: str, parents: list[dict]) -> dict:
        url = clean_url(parser.unescape(match))
        if not url or has_invalid_parent(self.invalid_parents, parents):
            return parser.text_ast(match)

        return {"type": self.pattern_type, "href": url}
