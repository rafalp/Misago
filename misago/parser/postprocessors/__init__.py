from .block import BlockPostProcessor
from .quote import QuoteBBCodePostProcessor
from .spoiler import SpoilerBBCodePostProcessor

__all__ = [
    "BlockPostProcessor",
    "QuoteBBCodePostProcessor",
    "SpoilerBBCodePostProcessor",
    "post_processors",
]

post_processors = [
    QuoteBBCodePostProcessor(),
    SpoilerBBCodePostProcessor(),
]
