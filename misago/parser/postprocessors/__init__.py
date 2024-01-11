from .block import BlockPostProcessor
from .quote import QuoteBBCodePostProcessor

__all__ = ["BlockPostProcessor", "QuoteBBCodePostProcessor", "post_processors"]

post_processors = [
    QuoteBBCodePostProcessor(),
]
