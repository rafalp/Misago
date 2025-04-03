from markdown_it import MarkdownIt
from markdown_it.rules_inline.state_inline import StateInline

from ...core.utils import slugify


def attachment_plugin(md: MarkdownIt):
    md.inline.ruler.push("attachment", attachment_rule)


def attachment_rule(state: StateInline, silent: bool):
    start = state.pos
    maximum = state.posMax

    args_start = start + 12
    if state.src[start:args_start].lower() != "<attachment=":
        return False

    pos = args_start
    while pos <= maximum:
        if state.src[pos] == ">":
            break

        pos += 1

    if state.src[pos] != ">":
        return False

    args_end = pos
    end = args_end

    attrs = parse_args(state.src[args_start:args_end])
    if not attrs:
        return False

    if not silent:
        token = state.push("attachment", "misago-attachment", 0)
        token.markup = state.src[start:end]
        token.attrs = attrs
        token.meta = {"attachment": attrs["id"]}

    state.pos = end + 1
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
