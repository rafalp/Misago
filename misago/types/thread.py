from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Thread:
    id: int
    category_id: int
    starter_name: str
    last_poster_name: str
    title: str
    slug: str
    started_at: datetime
    last_posted_at: datetime
    ordering: int
    replies: int
    is_closed: bool
    extra: dict

    first_post_id: Optional[int]
    starter_id: Optional[int]
    last_poster_id: Optional[int]
