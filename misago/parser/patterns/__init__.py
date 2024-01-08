from ..parser import Pattern

from .code import CodeBBCode, FencedCodeMarkdown, InlineCodeMarkdown


block_patterns: list[Pattern] = [
    FencedCodeMarkdown(),
    CodeBBCode(),
]

inline_patterns: list[Pattern] = [
    InlineCodeMarkdown(),
]
