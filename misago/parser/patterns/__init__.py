from ..parser import Pattern

from .code import CodeBBCode, FencedCodeMarkdown, InlineCodeMarkdown
from .lists import ListMarkdown
from .quote import QuoteBBCodeOpen, QuoteBBCodeClose


block_patterns: list[Pattern] = [
    FencedCodeMarkdown(),
    CodeBBCode(),
    ListMarkdown(),
    QuoteBBCodeOpen(),
    QuoteBBCodeClose(),
]

inline_patterns: list[Pattern] = [
    InlineCodeMarkdown(),
]
