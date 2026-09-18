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
from .types import ThreadsSearchResult

if TYPE_CHECKING:
    from ..users.models import User


class Search:
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
        return self.backend.index_threads([thread])

    def bulk_index_threads(self, threads: Iterable[Thread]):
        return self.backend.index_threads(threads)

    def index_post(self, post: Post, search_document: str):
        return self.backend.index_posts([(post, search_document)])

    def bulk_index_posts(self, posts: Iterable[tuple[Post, str]]):
        return self.backend.index_posts(posts)

    def bulk_move_categories(
        self, categories: Category | Iterable[Category], new_category: Category
    ):
        if isinstance(categories, Category):
            categories = [categories]

        return self.backend.move_categories(categories, new_category)

    def bulk_move_thread_posts(
        self, threads: Thread | Iterable[Thread], new_thread: Thread
    ):
        if isinstance(threads, Thread):
            threads = [threads]

        return self.backend.move_thread_posts(threads, new_thread)

    def bulk_move_threads(
        self, threads: Thread | Iterable[Thread], new_category: Category
    ):
        if isinstance(threads, Thread):
            threads = [threads]

        return self.backend.move_threads(threads, new_category)

    def bulk_move_posts(self, posts: Post | Iterable[Post], new_thread: Thread):
        if isinstance(posts, Post):
            posts = [posts]

        return self.backend.move_posts(posts, new_thread)

    def update_thread_first_post(self, thread: Thread):
        return self.backend.update_thread_first_post(thread)

    def update_thread_title(self, thread: Thread):
        return self.backend.update_thread_title(thread)

    def update_thread_members(self, thread: Thread, members: Iterable[int]):
        return self.backend.update_thread_members(thread, members)

    def update_thread(
        self,
        thread: Thread,
        *,
        is_hidden: bool | None = None,
        is_unapproved: bool | None = None,
        **kwargs,
    ):
        return self.backend.update_threads(
            [thread],
            is_hidden=is_hidden,
            is_unapproved=is_unapproved,
            **kwargs,
        )

    def bulk_update_threads(
        self,
        threads: Iterable[Thread],
        *,
        is_hidden: bool | None = None,
        is_unapproved: bool | None = None,
        **kwargs,
    ):
        return self.backend.update_threads(
            threads,
            is_hidden=is_hidden,
            is_unapproved=is_unapproved,
            **kwargs,
        )

    def update_post(
        self,
        post: Post,
        *,
        is_hidden: bool | None = None,
        is_unapproved: bool | None = None,
        **kwargs,
    ):
        return self.backend.update_posts(
            [post],
            is_hidden=is_hidden,
            is_unapproved=is_unapproved,
            **kwargs,
        )

    def bulk_update_posts(
        self,
        posts: Iterable[Post],
        *,
        is_hidden: bool | None = None,
        is_unapproved: bool | None = None,
        **kwargs,
    ):
        return self.backend.update_posts(
            posts,
            is_hidden=is_hidden,
            is_unapproved=is_unapproved,
            **kwargs,
        )

    def delete_category(self, category: Category):
        return self.backend.delete_categories([category])

    def bulk_delete_categories(self, categories: Iterable[Category]):
        return self.backend.delete_categories(categories)

    def delete_thread(self, thread: Thread):
        return self.backend.delete_threads([thread])

    def bulk_delete_threads(self, threads: Iterable[Thread]):
        return self.backend.delete_threads(threads)

    def delete_post(self, post: Post):
        return self.backend.delete_posts([post])

    def bulk_delete_posts(self, posts: Iterable[Post]):
        return self.backend.delete_posts(posts)

    def delete_user(self, user: "User"):
        return self.backend.delete_users([user])

    def bulk_delete_users(self, users: Iterable["User"]):
        return self.backend.delete_users(users)

    def clear(self):
        return self.backend.clear()


search = Search(settings.MISAGO_SEARCH)
