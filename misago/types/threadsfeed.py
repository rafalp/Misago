from dataclasses import dataclass, field
from typing import List, Optional

from .thread import Thread


@dataclass
class ThreadsFeed:
    items: List[Thread] = field(default_factory=list)
    next_cursor: Optional[int] = None
