from markdown_it import MarkdownIt
from markdown_it.rules_inline.state_inline import StateInline


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

    if state.src[4] == "=":
        if "]" not in state.src[start + 5 : maximum]:
            return False

        args_start = start + 5
        content_start = state.src.index("]", args_start) + 1
        args_end = content_start - 1

        args_str = state.src[args_start:args_end].strip() or None
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

    if args_start and args_end and args_start == args_end:
        return False  # Eject if [url=]...[/url]

    if content_start and content_end and content_start == content_end:
        return False  # Eject if [url][/url]

    if args_str:
        res = state.md.helpers.parseLinkDestination(state.src, args_start, args_end)
    else:
        res = state.md.helpers.parseLinkDestination(
            state.src, content_start, content_end
        )

    if not res.ok:
        return False

    href = state.md.normalizeLink(res.str)

    if not state.md.validateLink(href):
        return False

    pos_max_org = state.posMax

    if not silent:
        token = state.push("link_open", "a", 1)
        token.markup = state.src[start:content_start]
        token.attrs = {"href": href}

        if args_str:
            state.pos = content_start
            state.posMax = content_end
            state.linkLevel += 1
            state.md.inline.tokenize(state)
            state.linkLevel -= 1
        else:
            token = state.push("text", "", 0)
            token.content = state.md.normalizeLinkText(
                state.src[content_start:content_end]
            )

        state.linkLevel -= 1

        token = state.push("link_close", "a", -1)
        token.markup = "[/url]"

    state.pos = end
    state.posMax = pos_max_org

    return True
