from markdown_it import MarkdownIt
from markdown_it.rules_inline.state_inline import StateInline
from markdown_it.token import Token

from ..args import parse_inline_bbcode_args


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
            token.content = content

    state.pos = end
    state.posMax = pos_max_org

    return True
