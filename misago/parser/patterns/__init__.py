from ..parser import Pattern

from .code import (
    CodeBBCode,
    FencedCodeMarkdown,
    IndentedCodeMarkdown,
    InlineCodeMarkdown,
)
from .headings import AtxHeading
from .lists import ListMarkdown
from .quote import QuoteBBCodeOpen, QuoteBBCodeClose, QuoteMarkdown
from .spoiler import SpoilerBBCodeOpen, SpoilerBBCodeClose


block_patterns: list[Pattern] = [
    FencedCodeMarkdown(),
    CodeBBCode(),
    ListMarkdown(),
    IndentedCodeMarkdown(),
    AtxHeading(),
    QuoteMarkdown(),
    QuoteBBCodeOpen(),
    QuoteBBCodeClose(),
    SpoilerBBCodeOpen(),
    SpoilerBBCodeClose(),
]

inline_patterns: list[Pattern] = [
    InlineCodeMarkdown(),
]
