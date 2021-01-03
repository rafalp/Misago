from mistune import Markdown
from mistune.inline_parser import escape_url


SHORT_IMAGE_PATTERN = (
    r"!\(([A-Za-z][A-Za-z0-9+.-]{1,31}:"
    r"[^ <>]*?|[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9]"
    r"(?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*)\)"
)


def parse_short_image(parser, m, state: dict):
    link = m.group(1)
    return "image", escape_url(link), None, None


def plugin_short_image(markdown: Markdown):
    markdown.inline.register_rule("short_image", SHORT_IMAGE_PATTERN, parse_short_image)
    markdown.inline.rules.append("short_image")
