from abc import ABC, abstractmethod
from datetime import datetime
from itertools import batched
from typing import TYPE_CHECKING, Iterable

from django.contrib.postgres.search import SearchVector
from django.db import transaction
from django.db.models import Value

from ..categories.models import Category
from ..permissions.proxy import UserPermissionsProxy
from ..threads.models import Post, Thread
from .enums import SearchMode, SearchOrder
from .models import PostSearch

if TYPE_CHECKING:
    from ..users.models import User


class SearchBackend(ABC):
    name: str

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
    def index_posts(self, posts: Iterable[tuple[Post, str]]):
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
    name = "PostgreSQL full-text search"
    search_config: str

    def __init__(self, options: dict):
        self.search_config = options.get("PG_SEARCH_CONFIG", "simple")

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

    @transaction.atomic
    def index_posts(self, posts: Iterable[tuple[Post, str]]):
        for batch in batched(posts, 50):
            for post, _ in batch:
                print(post.id, post.thread.first_post_id)

            PostSearch.objects.filter(post_id__in=[post.id for post, _ in batch])
            PostSearch.objects.bulk_create(
                [
                    PostSearch(
                        category_id=post.category_id,
                        thread_id=post.thread_id,
                        post_id=post.id,
                        poster_id=post.poster_id,
                        thread_title=(
                            SearchVector(
                                Value(post.thread.title),
                                config=self.search_config,
                                weight="A",
                            )
                            if post.id == post.thread.first_post_id
                            else None
                        ),
                        post_content=SearchVector(
                            Value(search_document),
                            config=self.search_config,
                            weight="B",
                        ),
                        posted_at=post.posted_at,
                        is_thread_pinned=bool(
                            post.id == post.thread.first_post_id and post.thread.pinned
                        ),
                        incoming_links=0,
                        is_hidden=post.is_hidden,
                        is_unapproved=post.is_unapproved,
                    )
                    for post, search_document in batch
                ]
            )

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
