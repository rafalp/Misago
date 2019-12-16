from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Post:
    id: int
    category_id: int
    thread_id: int
    poster_name: str
    body: dict
    edits: int
    posted_at: datetime
    extra: dict
    poster_id: Optional[int]
