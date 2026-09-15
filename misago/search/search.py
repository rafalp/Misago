from datetime import datetime
from typing import TYPE_CHECKING, Iterable

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.module_loading import import_string

from ..categories.models import Category
from ..categories.proxy import CategoryProxy
from ..permissions.proxy import UserPermissionsProxy
from ..threads.models import Post, Thread
from .backends import SearchBackend
from .enums import SearchMode, SearchSort
from .types import ThreadsSearchResults

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
        categories: list[Category | CategoryProxy] | None = None,
        threads: list[Thread] | None = None,
        users: list["User"] | None = None,
        after: datetime | None = None,
        before: datetime | None = None,
        mode: SearchMode = SearchMode.THREADS,
        order_by: SearchSort = SearchSort.RELEVANCE,
        offset: int = 0,
        limit: int = 50,
        **kwargs,
    ) -> ThreadsSearchResults:
        return self.backend.search_threads(
            query=query,
            permissions=permissions,
            categories=categories,
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
    ) -> ThreadsSearchResults:
        return self.backend.search_private_threads(
            query=query,
            permissions=permissions,
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

    def index_threads(self, threads: Iterable[Thread]):
        return self.backend.index_threads(threads)

    def index_post(self, post: Post, search_document: str):
        return self.backend.index_posts([(post, search_document)])

    def index_posts(self, posts: Iterable[tuple[Post, str]]):
        return self.backend.index_posts(posts)

    def move_category_posts(
        self, categories: Category | Iterable[Category], new_category: Category
    ):
        if isinstance(categories, Category):
            categories = [categories]

        return self.backend.move_category_posts(categories, new_category)

    def move_thread_posts(self, threads: Thread | Iterable[Thread], new_thread: Thread):
        if isinstance(threads, Thread):
            threads = [threads]

        return self.backend.move_thread_posts(threads, new_thread)

    def move_threads(self, threads: Thread | Iterable[Thread], new_category: Category):
        if isinstance(threads, Thread):
            threads = [threads]

        return self.backend.move_threads(threads, new_category)

    def move_posts(self, posts: Post | Iterable[Post], new_thread: Thread):
        if isinstance(posts, Post):
            posts = [posts]

        return self.backend.move_posts(posts, new_thread)

    def update_thread_title(self, thread: Thread):
        return self.backend.update_thread_title(thread)

    def update_thread_members(self, thread: Thread, members: Iterable[int]):
        return self.backend.update_thread_members(thread, members)

    def update_threads(
        self,
        threads: Thread | Iterable[Thread],
        *,
        is_hidden: bool | None = None,
        is_unapproved: bool | None = None,
        **kwargs,
    ):
        if isinstance(threads, Thread):
            threads = [threads]

        return self.backend.update_threads(
            threads,
            is_hidden=is_hidden,
            is_unapproved=is_unapproved,
            **kwargs,
        )

    def update_posts(
        self,
        posts: Post | Iterable[Post],
        *,
        is_hidden: bool | None = None,
        is_unapproved: bool | None = None,
        **kwargs,
    ):
        if isinstance(posts, Post):
            posts = [posts]

        return self.backend.update_posts(
            posts,
            is_hidden=is_hidden,
            is_unapproved=is_unapproved,
            **kwargs,
        )

    def delete_categories(self, categories: Category | Iterable[Category]):
        if isinstance(categories, Category):
            categories = [categories]

        return self.backend.delete_categories(categories)

    def delete_threads(self, threads: Thread | Iterable[Thread]):
        if isinstance(threads, Thread):
            threads = [threads]

        return self.backend.delete_threads(threads)

    def delete_posts(self, posts: Post | Iterable[Post]):
        if isinstance(posts, Post):
            posts = [posts]

        return self.backend.delete_posts(posts)

    def delete_users(self, users: "User | Iterable[User]"):
        user_model = get_user_model()
        if isinstance(users, user_model):
            users = [users]

        return self.backend.delete_users(users)

    def clear(self):
        return self.backend.clear()


search = Search(settings.MISAGO_SEARCH)
