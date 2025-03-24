from contextlib import contextmanager

from markdown_it.rules_block.state_block import StateBlock


@contextmanager
def parse_nested_blocks(state: StateBlock, parent: str, start_line: int, end_line: int):
    if start_line + 1 == end_line:
        return

    old_line_max = state.lineMax
    old_parent = state.parentType

    state.lineMax = start_line + 1
    state.parentType = parent

    state.level += 1
    state.md.block.tokenize(state, start_line + 1, end_line - 1)
    state.level -= 1

    state.lineMax = old_line_max
    state.parentType = old_parent
