from dataclasses import dataclass
from typing import Callable

from markdown_it.rules_block.state_block import StateBlock
from markdown_it.token import Token

BBCodeArgsParser = Callable[[str], dict | None]


@dataclass(frozen=True)
class BBCodeBlockStart:
    start: int
    end: int
    markup: str
    attrs: dict | None


@dataclass(frozen=True)
class BBCodeBlockEnd:
    start: int
    end: int
    markup: str


class BBCodeBlockRule:
    name: str
    bbcode: str
    bbcode_len: int
    element: str
    args_parser: BBCodeArgsParser | None

    def __init__(
        self,
        name: str,
        bbcode: str,
        element: str,
        args_parser: BBCodeArgsParser,
    ):
        self.name = name
        self.bbcode = bbcode
        self.bbcode_len = len(bbcode)
        self.element = element
        self.args_parser = args_parser

    def __call__(
        self, state: StateBlock, startLine: int, endLine: int, silent: bool
    ) -> bool:
        if state.is_code_block(startLine):
            return False

        if self.parse_single_line(state, startLine, silent):
            return True

        return self.parse_multiple_lines(state, startLine, endLine, silent)

    def parse_single_line(
        self,
        state: StateBlock,
        line: int,
        silent: bool,
    ) -> bool:
        start = self.find_single_line_bbcode_block_start(state, line)
        if not start:
            return False

        end = self.find_single_line_bbcode_block_end(state, line, start.end)
        if not end:
            return False

        if silent:
            return True

        old_parent_type = state.parentType

        state.parentType = self.name
        self.state_push_open_token(state, line, line, start.markup, start.attrs)

        state.parentType = "paragraph"
        token = state.push("paragraph_open", "p", 1)
        token.map = [line, line]

        token = state.push("inline", "", 0)
        token.content = state.src[start.end : end.start].strip()
        token.map = [line, line]
        token.children = []

        token = state.push("paragraph_close", "p", -1)

        self.state_push_close_token(state, end.markup)

        state.parentType = old_parent_type
        state.line += 1

        return True

    def find_single_line_bbcode_block_start(
        self, state: StateBlock, line: int
    ) -> BBCodeBlockStart | None:
        pos = state.bMarks[line] + state.tShift[line]
        maximum = state.eMarks[line]

        while pos < maximum:
            if state.src[pos] == "[":
                break
            elif state.src[pos] == " ":
                pos += 1
            else:
                return None
        else:
            return None

        start = pos

        pos += 1
        if state.src[pos : pos + self.bbcode_len].lower() != self.bbcode:
            return None

        pos += self.bbcode_len
        if state.src[pos] == "]":
            end = pos + 1

            return BBCodeBlockStart(
                start=start,
                end=end,
                markup=state.src[start:end],
                attrs=None,
            )

        if state.src[pos] != "=" or not self.args_parser:
            return None

        pos += 1

        level = 1
        args_start = pos

        while pos < maximum:
            if state.src[pos] == "\\":
                pos += 2

            elif state.src[pos] == "[":
                level += 1
                pos += 1

            elif state.src[pos] == "]":
                level -= 1
                if not level:
                    attrs = None
                    if args_str := state.src[args_start:pos].strip():
                        attrs = self.parse_args(args_str)

                    end = pos + 1
                    return BBCodeBlockStart(
                        start=start,
                        end=end,
                        markup=state.src[start:end],
                        attrs=attrs,
                    )

                pos += 1

            else:
                pos += 1

        else:
            return None

    def find_single_line_bbcode_block_end(
        self, state: StateBlock, line: int, minimum: int
    ) -> BBCodeBlockEnd | None:
        maximum = state.eMarks[line]

        start = None
        end = None

        pos = minimum
        while pos < maximum:
            if state.src[pos] == "\\":
                pos += 2
            else:
                bbcode_end = pos + self.bbcode_len + 3
                if state.src[pos:bbcode_end].lower() == f"[/{self.bbcode}]":
                    start = pos
                    end = bbcode_end
                pos += 1
        else:
            if start is None:
                return None

        if state.src[end:maximum].strip():
            return None

        return BBCodeBlockEnd(
            start=start,
            end=end,
            markup=state.src[start:end],
        )

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

        end = None
        nesting = 1

        while line < endLine:
            line += 1

            if (
                state.isEmpty(line)
                or state.is_code_block(line)
                or self.parse_single_line(state, line, True)
                or line > state.lineMax
            ):
                continue

            if self.find_multi_line_bbcode_block_start(state, line):
                nesting += 1

            elif match := self.find_multi_line_bbcode_block_end(state, line):
                nesting -= 1

                if nesting == 0:
                    end = match
                    break

        if silent or not end:
            return nesting == 0

        self.state_push_open_token(state, startLine, line, start.markup, start.attrs)
        self.state_push_children(state, startLine + 1, line)
        self.state_push_close_token(state, end.markup)

        state.line = line + 1
        return True

    def find_multi_line_bbcode_block_start(
        self, state: StateBlock, line: int
    ) -> BBCodeBlockStart | None:
        pos = state.bMarks[line] + state.tShift[line]
        maximum = state.eMarks[line]

        while pos < maximum:
            if state.src[pos] == "[":
                break
            elif state.src[pos] == " ":
                pos += 1
            else:
                return None
        else:
            return None

        start = pos

        pos += 1
        if state.src[pos : pos + self.bbcode_len].lower() != self.bbcode:
            return None

        pos += self.bbcode_len
        if state.src[pos] == "]":
            end = pos + 1

            if state.src[end:maximum].strip():
                return None

            return BBCodeBlockStart(
                start=start,
                end=end,
                markup=state.src[start:end],
                attrs=None,
            )

        if state.src[pos] != "=":
            return None

        if not self.args_parser:
            return None

        pos += 1

        level = 1
        args_start = pos

        while pos < maximum:
            if state.src[pos] == "\\":
                pos += 2

            elif state.src[pos] == "[":
                level += 1
                pos += 1

            elif state.src[pos] == "]":
                level -= 1
                if not level:
                    attrs = None
                    if args_str := state.src[args_start:pos].strip():
                        attrs = self.parse_args(args_str)

                    end = pos + 1
                    if state.src[end:maximum].strip():
                        return None

                    return BBCodeBlockStart(
                        start=start,
                        end=pos,
                        markup=state.src[start:pos],
                        attrs=attrs,
                    )

                pos += 1

            else:
                pos += 1

        else:
            return None

    def find_multi_line_bbcode_block_end(
        self, state: StateBlock, line: int
    ) -> BBCodeBlockEnd | None:
        pos = state.bMarks[line] + state.tShift[line]
        maximum = state.eMarks[line]

        while pos < maximum:
            if state.src[pos] == "[":
                start = pos
                break
            elif state.src[pos] == " ":
                pos += 1
            else:
                return None

        pos += 1
        if state.src[pos] != "/":
            return None

        pos += 1
        if state.src[pos : pos + self.bbcode_len].lower() != self.bbcode:
            return None

        pos += self.bbcode_len
        if state.src[pos] != "]":
            return None

        end = pos + 1
        if state.src[end:maximum].strip():
            return None

        return BBCodeBlockEnd(
            start=start,
            end=end,
            markup=state.src[start:end],
        )

    def parse_args(self, args_str: str) -> dict | None:
        if args_str and (
            (args_str[0] == '"' and args_str[-1] == '"')
            or (args_str[0] == "'" and args_str[-1] == "'")
        ):
            args_str = args_str[1:-1]

        args_str = args_str.strip() or None
        if args_str:
            return self.args_parser(args_str)

        return None

    def state_push_open_token(
        self,
        state: StateBlock,
        startLine: int,
        endLine: int,
        markup: str,
        attrs: dict | None = None,
    ) -> Token:
        token = state.push(f"{self.name}_open", self.element, 1)
        token.markup = markup
        token.map = [startLine, endLine]

        if attrs:
            for attr_name, attr_value in attrs.items():
                token.attrSet(attr_name, attr_value)

            if meta := self.get_meta(attrs):
                token.meta = meta

        return token

    def state_push_close_token(self, state: StateBlock, markup: str) -> Token:
        token = state.push(f"{self.name}_close", self.element, -1)
        token.markup = markup
        return token

    def state_push_void_token(
        self, state: StateBlock, line: int, markup: str, attrs: dict | None
    ) -> Token:
        token = state.push(self.name, self.element, 0)
        token.markup = markup
        token.map = [line, line]

        if attrs:
            for attr_name, attr_value in attrs.items():
                token.attrSet(attr_name, attr_value)

            if meta := self.get_meta(attrs):
                token.meta = meta

        return token

    def state_push_children(self, state: StateBlock, startLine: int, endLine: int):
        if startLine == endLine:
            return

        old_line_max = state.lineMax
        old_parent = state.parentType

        state.lineMax = endLine
        state.parentType = self.name

        state.level += 1
        state.md.block.tokenize(state, startLine, endLine)
        state.level -= 1

        state.lineMax = old_line_max
        state.parentType = old_parent

    def get_meta(self, attrs: dict) -> dict | None:
        return None
