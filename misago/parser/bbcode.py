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
    args: dict | None


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
        self.state_push_open_token(state, line, line, start.markup, start.args)

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
                args=None,
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
                    args_str = state.src[args_start:pos]
                    if args_str:
                        args = self.parse_args(args_str)

                    end = pos + 1

                    return BBCodeBlockStart(
                        start=start,
                        end=end,
                        markup=state.src[start:end],
                        args=args,
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
        return False

        line = startLine
        start = state.bMarks[line] + state.tShift[line]
        maximum = state.eMarks[line]

        args = None

        pos = start
        while pos < maximum:
            if state.src[pos] == "\\":
                pos += 2
            elif state.src[pos] == "[":
                pos += 1
                bbcode = state.src[pos : pos + self.bbcode_len].lower()
                if bbcode != self.bbcode:
                    return False

                if state.src[pos + self.bbcode_len] == "]":
                    pos = content_start = pos + self.bbcode_len + 1
                    break

                elif state.src[pos + self.bbcode_len] == "=":
                    if not self.args_parser:
                        return False

                    level = 1
                    pos = args_start = pos + self.bbcode_len + 1
                    while pos < maximum:
                        if state.src[pos] == "\\":
                            pos += 2
                        elif state.src[pos] == "[":
                            level += 1
                            pos += 1
                        elif state.src[pos] == "]":
                            level -= 1
                            if not level:
                                args_str = state.src[args_start:pos]
                                if args_str:
                                    args = self.parse_args(args_str)
                                pos = content_start = pos + 1
                                break

                            pos += 1

                        else:
                            pos += 1

                    else:
                        return False

                    break

                else:
                    return False

            elif state.src[pos] == "]":
                break

            else:
                pos += 1
        else:
            return False

        state.src[pos]

        return False

        end = None
        nesting = 1

        while line < endLine:
            line += 1

            if (
                state.isEmpty(line)
                or state.is_code_block(line)
                or all(self.scan_single_line(state, line))
                or line > state.lineMax
            ):
                continue

            if self.scan_line_for_start(state, line):
                nesting += 1

            elif match := self.scan_line_for_end(state, line):
                nesting -= 1

                if nesting == 0:
                    end = match
                    break

        if silent or not end:
            return nesting == 0

        self.state_push_open_token(state, startLine, line, start)
        self.state_push_children(state, startLine + 1, line)
        self.state_push_close_token(state, end)

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
                args=None,
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
                    args_str = state.src[args_start:pos]
                    if args_str:
                        args = self.parse_args(args_str)

                    end = pos + 1
                    if state.src[end:maximum].strip():
                        return None

                    return BBCodeBlockStart(
                        start=start,
                        end=pos,
                        markup=state.src[start:pos],
                        args=args,
                    )

                pos += 1

            else:
                pos += 1

        else:
            return None

    def find_bbcode_end(
        self, state: StateBlock, line: int, start: int, single_line: bool
    ) -> BBCodeBlockEnd | None:
        if single_line:
            return self.find_single_line_bbcode_end(state, line, start)

        return self.find_multi_line_bbcode_end(state, line, start)

    def find_single_line_bbcode_end(
        self, state: StateBlock, line: int, start: int
    ) -> BBCodeBlockEnd | None:
        maximum = state.eMarks[line]

        raise NotImplementedError()

    def find_multi_line_bbcode_end(
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
        self, state: StateBlock, startLine: int, start: BBCodeBlockStart
    ) -> Token:
        token = state.push(f"{self.name}", self.element, 0)
        token.markup = start[0]
        token.map = [startLine, startLine]

        if attrs := start[1]:
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


def bbcode_block_start_rule(
    bbcode: str, state: StateBlock, line: int, args: bool = False
) -> tuple[str, str | None, int, int] | None:
    start = state.bMarks[line] + state.tShift[line]
    maximum = state.eMarks[line]
    src = state.src[start:maximum]

    block_bbcode = f"[{bbcode}".lower()
    block_bbcode_len = len(block_bbcode)

    if src.lower()[:block_bbcode_len] != block_bbcode:
        return None

    if "]" not in src[block_bbcode_len:]:
        return None

    end = src.index("]", 0, maximum - start)
    if end == block_bbcode_len:
        return src[: block_bbcode_len + 1], None, start, start + end + 1

    if src[block_bbcode_len] != "=" or not args:
        return None

    args_str = src[block_bbcode_len + 1 : end]
    if args_str and (
        (args_str[0] == '"' and args_str[-1] == '"')
        or (args_str[0] == "'" and args_str[-1] == "'")
    ):
        args_str = args_str[1:-1]

    args_str = args_str.strip() or None

    return src[: end + 1], args_str, start, end + 1


def bbcode_block_end_rule(
    bbcode: str, state: StateBlock, line: int
) -> tuple[str, int, int] | None:
    start = state.bMarks[line] + state.tShift[line]
    maximum = state.eMarks[line]
    src = state.src[start:maximum]

    block_bbcode = f"[/{bbcode}]".lower()
    block_bbcode_len = len(block_bbcode)

    if src[:block_bbcode_len].lower() == block_bbcode:
        return src[:block_bbcode_len], start, start + block_bbcode_len

    return None
