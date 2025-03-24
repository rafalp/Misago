from typing import Callable

from markdown_it.rules_block.state_block import StateBlock


class BBCodeBlockRule:
    name: str
    element: str
    start: Callable[[str], tuple[str, dict | None]]
    end: Callable[[str], str | None]

    def __init__(
        self,
        name: str,
        element: str,
        start: Callable[[str], tuple[str, dict | None]],
        end: Callable[[str], str | None],
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

        line = startLine

        start = state.bMarks[line] + state.tShift[line]
        maximum = state.eMarks[line]

        opening = self.start(state.src[start:maximum])
        if not opening:
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
