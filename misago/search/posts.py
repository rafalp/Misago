from datetime import datetime
from typing import TYPE_CHECKING, Iterable, Union

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.module_loading import import_string

from ..categories.models import Category
from ..permissions.proxy import UserPermissionsProxy
from ..threads.models import Post, Thread
from .backends import SearchBackend
from .enums import SearchMode, SearchOrder

if TYPE_CHECKING:
    from ..users.models import User


class PostsSearch:
    backend: SearchBackend
    index_batch_size: int
    max_limit: int

    def __init__(self, options: dict):
        if not isinstance(options, dict):
            raise TypeError("MISAGO_POSTS_SEARCH must be a dictionary")

        try:
            backend_name = options["BACKEND"]
        except KeyError:
            raise ValueError("MISAGO_POSTS_SEARCH is missing the 'BACKEND' option")

        try:
            backend_class = import_string(backend_name)
        except ImportError as exc:
            raise ValueError(
                f"Could not import '{backend_name}' search backend"
            ) from exc

        self.backend = backend_class(options)

        try:
            self.index_batch_size = int(options.get("INDEX_BATCH_SIZE", 50))
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"PostsSearch was initialized with invalid 'INDEX_BATCH_SIZE': {exc}"
            ) from exc

        try:
            self.max_limit = int(options.get("MAX_LIMIT", 50))
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"PostsSearch was initialized with invalid 'MAX_LIMIT': {exc}"
            ) from exc

    def initialize(self):
        self.backend.initialize()

    def search(
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
        return self.backend.search_posts(
            query,
            mode,
            permissions,
            categories=categories,
            threads=threads,
            users=users,
            posted_after=posted_after,
            posted_before=posted_before,
            order=order,
            offset=offset,
            limit=limit,
            **kwargs,
        )

    def index_post(self, post: Post, search_document: str):
        self.backend.index_posts([(post, search_document)])

    def index_posts(self, posts: Iterable[tuple[Post, str]]):
        self.backend.index_posts(posts)

    def move_category_posts(
        self, categories: Category | Iterable[Category], new_category: Category
    ) -> int:
        if isinstance(categories, Category):
            categories = [categories]

        return self.backend.move_category_posts(categories, new_category)

    def move_thread_posts(
        self, threads: Thread | Iterable[Thread], new_thread: Thread
    ) -> int:
        if isinstance(threads, Thread):
            threads = [threads]

        return self.backend.move_thread_posts(threads, new_thread)

    def move_threads(
        self, threads: Thread | Iterable[Thread], new_category: Category
    ) -> int:
        if isinstance(threads, Thread):
            threads = [threads]

        return self.backend.move_threads(threads, new_category)

    def move_posts(self, posts: Post | Iterable[Post], new_thread: Thread) -> int:
        if isinstance(posts, Post):
            posts = [posts]

        return self.backend.move_posts(posts, new_thread)

    def delete_categories(self, categories: Category | Iterable[Category]) -> int:
        if isinstance(categories, Category):
            categories = [categories]

        return self.backend.delete_categories(categories)

    def delete_threads(self, threads: Thread | Iterable[Thread]) -> int:
        if isinstance(threads, Thread):
            threads = [threads]

        return self.backend.delete_threads(threads)

    def delete_posts(self, posts: Post | Iterable[Post]) -> int:
        if isinstance(posts, Post):
            posts = [posts]

        return self.backend.delete_posts(posts)

    def delete_users(self, users: Union["User", Iterable["User"]]) -> int:
        user_model = get_user_model()
        if isinstance(users, user_model):
            users = [users]

        return self.backend.delete_users(users)

    def clear(self):
        self.backend.clear()


posts_search = PostsSearch(settings.MISAGO_POSTS_SEARCH)
