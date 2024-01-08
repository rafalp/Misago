from ..parser import Pattern

from .code import CodeBBCode, FencedCodeMarkdown


block_patterns: list[Pattern] = [
    FencedCodeMarkdown(),
    CodeBBCode(),
]

inline_patterns: list[Pattern] = []
