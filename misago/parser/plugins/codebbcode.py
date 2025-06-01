from textwrap import dedent
from typing import Sequence

from markdown_it import MarkdownIt
from markdown_it.common.utils import escapeHtml
from markdown_it.renderer import RendererHTML
from markdown_it.rules_block.state_block import StateBlock
from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

from ..bbcode import BBCodeBlockRule
from ..codeargs import parse_code_args


def code_bbcode_plugin(md: MarkdownIt):
    md.block.ruler.before(
        "paragraph",
        "code_bbcode",
        CodeBBCodeBlockRule(
            name="code_bbcode",
            bbcode="code",
            element="code",
            args_parser=parse_code_args,
        ),
        {"alt": ["paragraph"]},
    )

    md.add_render_rule("code_bbcode", code_bbcode_renderer)


class CodeBBCodeBlockRule(BBCodeBlockRule):
    def parse_single_line(
        self,
        state: StateBlock,
        line: int,
        silent: bool,
    ):
        start = self.find_single_line_bbcode_block_start(state, line)
        if not start:
            return False

        end = self.find_single_line_bbcode_block_end(state, line, start.end)
        if not end:
            return False

        if silent:
            return True

        token = self.state_push_void_token(state, line, start.markup, start.attrs)
        token.content = state.src[start.end : end.start].strip()

        state.line += 1
        return True

    def parse_multiple_lines(
        self,
        state: StateBlock,
        startLine: int,
        endLine: int,
        silent: bool,
    ) -> bool:
        line = startLine

        start = self.find_multi_line_bbcode_block_start(state, line)
        if not start:
            return False

        line += 1
        while line < endLine:
            if self.find_multi_line_bbcode_block_end(state, line):
                break

            line += 1
        else:
            return False

        if silent:
            return True

        token = self.state_push_void_token(state, startLine, start.markup, start.attrs)
        token.content = self.get_lines(state, startLine + 1, line)

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
