from markdown_it import MarkdownIt
from markdown_it.rules_inline.state_inline import StateInline

from ..args import parse_inline_bbcode_args


def url_bbcode_plugin(md: MarkdownIt):
    md.inline.ruler.before("link", "url_bbcode", url_bbcode_rule)


def url_bbcode_rule(state: StateInline, silent: bool):
    if state.linkLevel:
        return False

    start = state.pos
    maximum = state.posMax

    args_start = None
    args_end = None
    args_str = None

    content_start = None
    content_end = None

    if maximum - start < 11:
        return False

    if state.src[start : start + 4].lower() != "[url":
        return False

    parsed_args = parse_inline_bbcode_args(state, start + 4)
    if parsed_args:
        args_start = start + 5
        args_str, args_end = parsed_args
        content_start = args_end + 1
    elif parsed_args is False:
        return False
    else:
        content_start = start + 5

    pos = content_start
    while pos + 6 <= maximum:
        if state.src[pos : pos + 6].lower() == "[/url]":
            break

        pos += 1

    if state.src[pos : pos + 6].lower() != "[/url]":
        return False

    content_end = pos
    end = content_end + 6

    content = state.src[content_start:content_end]

    if args_start and args_end and not args_str:
        return False  # Eject if [url=]...[/url]

    if not content.strip():
        return False  # Eject if [url][/url]

    if args_str:
        href = state.md.normalizeLink(args_str)
    else:
        href = state.md.normalizeLink(content.strip())

    if not state.md.validateLink(href):
        return False

    pos_max_org = state.posMax

    if not silent:
        token = state.push("link_open", "a", 1)
        token.markup = state.src[start:content_start]
        token.attrs = {"href": href}

        if not args_str:
            token.info = "auto"

        if args_str:
            state.pos = content_start
            state.posMax = content_end
            state.linkLevel += 1
            state.md.inline.tokenize(state)
            state.linkLevel -= 1
        else:
            token = state.push("text", "", 0)
            token.content = state.md.normalizeLinkText(content)

        token = state.push("link_close", "a", -1)
        token.markup = "[/url]"

        if not args_str:
            token.info = "auto"

    state.pos = end
    state.posMax = pos_max_org

    return True
