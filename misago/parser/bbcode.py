from typing import Callable

from markdown_it.rules_block.state_block import StateBlock
from markdown_it.token import Token

BBCodeBlockStart = tuple[str, dict | None, int, int]
BBCodeBlockEnd = tuple[str, int, int]
BBCodeBlockStartRule = Callable[[StateBlock, int], BBCodeBlockStart | None]
BBCodeBlockEndRule = Callable[[StateBlock, int], BBCodeBlockEnd | None]


class BBCodeBlockRule:
    name: str
    element: str
    start: BBCodeBlockStartRule
    end: BBCodeBlockEndRule

    def __init__(
        self,
        name: str,
        element: str,
        start: BBCodeBlockStartRule,
        end: BBCodeBlockEndRule,
    ):
        self.name = name
        self.element = element

        self.start = start
        self.end = end

    def __call__(
        self, state: StateBlock, startLine: int, endLine: int, silent: bool
    ) -> bool:
        if state.is_code_block(startLine):
            return False

        start, end = self.scan_full_line(state, startLine)
        if start and end:
            if silent:
                return True

            return self.parse_single_line(state, startLine, start, end)

        if not start:
            return False

        return self.parse_multiple_lines(state, startLine, endLine, silent, start)

    def scan_full_line(
        self, state: StateBlock, line: int
    ) -> tuple[BBCodeBlockStart | None, BBCodeBlockEnd | None]:
        start = self.scan_line_for_start(state, line)

        if start:
            end = self.scan_line_for_end(state, line, True)
            if end and end[1] > start[3]:
                return start, end

        return start, None

    def scan_line_for_start(
        self, state: StateBlock, line: int
    ) -> BBCodeBlockStart | None:
        return self._scan_line_from_start(state, line, self.start)

    def scan_line_for_end(
        self, state: StateBlock, line: int, closing: bool = False
    ) -> BBCodeBlockEnd | None:
        if closing:
            return self._scan_line_from_end(state, line, self.end)

        return self._scan_line_from_start(state, line, self.end)

    def _scan_line_from_start(
        self,
        state: StateBlock,
        line: int,
        rule: BBCodeBlockStartRule | BBCodeBlockEndRule,
    ) -> BBCodeBlockStart | BBCodeBlockEnd | None:
        org_bmark = state.bMarks[line]
        maximum = state.eMarks[line]
        steps = 0

        try:
            while (state.bMarks[line] + state.tShift[line]) < maximum and steps < 3:
                if match := rule(state, line):
                    return match

                if state.src[state.bMarks[line] + state.tShift[line]]:
                    return None

                state.bMarks[line] += 1
                steps += 1

            return None
        except Exception:
            raise
        finally:
            state.bMarks[line] = org_bmark

    def _scan_line_from_end(
        self,
        state: StateBlock,
        line: int,
        rule: BBCodeBlockEndRule,
    ) -> BBCodeBlockEnd | None:
        org_bmark = state.bMarks[line]
        state.bMarks[line] = state.eMarks[line]
        maximum = state.eMarks[line]

        try:
            while state.bMarks[line] >= org_bmark:
                if match := rule(state, line):
                    if state.src[match[2] : maximum].strip():
                        return None

                    return match

                state.bMarks[line] -= 1

            return None
        except Exception:
            raise
        finally:
            state.bMarks[line] = org_bmark

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

        old_parent_type = state.parentType

        state.parentType = self.name
        self.state_push_open_token(state, startLine, startLine, start)

        state.parentType = "paragraph"
        token = state.push("paragraph_open", "p", 1)
        token.map = [startLine, startLine]

        token = state.push("inline", "", 0)
        token.content = content
        token.map = [startLine, state.line]
        token.children = []

        token = state.push("paragraph_close", "p", -1)

        self.state_push_close_token(state, end)

        state.parentType = old_parent_type
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
        nesting = 1

        while line < endLine:
            line += 1

            if (
                state.isEmpty(line)
                or state.is_code_block(line)
                or all(self.scan_full_line(state, line))
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

    def state_push_open_token(
        self, state: StateBlock, startLine: int, endLine: int, start: BBCodeBlockStart
    ) -> Token:
        token = state.push(f"{self.name}_open", self.element, 1)
        token.markup = start[0]
        token.map = [startLine, endLine]

        if attrs := start[1]:
            for attr_name, attr_value in attrs.items():
                token.attrSet(attr_name, attr_value)

            if meta := self.get_meta(attrs):
                token.meta = meta

        return token

    def state_push_close_token(self, state: StateBlock, end: BBCodeBlockEnd) -> Token:
        token = state.push(f"{self.name}_close", self.element, -1)
        token.markup = end[0]
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

        state.lineMax = startLine
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
