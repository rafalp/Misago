from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model

from ..categories.models import Category
from ..permissions.proxy import UserPermissionsProxy
from ..threads.models import Post, Thread
from .enums import SearchMode, SearchOrder

if TYPE_CHECKING:
    from ..users.models import User


class SearchBackend(ABC):
    @abstractmethod
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
        mode: SearchMode = SearchMode.THREADS,
        order: SearchOrder = SearchOrder.RELEVANCE,
        offset: int = 0,
        limit: int = 50,
        **kwargs,
    ) -> dict:
        pass

    @abstractmethod
    def index_posts(self, posts: Post | list[Post]):
        pass

    @abstractmethod
    def move_category_posts(
        self, categories: Category | list[Category], new_category: Category
    ):
        pass

    @abstractmethod
    def move_thread_posts(self, threads: Thread | list[Thread], new_thread: Thread):
        pass

    @abstractmethod
    def move_threads(self, threads: Thread | list[Thread], new_category: Category):
        pass

    @abstractmethod
    def move_posts(self, posts: Post | list[Post], new_thread: Thread):
        pass

    @abstractmethod
    def delete_categories(self, categories: Category | list[Category]):
        pass

    @abstractmethod
    def delete_threads(self, threads: Thread | list[Thread]):
        pass

    @abstractmethod
    def delete_posts(self, posts: Post | list[Post]):
        pass

    @abstractmethod
    def delete_users(self, users: "User" | list["User"]):
        pass

    @abstractmethod
    def clear(self):
        pass


class PostgreSQLSearchBackend(SearchBackend):
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
        mode: SearchMode = SearchMode.THREADS,
        order: SearchOrder = SearchOrder.RELEVANCE,
        start: int = 0,
        stop: int | None = None,
        **kwargs,
    ) -> dict:
        pass

    def index_posts(self, posts: Post | list[Post]):
        if isinstance(posts, Post):
            posts = [posts]

    def move_category_posts(
        self, categories: Category | list[Category], new_category: Category
    ):
        if isinstance(categories, Category):
            categories = [categories]

    def move_thread_posts(self, threads: Thread | list[Thread], new_thread: Thread):
        if isinstance(threads, Thread):
            threads = [threads]

    def move_threads(self, threads: Thread | list[Thread], new_category: Category):
        if isinstance(threads, Thread):
            threads = [threads]

    def move_posts(self, posts: Post | list[Post], new_thread: Thread):
        if isinstance(posts, Post):
            posts = [posts]

    def delete_categories(self, categories: Category | list[Category]):
        if isinstance(categories, Category):
            categories = [categories]

    def delete_threads(self, threads: Thread | list[Thread]):
        if isinstance(threads, Thread):
            threads = [threads]

    def delete_posts(self, posts: Post | list[Post]):
        if isinstance(posts, Post):
            posts = [posts]

    def delete_users(self, users: "User" | list["User"]):
        user_model = get_user_model()
        if isinstance(users, user_model):
            users = [users]

    def clear(self):
        pass
