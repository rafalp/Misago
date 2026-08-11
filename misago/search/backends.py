from abc import ABC, abstractmethod
from datetime import datetime
from html import escape
from itertools import batched
from time import time
from typing import TYPE_CHECKING, Iterable

from django.contrib.postgres.search import (
    SearchHeadline,
    SearchQuery,
    SearchRank,
    SearchVector,
)
from django.db import transaction
from django.db.models import Q, Value

from ..categories.models import Category
from ..permissions.proxy import UserPermissionsProxy
from ..threads.models import Post, Thread
from .enums import SearchMode, SearchOrder
from .models import PostSearch
from .types import PostSearchResult, PostSearchResults

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
        order_by: SearchOrder = SearchOrder.RELEVANCE,
        offset: int = 0,
        limit: int = 50,
        **kwargs,
    ) -> PostSearchResults:
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
    min_rank: float | None

    def __init__(self, options: dict):
        self.search_config = options.get("PG_SEARCH_CONFIG", "simple")
        self.min_rank = options.get("PG_MIN_RANK")

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
        order_by: SearchOrder = SearchOrder.RELEVANCE,
        offset: int = 0,
        limit: int = 50,
        **kwargs,
    ) -> PostSearchResults:
        search_query = SearchQuery(query, config=self.search_config)

        queryset = PostSearch.objects
        # queryset.filter(category_id__in=[category.id for category in categories])

        queryset = queryset.filter(
            search_vector=search_query,
        ).annotate(
            rank=SearchRank("search_vector", search_query),
            thread_title_headline=SearchHeadline(
                "thread_title",
                query,
                start_sel="<b>",
                stop_sel="</b>",
            ),
            post_content_headline=SearchHeadline(
                "post_content",
                query,
                start_sel="<b>",
                stop_sel="</b>",
            ),
        )

        if self.min_rank is not None:
            queryset = queryset.filter(rank__gt=self.min_rank)

        if order_by == SearchOrder.RELEVANCE:
            queryset = queryset.order_by("rank")
        elif order_by == SearchOrder.NEWEST:
            queryset = queryset.order_by("-posted_at")

        queryset = queryset[offset : offset + limit + 1]

        start_time = time()
        results = list(queryset)
        total_time = time() - start_time

        return PostSearchResults(
            results=[
                PostSearchResult(
                    post_id=result.post_id,
                    thread_title=result.thread_title_headline,
                    post_content=result.post_content_headline,
                    rank=getattr(result, "rank"),
                )
                for result in results[:limit]
            ],
            offset=offset,
            limit=limit,
            count=min(len(results), limit),
            has_more=len(results) > limit,
            time=total_time,
        )

    def index_posts(self, posts: Iterable[tuple[Post, str]]):
        for batch in batched(posts, 50):
            self._index_posts_batch(batch)

    @transaction.atomic
    def _index_posts_batch(self, posts: Iterable[tuple[Post, str]]):
        PostSearch.objects.filter(post_id__in=[post.id for post, _ in posts]).delete()
        PostSearch.objects.bulk_create(
            [
                self._create_post_search(post, search_document)
                for post, search_document in posts
            ]
        )

    def _create_post_search(self, post: Post, search_document: str) -> PostSearch:
        thread = post.thread

        search_vector = SearchVector(
            Value(search_document),
            config=self.search_config,
            weight="B",
        )

        if post.id == thread.first_post_id:
            thread_title = thread.title
            search_vector = (
                SearchVector(
                    Value(thread_title),
                    config=self.search_config,
                    weight="A",
                )
                + search_vector
            )

            is_thread_pinned = bool(post.thread.pinned)

        else:
            thread_title = None
            is_thread_pinned = False

        return PostSearch(
            category_id=post.category_id,
            thread_id=post.thread_id,
            post_id=post.id,
            poster_id=post.poster_id,
            thread_title=escape(thread_title) if thread_title else None,
            post_content=escape(search_document),
            search_vector=search_vector,
            posted_at=post.posted_at,
            is_thread_pinned=is_thread_pinned,
            incoming_links=0,
            is_hidden=post.is_hidden,
            is_unapproved=post.is_unapproved,
        )

    def move_category_posts(
        self, categories: Iterable[Category], new_category: Category
    ) -> int:
        PostSearch.objects.filter(
            category_id__in=[category.id for category in categories],
        ).update(category_id=new_category.id)

    def move_thread_posts(self, threads: Iterable[Thread], new_thread: Thread) -> int:
        PostSearch.objects.filter(
            thread_id__in=[thread.id for thread in threads],
        ).update(
            category_id=new_thread.category_id,
            thread_id=new_thread.id,
        )

    def move_threads(self, threads: Iterable[Thread], new_category: Category) -> int:
        PostSearch.objects.filter(
            thread_id__in=[thread.id for thread in threads],
        ).update(category_id=new_category.id)

    def move_posts(self, posts: Iterable[Post], new_thread: Thread) -> int:
        PostSearch.objects.filter(
            post_id__in=[post.id for post in posts],
        ).update(
            category_id=new_thread.category_id,
            thread_id=new_thread.id,
        )

    def delete_categories(self, categories: Iterable[Category]) -> int:
        PostSearch.objects.filter(
            category_id__in=[category.id for category in categories],
        ).delete()

    def delete_threads(self, threads: Iterable[Thread]) -> int:
        PostSearch.objects.filter(
            thread_id__in=[thread.id for thread in threads],
        ).delete()

    def delete_posts(self, posts: Iterable[Post]) -> int:
        PostSearch.objects.filter(
            post_id__in=[post.id for post in posts],
        ).delete()

    def delete_users(self, users: Iterable["User"]) -> int:
        PostSearch.objects.filter(
            poster_id__in=[user.id for user in users],
        ).delete()

    def clear(self):
        PostSearch.objects.all().delete()
