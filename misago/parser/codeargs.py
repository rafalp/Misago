import re

from markdown_it.common.utils import unescapeAll

from .pygments import PYGMENTS_LANGUAGES


CODE_ARGS = re.compile(r"^(?P<info>.+)[;,] *syntax[:=] *(?P<syntax>.+) *$")


def parse_code_args(args_str: str) -> dict | None:
    if args_str.lower().startswith("syntax:") or args_str.lower().startswith("syntax="):
        syntax = unescapeAll(args_str[7:].strip())
        if not syntax:
            return None
        return {"syntax": syntax.lower()}

    if match := CODE_ARGS.match(args_str):
        args = {}

        if info := match.group("info").strip():
            args["info"] = unescapeAll(info)
        if syntax := match.group("syntax").strip():
            args["syntax"] = unescapeAll(syntax)

        return args if args else None

    if args_str.lower() in PYGMENTS_LANGUAGES:
        return {"syntax": args_str.lower()}

    if args_str:
        return {"info": unescapeAll(args_str)}

    return None
