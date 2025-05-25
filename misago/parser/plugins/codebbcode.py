from textwrap import dedent
from typing import Sequence

from markdown_it import MarkdownIt
from markdown_it.common.utils import escapeHtml
from markdown_it.renderer import RendererHTML
from markdown_it.rules_block.state_block import StateBlock
from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

from ..args import parse_code_args
from ..bbcode import (
    BBCodeBlockEnd,
    BBCodeBlockRule,
    BBCodeBlockStart,
    bbcode_block_end_rule,
    bbcode_block_start_rule,
)


def code_bbcode_plugin(md: MarkdownIt):
    md.block.ruler.before(
        "paragraph",
        "code_bbcode",
        CodeBBCodeBlockRule(
            name="code_bbcode",
            element="code",
            start=code_bbcode_start,
            end=code_bbcode_end,
        ),
        {"alt": ["paragraph"]},
    )

    md.add_render_rule("code_bbcode", code_bbcode_renderer)


class CodeBBCodeBlockRule(BBCodeBlockRule):
    def parse_single_line(
        self,
        state: StateBlock,
        startLine: int,
        start: BBCodeBlockStart,
        end: BBCodeBlockEnd,
    ):
        content_start = start[3]
        content_end = end[1]
        content = state.src[content_start:content_end].strip()

        token = self.state_push_void_token(state, startLine, start)
        token.content = content

        state.line += 1

        return True

    def parse_multiple_lines(
        self,
        state: StateBlock,
        startLine: int,
        endLine: int,
        silent: bool,
        start: BBCodeBlockStart,
    ) -> bool:
        line = startLine
        pos = state.bMarks[line] + state.tShift[line] + start[3]
        maximum = state.eMarks[line]

        if state.src[pos:maximum].strip():
            return False

        end = None

        while line < endLine:
            line += 1

            if (
                state.isEmpty(line)
                or state.is_code_block(line)
                or all(self.scan_full_line(state, line))
                or line > state.lineMax
            ):
                continue

            if match := self.scan_line_for_end(state, line):
                end = match

        if silent or not end:
            return bool(end)

        token = self.state_push_void_token(state, startLine, start)
        token.content = self.get_lines(state, startLine + 1, line - 1)

        state.line = line + 1
        return True

    def get_lines(self, state: StateBlock, startLine: int, endLine: int):
        length = state.sCount[startLine]
        content = state.getLines(startLine, endLine, length, False).rstrip()

        lines: list[str] = []
        for line in content.splitlines():
            if line.strip() or lines:
                lines.append(line)

        return dedent("\n".join(lines))

    def get_meta(self, attrs: dict) -> dict | None:
        if attrs.get("syntax"):
            return {"syntax": attrs["syntax"]}

        return None


def code_bbcode_start(
    state: StateBlock, line: int
) -> tuple[str, dict | None, int, int] | None:
    start = bbcode_block_start_rule("code", state, line, args=True)
    if not start:
        return None

    markup, args_str, start, end = start

    if args_str:
        args = parse_code_args(args_str)
    else:
        args = None

    return markup, args, start, end


def code_bbcode_end(state: StateBlock, line: int) -> tuple[str, int, int] | None:
    return bbcode_block_end_rule("code", state, line)


def code_bbcode_renderer(
    renderer: RendererHTML,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    token = tokens[idx]

    return (
        "<misago-code"
        + renderer.renderAttrs(token)
        + ">"
        + escapeHtml(token.content)
        + "</misago-code>\n"
    )
