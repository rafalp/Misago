from abc import ABC, abstractmethod
from datetime import datetime
from html import escape
from itertools import batched
from time import time
from typing import TYPE_CHECKING, Iterable, TypedDict

from django.conf import settings
from django.contrib.postgres.search import (
    SearchHeadline,
    SearchQuery,
    SearchRank,
    SearchVector,
)
from django.db import transaction
from django.db.models import F, Max, QuerySet, Value

from ..categories.models import Category
from ..categories.proxy import CategoryProxy
from ..permissions.privatethreads import (
    filter_private_threads_posts_queryset,
    filter_private_threads_queryset,
)
from ..permissions.proxy import UserPermissionsProxy
from ..permissions.threads import filter_threads_posts_queryset, filter_threads_queryset
from ..threads.models import Post, Thread
from .enums import SearchMode, SearchSort
from .models import PostSearch, ThreadSearch
from .types import ThreadsSearchResult, ThreadsSearchResultItem

if TYPE_CHECKING:
    from ..users.models import User


class ThreadsSearchUpdate(TypedDict, total=False):
    category: Category
    starter: "User"

    is_hidden: bool
    is_unapproved: bool


class PostsSearchUpdate(TypedDict, total=False):
    category: Category
    category_id: int
    thread: Thread
    thread_id: int
    poster: "User | None"
    poster_id: int | None

    is_hidden: bool
    is_unapproved: bool


class SearchBackend(ABC):
    name: str

    def __init__(self, options: dict):
        pass

    def initialize(self):
        pass

    @abstractmethod
    def search_threads(
        self,
        query: str,
        permissions: UserPermissionsProxy,
        categories: list[Category | CategoryProxy],
        threads: list[Thread] | None = None,
        users: list["User"] | None = None,
        after: datetime | None = None,
        before: datetime | None = None,
        mode: SearchMode = SearchMode.THREADS,
        order_by: SearchSort = SearchSort.RELEVANCE,
        offset: int = 0,
        limit: int = 50,
        **kwargs,
    ) -> ThreadsSearchResult:
        pass

    @abstractmethod
    def search_private_threads(
        self,
        query: str,
        permissions: UserPermissionsProxy,
        threads: list[Thread] | None = None,
        users: list["User"] | None = None,
        after: datetime | None = None,
        before: datetime | None = None,
        mode: SearchMode = SearchMode.THREADS,
        order_by: SearchSort = SearchSort.RELEVANCE,
        offset: int = 0,
        limit: int = 50,
        **kwargs,
    ) -> ThreadsSearchResult:
        pass

    @abstractmethod
    def index_threads(self, threads: Iterable[Thread]):
        pass

    @abstractmethod
    def index_posts(self, posts: Iterable[tuple[Post, str]]):
        pass

    @abstractmethod
    def update_thread_first_post(self, thread: Thread):
        pass

    @abstractmethod
    def update_thread_title(self, thread: Thread):
        pass

    @abstractmethod
    def update_thread_members(self, thread: Thread, members: Iterable[int]):
        pass

    @abstractmethod
    def update_threads(
        self,
        update: ThreadsSearchUpdate,
        *,
        categories: Iterable[Category | CategoryProxy] | None = None,
        threads: Iterable[Thread] | None = None,
        starters: Iterable["User"] | None = None,
    ):
        pass

    @abstractmethod
    def update_posts(
        self,
        update: PostsSearchUpdate,
        *,
        categories: Iterable[Category | CategoryProxy] | None = None,
        threads: Iterable[Thread] | None = None,
        posts: Iterable[Post] | None = None,
        posters: Iterable["User"] | None = None,
    ):
        pass

    @abstractmethod
    def delete(
        self,
        *,
        categories: Iterable[Category | CategoryProxy] | None = None,
        threads: Iterable[Thread] | None = None,
        posts: Iterable[Post] | None = None,
        users: Iterable["User"] | None = None,
    ):
        pass

    @abstractmethod
    def clear(self):
        pass


class PostgreSQLSearchBackend(SearchBackend):
    name = "PostgreSQL full-text search"
    search_config: str
    min_rank: float | None

    HEADLINE_START_SELECTION = "<hl>"
    HEADLINE_STOP_SELECTION = "</hl>"

    headline_min_words: int | None
    headline_max_words: int | None
    headline_max_fragments: int | None
    headline_short_word: int | None

    languages_configs = {
        "ar": "arabic",
        "hy": "armenian",
        "eu": "basque",
        "ca": "catalan",
        "da": "danish",
        "nl": "dutch",
        "en": "english",
        "fi": "finnish",
        "fr": "french",
        "de": "german",
        "el": "greek",
        "hi": "hindi",
        "hu": "hungarian",
        "id": "indonesian",
        "ga": "irish",
        "it": "italian",
        "lt": "lithuanian",
        "ne": "nepali",
        "nb": "norwegian",
        "pt": "portuguese",
        "ro": "romanian",
        "ru": "russian",
        "sr": "serbian",
        "es": "spanish",
        "sv": "swedish",
        "ta": "tamil",
        "tr": "turkish",
    }

    def __init__(self, options: dict):
        search_config = options.get("PG_SEARCH_CONFIG", "simple")
        if search_config == "auto":
            language, *_ = settings.LANGUAGE_CODE.replace("-", "_").partition("_")
            search_config = self.languages_configs.get(language, "simple")

        self.search_config = search_config
        self.min_rank = options.get("PG_MIN_RANK", 0.0001)

        self.headline_min_words = options.get("PG_HEADLINE_MIN_WORDS", 60)
        self.headline_max_words = options.get("PG_HEADLINE_MAX_WORDS", 61)
        self.headline_max_fragments = options.get("PG_HEADLINE_MAX_FRAGMENTS", 0)
        self.headline_short_word = options.get("PG_HEADLINE_SHORT_WORD")

    # Search operations

    def search_threads(
        self,
        query: str,
        permissions: UserPermissionsProxy,
        categories: list[Category | CategoryProxy],
        threads: list[Thread] | None = None,
        users: list["User"] | None = None,
        after: datetime | None = None,
        before: datetime | None = None,
        mode: SearchMode = SearchMode.THREADS,
        order_by: SearchSort = SearchSort.RELEVANCE,
        offset: int = 0,
        limit: int = 50,
        **kwargs,
    ) -> ThreadsSearchResult:
        if isinstance(threads, list):
            thread_ids = [thread.id for thread in threads]
        else:
            thread_ids = filter_threads_queryset(permissions, categories).values("id")

        common_kwargs = dict(
            users=users,
            after=after,
            before=before,
            order_by=order_by,
            offset=offset,
            limit=limit,
            **kwargs,
        )

        if mode == SearchMode.THREAD_TITLES:
            return self._search_thread_titles(query, thread_ids, **common_kwargs)

        post_ids = filter_threads_posts_queryset(permissions, categories).values("id")

        if mode == SearchMode.THREADS:
            return self._search_threads(query, thread_ids, post_ids, **common_kwargs)

        if mode == SearchMode.POSTS:
            return self._search_posts(query, thread_ids, post_ids, **common_kwargs)

    def search_private_threads(
        self,
        query: str,
        permissions: UserPermissionsProxy,
        threads: list[Thread] | None = None,
        users: list["User"] | None = None,
        after: datetime | None = None,
        before: datetime | None = None,
        mode: SearchMode = SearchMode.THREADS,
        order_by: SearchSort = SearchSort.RELEVANCE,
        offset: int = 0,
        limit: int = 50,
        **kwargs,
    ) -> ThreadsSearchResult:
        private_threads = Category.objects.private_threads()

        if isinstance(threads, list):
            thread_ids = [thread.id for thread in threads]
        else:
            thread_ids = filter_private_threads_queryset(
                permissions, private_threads.thread_set
            ).values("id")

        common_kwargs = dict(
            users=users,
            after=after,
            before=before,
            order_by=order_by,
            offset=offset,
            limit=limit,
            **kwargs,
        )

        if mode == SearchMode.THREAD_TITLES:
            return self._search_thread_titles(query, thread_ids, **common_kwargs)

        post_ids = filter_private_threads_posts_queryset(
            permissions, private_threads.post_set
        ).values("id")

        if mode == SearchMode.THREADS:
            return self._search_threads(query, thread_ids, post_ids, **common_kwargs)

        if mode == SearchMode.POSTS:
            return self._search_posts(query, thread_ids, post_ids, **common_kwargs)

    def _search_thread_titles(
        self,
        query: str,
        thread_ids: list[int] | QuerySet,
        users: list["User"] | None = None,
        after: datetime | None = None,
        before: datetime | None = None,
        order_by: SearchSort = SearchSort.RELEVANCE,
        offset: int = 0,
        limit: int = 50,
        **kwargs,
    ):
        search_query = self.parse_search_query(query)

        # Build search queryset
        queryset = ThreadSearch.objects.filter(
            thread_id__in=thread_ids,
            search_vector=search_query,
        ).annotate(
            headline=self._get_title_headline(query),
        )

        if users:
            queryset = queryset.filter(starter_id__in=[user.id for user in users])
        if after:
            queryset = queryset.filter(started_at__gte=after)
        if before:
            queryset = queryset.filter(started_at__lte=before)

        if order_by == SearchSort.RELEVANCE or self.min_rank:
            queryset = queryset.annotate(
                rank=SearchRank(F("search_vector"), search_query),
            )
        if self.min_rank is not None:
            queryset = queryset.filter(rank__gt=self.min_rank)

        if order_by == SearchSort.RELEVANCE:
            queryset = queryset.order_by("-rank")
        else:
            queryset = queryset.order_by("-thread_id")

        start_time = time()

        # Search threads
        threads = list(queryset[offset : offset + limit + 1])
        threads, has_more = threads[:limit], bool(threads[limit:])

        # Escape hatch for no results
        if not threads:
            return self._empty_threads_result(start_time)

        # Fetch posts
        posts_queryset = PostSearch.objects.filter(
            thread_id__in=[thread.thread_id for thread in threads],
            is_first_post=True,
        ).annotate(
            headline=self._get_content_headline(search_query),
        )
        posts = {post.thread_id: post for post in posts_queryset}

        total_time = time() - start_time

        items: list[ThreadsSearchResultItem] = []
        for thread in threads:
            post = posts.get(thread.thread_id)
            if not post:
                continue

            items.append(
                ThreadsSearchResultItem(
                    post_id=post.post_id,
                    thread_title=thread.headline,
                    post_content=post.headline,
                )
            )

        return ThreadsSearchResult(
            items=items,
            has_more=has_more,
            time=total_time,
        )

    def _search_threads(
        self,
        query: str,
        thread_ids: list[int] | QuerySet,
        post_ids: QuerySet,
        users: list["User"] | None = None,
        after: datetime | None = None,
        before: datetime | None = None,
        order_by: SearchSort = SearchSort.RELEVANCE,
        offset: int = 0,
        limit: int = 50,
        **kwargs,
    ) -> ThreadsSearchResult:
        search_query = self.parse_search_query(query)

        queryset = PostSearch.objects.filter(
            thread_search_vector=search_query,
            post_id__in=post_ids,
        )

        if users:
            queryset = queryset.filter(poster__in=users)
        if after:
            queryset = queryset.filter(posted_at__gte=after)
        if before:
            queryset = queryset.filter(posted_at__lte=before)

        # 1st query: search for matching threads
        threads_queryset = queryset
        filter_by_min_rank = self.min_rank

        if order_by == SearchSort.RELEVANCE or filter_by_min_rank:
            threads_queryset = threads_queryset.annotate(
                rank=SearchRank(F("thread_search_vector"), search_query),
            )

        if filter_by_min_rank:
            threads_queryset = threads_queryset.filter(rank__gt=self.min_rank)

        if order_by == SearchSort.RELEVANCE:
            aggregate_by = "rank"
        else:
            aggregate_by = "thread_id"

        start_time = time()

        result_threads_ids = list(
            threads_queryset.filter(
                thread_id__in=thread_ids,
                post_id__in=post_ids,
            )
            .values("thread_id")
            .annotate(ordering=Max(aggregate_by))
            .order_by("-ordering")
            .values_list("thread_id", flat=True)[offset : offset + limit + 1]
        )

        result_threads_ids, has_more = (
            result_threads_ids[:limit],
            bool(result_threads_ids[limit:]),
        )

        # 2nd query: pull oldest matching post per thread result
        posts = list(
            queryset.filter(
                thread_id__in=result_threads_ids,
            )
            .order_by("thread_id", "post_id")
            .annotate(headline=self._get_content_headline(search_query))
            .distinct("thread_id")
        )

        if not posts:
            return self._empty_threads_result(start_time)

        thread_posts = {post.thread_id: post for post in posts}
        thread_headlines = self._get_thread_headlines(search_query, thread_posts)

        # Sort posts by threads
        items = []
        for thread_id in result_threads_ids:
            if post := thread_posts.get(thread_id):
                items.append(
                    ThreadsSearchResultItem(
                        post_id=post.post_id,
                        thread_title=thread_headlines.get(thread_id, "MISSING"),
                        post_content=post.headline,
                    )
                )

        total_time = time() - start_time

        return ThreadsSearchResult(
            items=items,
            has_more=has_more,
            time=total_time,
        )

    def _search_posts(
        self,
        query: str,
        thread_ids: list[int] | QuerySet,
        post_ids: QuerySet,
        users: list["User"] | None = None,
        after: datetime | None = None,
        before: datetime | None = None,
        order_by: SearchSort = SearchSort.RELEVANCE,
        offset: int = 0,
        limit: int = 50,
        **kwargs,
    ) -> ThreadsSearchResult:
        search_query = self.parse_search_query(query)

        queryset = PostSearch.objects.filter(
            thread_id__in=thread_ids, post_id__in=post_ids
        )

        if users:
            queryset = queryset.filter(poster__in=users)
        if after:
            queryset = queryset.filter(posted_at__gte=after)
        if before:
            queryset = queryset.filter(posted_at__lte=before)

        queryset = queryset.filter(
            post_search_vector=search_query,
        ).annotate(
            headline=self._get_content_headline(search_query),
        )

        if order_by == SearchSort.RELEVANCE or self.min_rank:
            queryset = queryset.annotate(
                rank=SearchRank(F("post_search_vector"), search_query),
            )
        if self.min_rank is not None:
            queryset = queryset.filter(rank__gt=self.min_rank)

        if order_by == SearchSort.RELEVANCE:
            queryset = queryset.order_by("-rank")
        else:
            queryset = queryset.order_by("-post_id")

        queryset = queryset[offset : offset + limit + 1]

        start_time = time()

        results = list(queryset)
        results, has_more = results[:limit], bool(results[limit:])

        if not results:
            return self._empty_threads_result(start_time)

        thread_headlines = self._get_thread_headlines(
            query, [result.thread_id for result in results]
        )

        total_time = time() - start_time

        return ThreadsSearchResult(
            items=[
                ThreadsSearchResultItem(
                    post_id=result.post_id,
                    thread_title=thread_headlines.get(result.thread_id, "MISSING"),
                    post_content=result.headline,
                )
                for result in results
            ],
            has_more=has_more,
            time=total_time,
        )

    def parse_search_query(self, query: str) -> SearchQuery:
        if query.startswith('"') and query.endswith('"'):
            search_type = "phrase"
            query = query[1:-1].strip()
        else:
            search_type = "plain"

        return SearchQuery(query, config=self.search_config, search_type=search_type)

    def _empty_threads_result(self, start_time: float) -> ThreadsSearchResult:
        return ThreadsSearchResult(
            items=[],
            has_more=False,
            time=time() - start_time,
        )

    def _get_thread_headlines(
        self, query: SearchQuery, thread_ids: Iterable[int]
    ) -> dict[int, str]:
        queryset = ThreadSearch.objects.filter(thread_id__in=thread_ids).annotate(
            headline=self._get_title_headline(query),
        )

        return {result.thread_id: result.headline for result in queryset}

    def _get_title_headline(self, query: SearchQuery) -> SearchHeadline:
        return SearchHeadline(
            "title",
            query,
            start_sel=self.HEADLINE_START_SELECTION,
            stop_sel=self.HEADLINE_STOP_SELECTION,
            highlight_all=True,
        )

    def _get_content_headline(self, query: SearchQuery) -> SearchHeadline:
        return SearchHeadline(
            "content",
            query,
            start_sel=self.HEADLINE_START_SELECTION,
            stop_sel=self.HEADLINE_STOP_SELECTION,
            max_words=self.headline_max_words,
            min_words=self.headline_min_words,
            short_word=self.headline_short_word,
            max_fragments=self.headline_max_fragments,
        )

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
                        )
                    ),
                    started_at=thread.started_at,
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
            is_first_post = True
        else:
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
                    weight="B",
                )
                + SearchVector(
                    Value(search_document),
                    config=self.search_config,
                )
            ),
            posted_at=post.posted_at,
            is_first_post=is_first_post,
        )

    # Update operations

    def update_thread_first_post(self, thread: Thread) -> 0:
        first_post_id = thread.first_post_id

        updated_posts = (
            PostSearch.objects.filter(
                thread=thread,
                is_first_post=True,
            )
            .exclude(post_id=first_post_id)
            .update(is_first_post=False)
        )

        if updated_posts:
            return updated_posts + PostSearch.objects.filter(
                thread=thread, post_id=first_post_id
            ).update(is_first_post=True)

        return updated_posts

    def update_thread_title(self, thread: Thread) -> int:
        updated_count = ThreadSearch.objects.filter(thread=thread).update(
            title=escape(thread.title),
            search_vector=SearchVector(
                Value(thread.title),
                config=self.search_config,
            ),
        )

        updated_count += PostSearch.objects.filter(thread=thread).update(
            thread_search_vector=(
                SearchVector(
                    Value(thread.title),
                    config=self.search_config,
                    weight="A",
                )
                + SearchVector(
                    F("post_search_vector"),
                    config=self.search_config,
                    weight="A",
                )
            ),
        )

        return updated_count

    def update_thread_members(self, thread: Thread, members: Iterable[int]) -> int:
        return 0  # Not used

    _INDEXED_THREAD_FIELDS = {
        "category",
        "category_id",
        "starter",
        "starter_id",
    }

    def update_threads(
        self,
        update: ThreadsSearchUpdate,
        *,
        categories: Iterable[Category | CategoryProxy] | None = None,
        threads: Iterable[Thread] | None = None,
        starters: Iterable["User"] | None = None,
    ) -> int:
        if not any((categories, threads, starters)):
            raise ValueError("Provide at least one filter.")

        if "category" in update and "category_id" in update:
            raise ValueError(
                "'category' and 'category_id' can't be updated at the same time."
            )

        if "starter" in update and "starter_id" in update:
            raise ValueError(
                "'starter' and 'starter_id' can't be updated at the same time."
            )

        clean_update = {
            field: value
            for field, value in update.items()
            if field in self._INDEXED_THREAD_FIELDS
        }

        if not clean_update:
            return 0

        return self._threads(
            categories=categories,
            threads=threads,
            users=starters,
        ).update(**clean_update)

    _INDEXED_POST_FIELDS = {
        "category",
        "category_id",
        "thread",
        "thread_id",
        "poster",
        "poster_id",
    }

    def update_posts(
        self,
        update: PostsSearchUpdate,
        *,
        categories: Iterable[Category | CategoryProxy] | None = None,
        threads: Iterable[Thread] | None = None,
        posts: Iterable[Post] | None = None,
        posters: Iterable["User"] | None = None,
    ) -> int:
        if not any((categories, threads, posts, posters)):
            raise ValueError("Provide at least one filter.")

        if "category" in update and "category_id" in update:
            raise ValueError(
                "'category' and 'category_id' can't be updated at the same time."
            )

        if "thread" in update and "thread_id" in update:
            raise ValueError(
                "'thread' and 'thread_id' can't be updated at the same time."
            )

        if "poster" in update and "poster_id" in update:
            raise ValueError(
                "'poster' and 'poster_id' can't be updated at the same time."
            )

        clean_update = {
            field: value
            for field, value in update.items()
            if field in self._INDEXED_POST_FIELDS
        }

        if not clean_update:
            return 0

        return self._posts(
            categories=categories,
            threads=threads,
            posts=posts,
            users=posters,
        ).update(**clean_update)

    def delete(
        self,
        *,
        categories: Iterable[Category | CategoryProxy] | None = None,
        threads: Iterable[Thread] | None = None,
        posts: Iterable[Post] | None = None,
        users: Iterable["User"] | None = None,
    ) -> int:
        if not any((categories, threads, posts, users)):
            raise ValueError("Provide at least one filter.")

        deleted_total = 0

        if any((categories, threads, users)):
            deleted_threads, _ = self._threads(
                categories=categories,
                threads=threads,
                users=users,
            ).delete()

            deleted_total += deleted_threads

        deleted_posts, _ = self._posts(
            categories=categories,
            threads=threads,
            posts=posts,
            users=users,
        ).delete()

        return deleted_total + deleted_posts

    def _threads(
        self,
        *,
        categories: Iterable[Category | CategoryProxy] | None = None,
        threads: Iterable[Thread] | None = None,
        users: Iterable["User"] | None = None,
    ) -> QuerySet:
        filters = {}

        if categories:
            category_ids = [category.id for category in categories]
            filters["category_id__in"] = category_ids
        if threads:
            filters["thread__in"] = threads
        if users:
            filters["starter__in"] = users

        return ThreadSearch.objects.filter(**filters)

    def _posts(
        self,
        *,
        categories: Iterable[Category | CategoryProxy] | None = None,
        threads: Iterable[Thread] | None = None,
        posts: Iterable[Post] | None = None,
        users: Iterable["User"] | None = None,
    ) -> QuerySet:
        filters = {}

        if categories:
            category_ids = [category.id for category in categories]
            filters["category_id__in"] = category_ids
        if threads:
            filters["thread__in"] = threads
        if posts:
            filters["post__in"] = posts
        if users:
            filters["poster__in"] = users

        return PostSearch.objects.filter(**filters)

    def clear(self):
        ThreadSearch.objects.all().delete()
        PostSearch.objects.all().delete()
