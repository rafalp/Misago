from markdown_it import MarkdownIt
from markdown_it.rules_inline.state_inline import StateInline

FORMATTING_BBCODE = {
    "bold": "b",
    "italic": "i",
    "underline": "u",
    "strikethrough": "del",
}


def formatting_bbcode_plugin(md: MarkdownIt):
    for name, markup in FORMATTING_BBCODE.items():
        md.inline.ruler.push(
            name + "bbcode",
            get_formatting_bbcode_rule(name, markup),
        )


def get_formatting_bbcode_rule(name: str, markup: str):
    def formatting_bbcode_rule(state: StateInline, silent: bool):
        markup_open = f"[{name[0]}]"
        markup_close = f"[/{name[0]}]"

        start = state.pos
        maximum = state.posMax

        if maximum - start < 7:
            return False

        marker = state.src[start : start + 3]

        if silent:
            return False

        if marker.lower() != markup_open:
            return False

        pos = start + 3
        maximum = state.posMax
        nesting = 1

        while pos < maximum:
            if state.src[pos] == "\\":
                pos += 2

            elif state.src[pos : pos + 3].lower() == markup_open:
                nesting += 1
                pos += 1

            elif state.src[pos : pos + 4].lower() == markup_close:
                nesting -= 1
                if nesting == 0:
                    break
                pos += 1

            else:
                pos += 1

        if state.src[pos : pos + 4].lower() != markup_close:
            return False

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

    return formatting_bbcode_rule
