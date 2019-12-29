from dataclasses import dataclass

from .pagination import PaginationPage
from .post import Post


@dataclass
class ThreadPostsPage(PaginationPage[Post]):
    pass
