from mistune import Markdown
from mistune.inline_parser import escape_url


URL_BBCODE_PATTERN = r"\[url(=(\"|')?(.*)(\"|')?)?\](.*)\[\/url\]"


def parse_url_bbcode(parser, m, state: dict):
    if state.get("_in_link"):
        return "text", m.group(0)

    url_attr = m.group(3)
    url_or_text = m.group(5)

    if url_attr:
        url = escape_url(url_attr)
        state["_in_link"] = True
        text = parser(url_or_text, state)
        state["_in_link"] = False
    else:
        url = escape_url(url_or_text)
        text = url_or_text

    return "link", url, text, None


def plugin_url_bbcode(markdown: Markdown):
    markdown.inline.register_rule("url_bbcode", URL_BBCODE_PATTERN, parse_url_bbcode)
    markdown.inline.rules.append("url_bbcode")
