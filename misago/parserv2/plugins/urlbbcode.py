from markdown_it import MarkdownIt
from markdown_it.rules_inline.state_inline import StateInline


def url_bbcode_plugin(md: MarkdownIt):
    md.inline.ruler.push("url_bbcode", url_bbcode_rule)


def url_bbcode_rule(state: StateInline, silent: bool):
    return False
