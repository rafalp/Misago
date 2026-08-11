from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING, Iterable

from django.contrib.auth import get_user_model

from ..categories.models import Category
from ..permissions.proxy import UserPermissionsProxy
from ..threads.models import Post, Thread
from .enums import SearchMode, SearchOrder

if TYPE_CHECKING:
    from ..users.models import User


class SearchBackend(ABC):
    def __init__(self, options: dict):
        pass

    def initialize(self):
        pass

    @abstractmethod
    def search_posts(
        self,
        query: str,
        mode: SearchMode,
        permissions: UserPermissionsProxy,
        *,
        categories: Iterable[Category] | None = None,
        threads: Iterable[Thread] | None = None,
        users: Iterable["User"] | None = None,
        posted_after: datetime | None = None,
        posted_before: datetime | None = None,
        order: SearchOrder = SearchOrder.RELEVANCE,
        offset: int = 0,
        limit: int = 50,
        **kwargs,
    ) -> dict:
        pass

    @abstractmethod
    def index_posts(self, posts: Iterable[Post]):
        pass

    @abstractmethod
    def move_category_posts(
        self, categories: Iterable[Category], new_category: Category
    ) -> int:
        pass

    @abstractmethod
    def move_thread_posts(self, threads: Iterable[Thread], new_thread: Thread) -> int:
        pass

    @abstractmethod
    def move_threads(self, threads: Iterable[Thread], new_category: Category) -> int:
        pass

    @abstractmethod
    def move_posts(self, posts: Iterable[Post], new_thread: Thread) -> int:
        pass

    @abstractmethod
    def delete_categories(self, categories: Iterable[Category]) -> int:
        pass

    @abstractmethod
    def delete_threads(self, threads: Iterable[Thread]) -> int:
        pass

    @abstractmethod
    def delete_posts(self, posts: Iterable[Post]) -> int:
        pass

    @abstractmethod
    def delete_users(self, users: Iterable["User"]) -> int:
        pass

    @abstractmethod
    def clear(self):
        pass


class PostgreSQLSearchBackend(SearchBackend):
    def search_posts(
        self,
        query: str,
        mode: SearchMode,
        permissions: UserPermissionsProxy,
        *,
        categories: list[Category] | None = None,
        threads: list[Thread] | None = None,
        users: list["User"] | None = None,
        posted_after: datetime | None = None,
        posted_before: datetime | None = None,
        order: SearchOrder = SearchOrder.RELEVANCE,
        offset: int = 0,
        limit: int = 50,
        **kwargs,
    ) -> dict:
        pass

    def index_posts(self, posts: Iterable[Post]):
        pass

    def move_category_posts(
        self, categories: Iterable[Category], new_category: Category
    ) -> int:
        pass

    def move_thread_posts(self, threads: Iterable[Thread], new_thread: Thread) -> int:
        pass

    def move_threads(self, threads: Iterable[Thread], new_category: Category) -> int:
        pass

    def move_posts(self, posts: Iterable[Post], new_thread: Thread) -> int:
        pass

    def delete_categories(self, categories: Iterable[Category]) -> int:
        pass

    def delete_threads(self, threads: Iterable[Thread]) -> int:
        pass

    def delete_posts(self, posts: Iterable[Post]) -> int:
        pass

    def delete_users(self, users: Iterable["User"]) -> int:
        pass

    def clear(self):
        pass
