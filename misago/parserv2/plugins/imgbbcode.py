from markdown_it import MarkdownIt
from markdown_it.rules_inline.state_inline import StateInline
from markdown_it.token import Token


def img_bbcode_plugin(md: MarkdownIt):
    md.inline.ruler.push("img_bbcode", img_bbcode_rule)


def img_bbcode_rule(state: StateInline, silent: bool):
    start = state.pos
    maximum = state.posMax

    args_start = None
    args_end = None
    args_str = None

    content_start = None
    content_end = None

    if maximum - start < 11:
        return False

    if state.src[start : start + 4].lower() != "[img":
        return False

    if state.src[4] == "=":
        if "]" not in state.src[start + 5 : maximum]:
            return False

        args_start = start + 5
        content_start = state.src.index("]", args_start) + 1
        args_end = content_start - 1

        args_str = state.src[args_start:args_end].strip() or None
        if args_str and (
            (args_str[0] == '"' and args_str[-1] == '"')
            or (args_str[0] == "'" and args_str[-1] == "'")
        ):
            args_str = args_str[1:-1].strip()
    else:
        content_start = start + 5

    pos = content_start
    while pos + 6 <= maximum:
        if state.src[pos : pos + 6].lower() == "[/img]":
            break

        pos += 1

    if state.src[pos : pos + 6].lower() != "[/img]":
        return False

    content_end = pos
    end = content_end + 6

    content = state.src[content_start:content_end].strip()

    if args_start and args_end and not args_str:
        return False  # Eject if [img=]...[/img]

    if not content:
        return False  # Eject if [img][/img]

    if args_str:
        href = state.md.normalizeLink(args_str)
    else:
        href = state.md.normalizeLink(content.strip())

    if not state.md.validateLink(href):
        return False

    pos_max_org = state.posMax

    if not silent:
        token = state.push("image", "img", 0)
        token.markup = state.src[start:end]
        token.attrs = {"src": href, "alt": ""}

        if args_str and content:
            token.children = [
                Token(
                    type="text",
                    tag="",
                    nesting=0,
                    content=content,
                )
            ]

    state.pos = end
    state.posMax = pos_max_org

    return True
