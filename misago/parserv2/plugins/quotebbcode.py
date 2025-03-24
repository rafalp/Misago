from markdown_it import MarkdownIt
from markdown_it.rules_block.state_block import StateBlock

from ..bbcode import parse_nested_blocks


def quote_bbcode_plugin(md: MarkdownIt):
    md.block.ruler.before("paragraph", "quote_bbcode", quote_bbcode_rule)


def quote_bbcode_rule(state: StateBlock, startLine: int, endLine: int, silent: bool):
    if state.is_code_block(startLine):
        return False

    line = startLine

    start = state.bMarks[line] + state.tShift[line]
    maximum = state.eMarks[line]

    opening = quote_bbcode_open_rule(state.src[start:maximum])
    if not opening:
        return False

    markup, attrs = opening
    closing = None

    nesting = 1
    line += 1

    while line <= endLine:
        start = state.bMarks[line] + state.tShift[line]
        maximum = state.eMarks[line]
        src = state.src[start:maximum]

        if state.is_code_block(startLine):
            line += 1
            continue

        if quote_bbcode_open_rule(src):
            nesting += 1

        elif match := quote_bbcode_close_rule(src):
            nesting -= 1

            if nesting == 0:
                closing = match
                break

        line += 1

    if silent:
        return nesting == 0

    max_line = line + 1

    token = state.push("quote_bbcode_open", "misago-quote", 1)
    token.markup = markup
    token.map = [startLine, max_line]

    if attrs:
        for attr_name, attr_value in attrs.items():
            token.attrSet(attr_name, attr_value)

    parse_nested_blocks(state, "quote_bbcode", startLine, max_line)

    token = state.push("quote_bbcode_close", "misago-quote", -1)
    token.markup = closing

    state.line = max_line + 1
    return True


def quote_bbcode_open_rule(src: str) -> tuple[str, dict | None] | None:
    if not src.lower().startswith("[quote") or "]" not in src:
        return None

    end = src.index("]")
    if end > 6 and src[6] != "=":
        return None

    return src, quote_bbcode_parse_args(src[7:end])


def quote_bbcode_parse_args(args_str: str) -> dict | None:
    if not args_str:
        return None

    if args_str[0] == '"' and args_str[-1] == '"':
        args_str = args_str[1:-1]
    elif args_str[0] == "'" and args_str[-1] == "'":
        args_str = args_str[1:-1]

    if not args_str:
        return None

    return {"info": args_str}


def quote_bbcode_close_rule(src: str) -> str | None:
    if src.lower().startswith("[/quote]"):
        return src

    return None
