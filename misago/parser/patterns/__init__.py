from ..parser import Pattern

from .bbcode import (
    BoldBBCodePattern,
    InlineBBCodePattern,
    ItalicsBBCodePattern,
    StrikethroughBBCodePattern,
    SubscriptBBCodePattern,
    SuperscriptBBCodePattern,
    UnderlineBBCodePattern,
)
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

bold_bbcode = BoldBBCodePattern()
italics_bbcode = ItalicsBBCodePattern()
underline_bbcode = UnderlineBBCodePattern()
strikethrough_bbcode = StrikethroughBBCodePattern()
superscript_bbcode = SuperscriptBBCodePattern()
subscript_bbcode = SubscriptBBCodePattern()

inline_patterns: list[Pattern] = [
    InlineCodeMarkdown(),
    bold_bbcode,
    italics_bbcode,
    underline_bbcode,
    strikethrough_bbcode,
    superscript_bbcode,
    subscript_bbcode,
]
