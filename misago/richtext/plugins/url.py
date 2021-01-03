from mistune import Markdown
from mistune.plugins import extra


def parse_url_link(parser, m, state: dict):
    if state.get("_in_link"):
        return "text", m.group(0)

    return extra.parse_url_link(parser, m, state)


def plugin_url(markdown: Markdown):
    markdown.inline.register_rule("url_link", extra.URL_LINK_PATTERN, parse_url_link)
    markdown.inline.rules.append("url_link")
