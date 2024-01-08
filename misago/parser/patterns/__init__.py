from ..parser import Pattern

from .code import FencedCodeMarkdown


block_patterns: list[Pattern] = [
    FencedCodeMarkdown(),
]

inline_patterns: list[Pattern] = []
