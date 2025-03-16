from markdown_it import MarkdownIt
from markdown_it.rules_block.state_block import StateBlock
from markdown_it.token import Token

from ...core.utils import slugify


def attachment_plugin(md: MarkdownIt):
    md.block.ruler.before(
        "table", "attachment", attachment_rule, {"alt": ["paragraph", "blockquote"]}
    )


def attachment_rule(state: StateBlock, startLine: int, endLine: int, silent: bool):
    if state.is_code_block(startLine):
        return False

    start = state.bMarks[startLine] + state.tShift[startLine]
    maximum = state.eMarks[startLine]

    args_start = start + 12
    if state.src[start:args_start].lower() != "<attachment=":
        return False

    pos = args_start
    while True:
        if pos >= maximum:
            return False

        if state.src[pos] == ">":
            break

        pos += 1

    args = parse_args(state.src[args_start:pos])
    if not args:
        return False

    if silent:
        return True

    state.line = startLine + 1

    token = state.push("attachment", "misago-attachment", 0)
    for attr_name, attr_value in args.items():
        token.attrSet(attr_name, attr_value)

    token.map = [startLine, state.line]
    token.markup = state.src[start : pos + 1]

    return True


def parse_args(args_str: str) -> dict | None:
    args_str = args_str.strip()

    if not args_str:
        return None

    if (args_str[0] == "'" and args_str[-1] == "'") or (
        args_str[0] == '"' and args_str[-1] == '"'
    ):
        args_str = args_str[1:-1].strip()

    if ":" not in args_str:
        return None

    name, id_ = [v.strip() for v in args_str.rsplit(":", 1)]

    try:
        id_ = int(id_)
    except (TypeError, ValueError):
        return None

    if name and id_ > 0:
        return {"name": name, "slug": slugify(name), "id": id_}

    return None
