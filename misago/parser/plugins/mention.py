import re

from markdown_it import MarkdownIt
from markdown_it.rules_inline.state_inline import StateInline

from ...core.utils import slugify


def mention_plugin(md: MarkdownIt):
    md.inline.ruler.push("mention", mention_rule)


MENTION = re.compile(r"^\@[A-Za-z0-9-_]+")


def mention_rule(state: StateInline, silent: bool):
    if state.linkLevel:
        return False

    start = state.pos
    if state.src[start] != "@":
        return False

    if start and state.src[start - 1].isalnum():
        return False

    match = MENTION.match(state.src[start:])
    if not match:
        return False

    markup = match.group(0)
    state.pos += len(markup)

    if silent:
        return True

    token = state.push("mention", "misago-mention", 0)
    token.attrSet("username", markup[1:])
    token.markup = markup
    token.meta = {"slug": slugify(markup[1:])}

    return True
