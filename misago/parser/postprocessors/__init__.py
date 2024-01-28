from .block import BlockPostProcessor
from .quote import QuoteBBCodePostProcessor
from .removerepeats import RemoveRepeatsPostProcessor
from .spoiler import SpoilerBBCodePostProcessor
from .thematicbreak import RemoveThematicBreaksRepeatsPostProcessor

__all__ = [
    "BlockPostProcessor",
    "QuoteBBCodePostProcessor",
    "RemoveRepeatsPostProcessor",
    "SpoilerBBCodePostProcessor",
    "post_processors",
]

post_processors = [
    QuoteBBCodePostProcessor(),
    SpoilerBBCodePostProcessor(),
    RemoveThematicBreaksRepeatsPostProcessor(),
]
