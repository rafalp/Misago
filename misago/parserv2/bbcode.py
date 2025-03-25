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

        opening, ending = self.scan_full_line(state, startLine)
        if opening and ending:
            if silent:
                return True

            return self.parse_single_line(state, startLine, opening, ending)

        if not opening:
            return False

        line = startLine
        start = state.bMarks[line] + state.tShift[line]
        maximum = state.eMarks[line]

        if state.src[start + opening[3] : maximum].strip():
            return False

        markup, attrs = opening
        closing = None

        nesting = 1
        line += 1

        while line <= endLine:
            start = state.bMarks[line] + state.tShift[line]
            maximum = state.eMarks[line]
            src = state.src[start:maximum]

            if state.is_code_block(startLine):
                line += 1
                continue

            if self.start(src):
                nesting += 1

            elif match := self.end(src):
                nesting -= 1

                if nesting == 0:
                    closing = match
                    break

            line += 1

        if silent:
            return nesting == 0

        max_line = line + 1

        token = state.push(f"{self.name}_open", self.element, 1)
        token.markup = markup
        token.map = [startLine, max_line]

        if attrs:
            for attr_name, attr_value in attrs.items():
                token.attrSet(attr_name, attr_value)

        self.parse_children_blocks(state, startLine, max_line)

        token = state.push(f"{self.name}_close", self.element, -1)
        token.markup = closing

        state.line = max_line + 1
        return True

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
                match = rule(state, line)
                if match:
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
        old_parent_type = state.parentType

        line_start = state.bMarks[startLine] + state.tShift[startLine]
        content_start = line_start + start[3]
        content_end = line_start + end[1]

        state.parentType = self.name
        self.state_push_open_token(state, startLine, startLine, start)

        state.parentType = "paragraph"
        token = state.push("paragraph_open", "p", 1)
        token.map = [startLine, startLine]

        token = state.push("inline", "", 0)
        token.content = state.src[content_start:content_end].strip()
        token.map = [startLine, state.line]
        token.children = []

        token = state.push("paragraph_close", "p", -1)

        self.state_push_close_token(state, end)

        state.parentType = old_parent_type
        state.line += 1

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

        return token

    def state_push_close_token(self, state: StateBlock, end: BBCodeBlockEnd) -> Token:
        token = state.push(f"{self.name}_close", self.element, -1)
        token.markup = end[0]
        return token

    def parse_children_blocks(self, state: StateBlock, startLine: int, endLine: int):
        if startLine + 1 == endLine:
            return

        old_line_max = state.lineMax
        old_parent = state.parentType

        state.lineMax = startLine + 1
        state.parentType = self.name

        state.level += 1
        state.md.block.tokenize(state, startLine + 1, endLine - 1)
        state.level -= 1

        state.lineMax = old_line_max
        state.parentType = old_parent
