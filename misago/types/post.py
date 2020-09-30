from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .richtext import RichText


@dataclass
class Post:
    id: int
    category_id: int
    thread_id: int
    poster_name: str
    markup: str
    rich_text: RichText
    html: str
    edits: int
    posted_at: datetime
    extra: dict
    poster_id: Optional[int]
