from ..parser import Pattern

from .code import (
    CodeBBCode,
    FencedCodeMarkdown,
    IndentedCodeMarkdown,
    InlineCodeMarkdown,
)
from .headings import AtxHeading, SetexHeading
from .lists import ListMarkdown
from .quote import QuoteBBCodeOpen, QuoteBBCodeClose, QuoteMarkdown
from .spoiler import SpoilerBBCodeOpen, SpoilerBBCodeClose
from .thematicbreak import ThematicBreakBBCode, ThematicBreakMarkdown


block_patterns: list[Pattern] = [
    FencedCodeMarkdown(),
    CodeBBCode(),
    AtxHeading(),
    SetexHeading(),
    ThematicBreakBBCode(),
    ThematicBreakMarkdown(),
    ListMarkdown(),
    IndentedCodeMarkdown(),
    QuoteMarkdown(),
    QuoteBBCodeOpen(),
    QuoteBBCodeClose(),
    SpoilerBBCodeOpen(),
    SpoilerBBCodeClose(),
]

inline_patterns: list[Pattern] = [
    InlineCodeMarkdown(),
]
