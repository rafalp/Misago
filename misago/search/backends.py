from abc import ABC, abstractmethod
from datetime import datetime
from functools import reduce
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
from django.db.models import Max, OuterRef, Q, Value

from ..categories.models import Category
from ..permissions.proxy import UserPermissionsProxy
from ..threads.models import Post, Thread
from .enums import SearchOrder
from .models import PostSearch, ThreadSearch
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
    def search_thread_titles(
        self,
        query: str,
        permissions: UserPermissionsProxy,
        *,
        categories: list[Category] | None = None,
        threads: list[Thread] | None = None,
        users: list["User"] | None = None,
        started_after: datetime | None = None,
        started_before: datetime | None = None,
        order_by: SearchOrder = SearchOrder.RELEVANCE,
        offset: int = 0,
        limit: int = 50,
        **kwargs,
    ) -> PostSearchResults:
        pass

    @abstractmethod
    def search_threads(
        self,
        query: str,
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
    def search_posts(
        self,
        query: str,
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
    def index_threads(self, threads: Iterable[Thread]):
        pass

    @abstractmethod
    def index_posts(self, posts: Iterable[tuple[Post, str]]):
        pass

    @abstractmethod
    def update_category(
        self,
        new_category: Category,
        *,
        categories: Iterable[Category] | None = None,
        threads: Iterable[Thread] | None = None,
    ) -> int:
        pass

    @abstractmethod
    def update_thread(
        self,
        new_thread: Thread,
        *,
        threads: Iterable[Thread] | None = None,
        posts: Iterable[Post] | None = None,
    ) -> int:
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
    def clear(self):
        pass


class PostgreSQLSearchBackend(SearchBackend):
    name = "PostgreSQL full-text search"
    search_config: str
    min_rank: float | None

    def __init__(self, options: dict):
        self.search_config = options.get("PG_SEARCH_CONFIG", "simple")
        self.min_rank = options.get("PG_MIN_RANK")

    # Search operations

    def search_thread_titles(
        self,
        query: str,
        permissions: UserPermissionsProxy,
        *,
        categories: list[Category] | None = None,
        threads: list[Thread] | None = None,
        users: list["User"] | None = None,
        started_after: datetime | None = None,
        started_before: datetime | None = None,
        order_by: SearchOrder = SearchOrder.RELEVANCE,
        offset: int = 0,
        limit: int = 50,
        **kwargs,
    ) -> PostSearchResults:
        search_query = self._get_search_query(query)

        queryset = ThreadSearch.objects.filter(
            category_id__in=[category.id for category in categories],
            search_vector=search_query,
        ).annotate(
            headline=SearchHeadline(
                "title",
                query,
                start_sel="<b>",
                stop_sel="</b>",
            ),
        )

        if threads:
            queryset = queryset.filter(thread_id__in=[thread.it for thread in threads])
        if users:
            queryset = queryset.filter(starter_id__in=[user.it for user in users])
        if started_after:
            queryset = queryset.filter(started_at__gte=started_after)
        if started_before:
            queryset = queryset.filter(started_at__lte=started_before)

        if order_by == SearchOrder.RELEVANCE or self.min_rank:
            queryset = queryset.annotate(
                rank=SearchRank("search_vector", search_query),
            )
        if self.min_rank is not None:
            queryset = queryset.filter(rank__gt=self.min_rank)

        if order_by == SearchOrder.RELEVANCE:
            queryset = queryset.order_by("-rank")
        else:
            queryset = queryset.order_by("-thread_id")

        queryset = queryset[offset : offset + limit + 1]

        start_time = time()

        threads = list(queryset)
        threads, has_more = threads[:limit], threads[limit:]

        if not threads:
            return PostSearchResults(
                results=[],
                offset=offset,
                limit=limit,
                count=0,
                has_more=bool(has_more),
                time=time() - start_time,
            )

        posts_queryset = PostSearch.objects.filter(
            thread_id__in=[thread.thread_id for thread in threads],
            is_first_post=True,
        ).annotate(
            headline=SearchHeadline(
                "content",
                query,
                start_sel="<b>",
                stop_sel="</b>",
            ),
        )
        posts = {post.thread_id: post for post in posts_queryset}

        total_time = time() - start_time

        final_results: list[PostSearchResult] = []
        for thread in threads:
            post = posts.get(thread.thread_id)
            if not post:
                continue

            final_results.append(
                PostSearchResult(
                    post_id=post.post_id,
                    thread_title=thread.headline,
                    post_content=post.headline,
                    rank=getattr(thread, "rank"),
                )
            )

        return PostSearchResults(
            results=final_results,
            offset=offset,
            limit=limit,
            count=min(len(posts), limit),
            has_more=bool(has_more),
            time=total_time,
        )

    def search_threads(
        self,
        query: str,
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
        search_query = self._get_search_query(query)

        queryset = self._filter_categories(PostSearch.objects, permissions, categories)

        if threads:
            queryset = queryset.filter(thread_id__in=[thread.it for thread in threads])
        if users:
            queryset = queryset.filter(poster_id__in=[user.it for user in users])
        if posted_after:
            queryset = queryset.filter(posted_at__gte=posted_after)
        if posted_before:
            queryset = queryset.filter(posted_at__lte=posted_before)

        queryset = queryset.filter(
            thread_search_vector=search_query,
        ).annotate(
            rank=SearchRank("thread_search_vector", search_query),
        )

        start_time = time()

        thread_ids = list(
            queryset.values("thread_id")
            .annotate(rank=Max("rank"))
            .order_by("-rank", "-thread_id")
            .values_list("thread_id", flat=True)[offset : offset + limit + 1]
        )

        posts = list(
            queryset.filter(thread_id__in=thread_ids)
            .order_by("thread_id", "-rank", "-post_id")
            .annotate(
                content_headline=SearchHeadline(
                    "content",
                    query,
                    start_sel="<b>",
                    stop_sel="</b>",
                ),
            )
            .distinct("thread_id")
        )

        posts, has_more = posts[:limit], posts[limit:]

        if not posts:
            return PostSearchResults(
                results=[],
                offset=offset,
                limit=limit,
                count=0,
                has_more=bool(has_more),
                time=time() - start_time,
            )

        posts = {post.thread_id: post for post in posts}

        results = []
        for thread_id in thread_ids:
            if post := posts.get(thread_id):
                results.append(post)

        headlines = self._get_thread_headlines(
            query, [result.thread_id for result in results]
        )

        total_time = time() - start_time

        return PostSearchResults(
            results=[
                PostSearchResult(
                    post_id=result.post_id,
                    thread_title=headlines.get(result.thread_id, "MISSING"),
                    post_content=result.content_headline,
                    rank=getattr(result, "rank"),
                )
                for result in results
            ],
            offset=offset,
            limit=limit,
            count=min(len(results), limit),
            has_more=bool(has_more),
            time=total_time,
        )

    def search_posts(
        self,
        query: str,
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
        search_query = self._get_search_query(query)

        queryset = self._filter_categories(PostSearch.objects, permissions, categories)

        if threads:
            queryset = queryset.filter(thread_id__in=[thread.it for thread in threads])
        if users:
            queryset = queryset.filter(poster_id__in=[user.it for user in users])
        if posted_after:
            queryset = queryset.filter(posted_at__gte=posted_after)
        if posted_before:
            queryset = queryset.filter(posted_at__lte=posted_before)

        queryset = queryset.filter(
            post_search_vector=search_query,
        ).annotate(
            content_headline=SearchHeadline(
                "content",
                query,
                start_sel="<b>",
                stop_sel="</b>",
            ),
        )

        if order_by == SearchOrder.RELEVANCE or self.min_rank:
            queryset = queryset.annotate(
                rank=SearchRank("post_search_vector", search_query),
            )
        if self.min_rank is not None:
            queryset = queryset.filter(rank__gt=self.min_rank)

        if order_by == SearchOrder.RELEVANCE:
            queryset = queryset.order_by("-rank")
        else:
            queryset = queryset.order_by("-post_id")

        queryset = queryset[offset : offset + limit + 1]

        start_time = time()

        results = list(queryset)
        results, has_more = results[:limit], results[limit:]

        if not results:
            return PostSearchResults(
                results=[],
                offset=offset,
                limit=limit,
                count=0,
                has_more=bool(has_more),
                time=time() - start_time,
            )

        headlines = self._get_thread_headlines(
            query, [result.thread_id for result in results]
        )

        total_time = time() - start_time

        return PostSearchResults(
            results=[
                PostSearchResult(
                    post_id=result.post_id,
                    thread_title=headlines.get(result.thread_id, "MISSING"),
                    post_content=result.content_headline,
                    rank=getattr(result, "rank"),
                )
                for result in results
            ],
            offset=offset,
            limit=limit,
            count=min(len(results), limit),
            has_more=bool(has_more),
            time=total_time,
        )

    def _get_search_query(self, query: str) -> SearchQuery:
        return SearchQuery(query, config=self.search_config)

    def _filter_categories(
        self, queryset, permissions: UserPermissionsProxy, categories: list[Category]
    ):
        all_posts = []
        visible_or_owned = []
        visible_only = []

        for category in categories:
            if permissions.is_category_moderator(category.id):
                all_posts.append(category.id)
            elif permissions.user.is_authenticated:
                visible_or_owned.append(category.id)
            else:
                visible_only.append(category.id)

        expressions = []
        if all_posts:
            expressions.append(Q(category_id__in=all_posts))
        if visible_or_owned:
            expressions.append(
                Q(category_id__in=visible_or_owned, is_hidden=False)
                & (Q(is_unapproved=False) | Q(poster_id=permissions.user.id))
            )
        if visible_only:
            expressions.append(
                Q(
                    category_id__in=visible_or_owned,
                    is_hidden=False,
                    is_unapproved=False,
                )
            )

        if not expressions:
            return queryset.empty()

        return queryset.filter(reduce(lambda l, r: l | r, expressions))

    def _get_thread_headlines(
        self, query: SearchQuery, thread_ids: Iterable[int]
    ) -> dict[int, str]:
        queryset = ThreadSearch.objects.filter(thread_id__in=thread_ids).annotate(
            headline=SearchHeadline(
                "title",
                query,
                start_sel="<b>",
                stop_sel="</b>",
            ),
        )

        return {result.thread_id: result.headline for result in queryset}

    # Indexing operations

    def index_threads(self, threads: Iterable[Thread]):
        for batch in batched(threads, 50):
            self._index_threads_batch(batch)

    @transaction.atomic
    def _index_threads_batch(self, threads: Iterable[Thread]):
        ThreadSearch.objects.filter(
            thread_id__in=[thread.id for thread in threads]
        ).delete()
        ThreadSearch.objects.bulk_create(
            [
                ThreadSearch(
                    category_id=thread.category_id,
                    thread_id=thread.id,
                    starter_id=thread.starter_id,
                    title=escape(thread.title),
                    search_vector=(
                        SearchVector(
                            Value(thread.title),
                            config=self.search_config,
                            weight="B",
                        )
                    ),
                    started_at=thread.started_at,
                    is_pinned=bool(thread.pinned),
                )
                for thread in threads
            ]
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

        if post.id == thread.first_post_id:
            is_thread_pinned = bool(post.thread.pinned)
            is_first_post = True
        else:
            is_thread_pinned = False
            is_first_post = False

        return PostSearch(
            category_id=post.category_id,
            thread_id=post.thread_id,
            post_id=post.id,
            poster_id=post.poster_id,
            content=escape(search_document),
            post_search_vector=(
                SearchVector(
                    Value(search_document),
                    config=self.search_config,
                )
            ),
            thread_search_vector=(
                SearchVector(
                    Value(thread.title),
                    config=self.search_config,
                    weight="A",
                )
                + SearchVector(
                    Value(search_document),
                    config=self.search_config,
                    weight="B",
                )
            ),
            posted_at=post.posted_at,
            is_thread_pinned=is_thread_pinned,
            incoming_links=0,
            is_first_post=is_first_post,
            is_hidden=post.is_hidden,
            is_unapproved=post.is_unapproved,
        )

    # Update operation

    def update_category(
        self,
        new_category: Category,
        *,
        categories: Iterable[Category] | None = None,
        threads: Iterable[Thread] | None = None,
    ) -> int:
        filters = {}
        if categories:
            filters["category_id__in"] = [category.id for category in categories]
        if threads:
            filters["thread_id__in"] = [thread.id for thread in threads]

        updated = ThreadSearch.objects.filter(**filters).update(
            category_id=new_category.id
        )
        updated += PostSearch.objects.filter(**filters).update(
            category_id=new_category.id
        )

        return updated

    def update_thread(
        self,
        new_thread: Thread,
        *,
        threads: Iterable[Thread] | None = None,
        posts: Iterable[Post] | None = None,
    ) -> int:
        filters = {}
        if threads:
            filters["thread_id__in"] = [thread.id for thread in threads]
        if posts:
            filters["post_id__in"] = [post.id for post in posts]

        return PostSearch.objects.filter(**filters).update(
            category_id=new_thread.category_id,
            thread_id=new_thread.id,
        )

    # Delete operations

    def delete_categories(self, categories: Iterable[Category]) -> int:
        filters = {"category_id__in": [category.id for category in categories]}

        deleted_threads, _ = ThreadSearch.objects.filter(**filters).delete()
        deleted_posts, _ = PostSearch.objects.filter(**filters).delete()

        return deleted_threads + deleted_posts

    def delete_threads(self, threads: Iterable[Thread]) -> int:
        filters = {"thread_id__in": [thread.id for thread in threads]}

        deleted_threads, _ = ThreadSearch.objects.filter(**filters).delete()
        deleted_posts, _ = PostSearch.objects.filter(**filters).delete()

        return deleted_threads + deleted_posts

    def delete_posts(self, posts: Iterable[Post]) -> int:
        deleted_posts, _ = PostSearch.objects.filter(
            post_id__in=[post.id for post in posts],
        ).delete()

        return deleted_posts

    def clear(self):
        ThreadSearch.objects.all().delete()
        PostSearch.objects.all().delete()
