import re

from markdown_it import MarkdownIt
from markdown_it.rules_block.state_block import StateBlock


def hr_bbcode_plugin(md: MarkdownIt):
    md.block.ruler.before(
        "paragraph",
        "hr_bbcode",
        hr_bbcode_rule,
        {"alt": ["paragraph"]},
    )


HR = re.compile(r"^ *\[hr\]( *\[hr\])* *$", re.IGNORECASE)


def hr_bbcode_rule(
    state: StateBlock, startLine: int, endLine: int, silent: bool
) -> bool:
    if state.is_code_block(startLine):
        return False

    start = state.bMarks[startLine] + state.tShift[startLine]
    maximum = state.eMarks[startLine]

    line = state.src[start:maximum]

    if not HR.match(line):
        return False

    if silent:
        return True

    state.line = startLine + 1

    if not state.tokens or state.tokens[-1].type not in ("hr", "hr_bbcode"):
        token = state.push("hr_bbcode", "hr", 0)
        token.map = [startLine, state.line]
        token.markup = "[hr]"

    return True
