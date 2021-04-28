from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from ..richtext import RichText
from ..types import PaginationPage


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
    replies: int
    is_closed: bool
    extra: dict

    first_post_id: Optional[int]
    starter_id: Optional[int]
    last_post_id: Optional[int]
    last_poster_id: Optional[int]


@dataclass
class Post:
    id: int
    category_id: int
    thread_id: int
    poster_name: str
    markup: str
    rich_text: RichText
    edits: int
    posted_at: datetime
    extra: dict
    poster_id: Optional[int]


@dataclass
class ThreadsFeed:
    items: List[Thread] = field(default_factory=list)
    next_cursor: Optional[int] = None


@dataclass
class ThreadPostsPage(PaginationPage[Post]):
    pass
