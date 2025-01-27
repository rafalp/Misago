from .attachments import AttachmentsPostProcessor
from .block import BlockPostProcessor
from .quote import QuoteBBCodePostProcessor
from .removerepeats import RemoveRepeatsPostProcessor
from .spoiler import SpoilerBBCodePostProcessor
from .thematicbreak import RemoveThematicBreaksRepeatsPostProcessor

__all__ = [
    "AttachmentsPostProcessor",
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
    AttachmentsPostProcessor(),
]
