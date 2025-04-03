import re

from .pygments import PYGMENTS_LANGUAGES


CODE_ARGS = re.compile(r"^(?P<info>.+)[;,] *syntax[:=] *(?P<syntax>.+) *$")


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
