from .attachment import AttachmentPostProcessor
from .block import BlockPostProcessor
from .quote import QuoteBBCodePostProcessor
from .removerepeats import RemoveRepeatsPostProcessor
from .spoiler import SpoilerBBCodePostProcessor
from .thematicbreak import RemoveThematicBreaksRepeatsPostProcessor

__all__ = [
    "AttachmentPostProcessor",
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
    AttachmentPostProcessor(),
]
