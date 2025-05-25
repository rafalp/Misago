import re

from markdown_it.rules_inline.state_inline import StateInline

from .escape import unescape
from .pygments import PYGMENTS_LANGUAGES


CODE_ARGS = re.compile(r"^(?P<info>.+)[;,] *syntax[:=] *(?P<syntax>.+) *$")


def parse_inline_bbcode_args(
    state: StateInline, start: int
) -> tuple[str, int] | bool | None:
    if state.src[start] == "]":
        return None
    if state.src[start] != "=":
        return False

    args_start = start + 1
    args_end = None

    pos = args_start
    level = 1

    while pos < state.posMax:
        if state.src[pos] == "\\":
            pos += 2
        else:
            if state.src[pos] == "]":
                level -= 1
                if not level:
                    args_end = pos
                    break
            elif state.src[pos] == "[":
                level += 1

            pos += 1
    else:
        return False

    args_str = state.src[args_start:args_end].strip()
    if args_str and (
        (args_str[0] == '"' and args_str[-1] == '"')
        or (args_str[0] == "'" and args_str[-1] == "'")
    ):
        args_str = args_str[1:-1].strip()

    args_str = unescape(args_str)

    return args_str or None, args_end


def parse_code_args(args_str: str) -> dict | None:
    if args_str.startswith("syntax:") or args_str.startswith("syntax="):
        syntax = args_str[7:].strip()
        if not syntax:
            return None
        return {"syntax": syntax.lower()}

    if match := CODE_ARGS.match(args_str):
        args = {}

        if info := match.group("info").strip():
            args["info"] = info
        if syntax := match.group("syntax").strip():
            args["syntax"] = syntax

        return args if args else None

    if args_str.lower() in PYGMENTS_LANGUAGES:
        return {"syntax": args_str.lower()}

    if args_str:
        return {"info": args_str}

    return None
