from markdown_it import MarkdownIt
from markdown_it.rules_inline.state_inline import Delimiter, StateInline

SIMPLE_INLINE_BBCODE = (
    "bold",
    "italics",
    "underline",
)


def inline_bbcode_plugin(md: MarkdownIt):
    for bbcode_name in SIMPLE_INLINE_BBCODE:
        md.inline.ruler.push(
            bbcode_name + "bbcode",
            get_simple_inline_bbcode_rule(bbcode_name, bbcode_name[0]),
        )


def get_simple_inline_bbcode_rule(name: str, markup: str):
    def simple_inline_bbcode_rule(state: StateInline, silent: bool):
        markup_open = f"[{markup}]"
        markup_close = f"[/{markup}]"

        start = state.pos
        marker = state.src[start : start + 3]

        if silent:
            return False

        if marker.lower() != markup_open:
            return False

        pos = start + 3
        maximum = state.posMax

        while True:
            if pos >= maximum:
                return False

            if state.src[pos : pos + 4].lower() == markup_close:
                break

            pos += 1

        if not silent:
            state.pos = start + 3
            state.posMax = pos

            token = state.push(name + "_bbcode_open", markup, 1)
            token.markup = markup_open

            state.md.inline.tokenize(state)

            token = state.push(name + "_bbcode_close", markup, -1)
            token.markup = markup_close

        state.pos = pos + 4
        state.posMax = maximum
        return True

    return simple_inline_bbcode_rule
