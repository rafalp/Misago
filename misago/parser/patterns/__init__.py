from ..parser import Pattern

from .code import CodeBBCode, FencedCodeMarkdown, InlineCodeMarkdown
from .lists import ListMarkdown


block_patterns: list[Pattern] = [
    FencedCodeMarkdown(),
    CodeBBCode(),
    ListMarkdown(),
]

inline_patterns: list[Pattern] = [
    InlineCodeMarkdown(),
]
