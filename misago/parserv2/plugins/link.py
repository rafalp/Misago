from markdown_it import MarkdownIt
from markdown_it.rules_inline.link import link
from markdown_it.rules_inline.state_inline import StateInline


def link_plugin(md: MarkdownIt):
    md.inline.ruler.at("link", link_rule)


def link_rule(state: StateInline, silent: bool):
    if state.linkLevel:
        return False

    return link(state, silent)
