from markdown_it import MarkdownIt
from markdown_it.rules_inline.state_inline import StateInline
from markdown_it.token import Token


def attachment_plugin(md: MarkdownIt):
    md.inline.ruler.before("autolink", "attachment", attachment_rule)


def attachment_rule(state: StateInline, silent: bool):
    pos = state.pos

    if state.src[pos : pos + 12] != "<attachment=":
        return False

    raise Exception(state)
    return False
