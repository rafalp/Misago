from datetime import datetime
from typing import TYPE_CHECKING, Iterable

from django.conf import settings
from django.utils.module_loading import import_string

from ..categories.models import Category
from ..categories.proxy import CategoryProxy
from ..permissions.proxy import UserPermissionsProxy
from ..threads.models import Post, Thread
from .backends import SearchBackend
from .enums import SearchMode, SearchSort
from .query import SearchQuery
from .types import ThreadsSearchResult

if TYPE_CHECKING:
    from ..users.models import User


class SearchService:
    backend: SearchBackend

    def __init__(self, options: dict):
        if not isinstance(options, dict):
            raise TypeError("MISAGO_SEARCH must be a dictionary")

        try:
            backend_name = options["BACKEND"]
        except KeyError:
            raise ValueError("MISAGO_SEARCH is missing the 'BACKEND' option")

        try:
            backend_class = import_string(backend_name)
        except ImportError as exc:
            raise ValueError(
                f"Could not import '{backend_name}' search backend"
            ) from exc

        self.backend = backend_class(options)

    def initialize(self):
        return self.backend.initialize()

    def search_threads(
        self,
        query: SearchQuery,
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
        return self.backend.search_threads(
            query,
            permissions,
            categories,
            threads=threads,
            users=users,
            after=after,
            before=before,
            mode=mode,
            order_by=order_by,
            offset=offset,
            limit=limit,
            **kwargs,
        )

    def search_private_threads(
        self,
        query: SearchQuery,
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
        return self.backend.search_private_threads(
            query,
            permissions,
            threads=threads,
            users=users,
            after=after,
            before=before,
            mode=mode,
            order_by=order_by,
            offset=offset,
            limit=limit,
            **kwargs,
        )

    def index_thread(self, thread: Thread):
        return self.bulk_index_threads([thread])

    def bulk_index_threads(self, threads: Iterable[Thread]):
        return self.backend.index_threads(threads)

    def index_post(self, post: Post, search_document: str):
        return self.bulk_index_posts([(post, search_document)])

    def bulk_index_posts(self, posts: Iterable[tuple[Post, str]]):
        return self.backend.index_posts(posts)

    def update_thread_members(self, thread: Thread, members: Iterable[int]):
        return self.backend.update_thread_members(thread, members)

    def move_category_data(
        self, category: Category | CategoryProxy, new_category: Category | CategoryProxy
    ):
        return self.bulk_move_categories_data([category], new_category)

    def bulk_move_categories_data(
        self,
        categories: Iterable[Category | CategoryProxy],
        new_category: Category | CategoryProxy,
    ):
        return (
            self.backend.update_threads(
                {"category": new_category},
                categories=categories,
            ),
            self.backend.update_posts(
                {"category": new_category},
                categories=categories,
            ),
        )

    def delete_category_data(self, category: Category | CategoryProxy):
        return self.bulk_delete_categories_data([category])

    def bulk_delete_categories_data(
        self, categories: Iterable[Category | CategoryProxy]
    ):
        return self.backend.delete(categories=categories)

    def clear(self):
        return self.backend.clear()


search = SearchService(settings.MISAGO_SEARCH)
