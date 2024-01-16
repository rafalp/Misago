from ..parser import Pattern

from .bbcode import (
    BoldBBCode,
    InlineBBCodePattern,
    ItalicsBBCode,
    StrikethroughBBCode,
    SubscriptBBCode,
    SuperscriptBBCode,
    UnderlineBBCode,
)
from .code import (
    CodeBBCode,
    FencedCodeMarkdown,
    IndentedCodeMarkdown,
    InlineCodeMarkdown,
)
from .headings import AtxHeading, SetexHeading
from .lists import ListMarkdown
from .markdown import (
    EmphasisMarkdown,
    EmphasisUnderscoreMarkdown,
    StrikethroughMarkdown,
    StrongMarkdown,
    StrongUnderscoreMarkdown,
)
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

bold_bbcode = BoldBBCode()
italics_bbcode = ItalicsBBCode()
underline_bbcode = UnderlineBBCode()
strikethrough_bbcode = StrikethroughBBCode()
superscript_bbcode = SuperscriptBBCode()
subscript_bbcode = SubscriptBBCode()

emphasis_markdown = EmphasisMarkdown()
emphasis_underscore_markdown = EmphasisUnderscoreMarkdown()

strong_markdown = StrongMarkdown()
strong_underscore_markdown = StrongUnderscoreMarkdown()

strikethrough_markdown = StrikethroughMarkdown()

inline_patterns: list[Pattern] = [
    InlineCodeMarkdown(),
    bold_bbcode,
    italics_bbcode,
    underline_bbcode,
    strikethrough_bbcode,
    superscript_bbcode,
    subscript_bbcode,
    strong_markdown,
    emphasis_markdown,
    strong_underscore_markdown,
    emphasis_underscore_markdown,
    strikethrough_markdown,
]
