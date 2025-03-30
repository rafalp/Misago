from markdown_it import MarkdownIt
from markdown_it.rules_inline.state_inline import StateInline


def img_bbcode_plugin(md: MarkdownIt):
    md.inline.ruler.push("img_bbcode", img_bbcode_rule)


def img_bbcode_rule(state: StateInline, silent: bool):
    return False
