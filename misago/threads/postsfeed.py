from typing import TYPE_CHECKING, Iterable, Protocol

from django.contrib.auth import get_user_model
from django.db.models import prefetch_related_objects
from django.http import HttpRequest
from django.urls import reverse

from ..attachments.models import Attachment
from ..categories.models import Category
from ..conf.dynamicsettings import DynamicSettings
from ..permissions.checkutils import check_permissions
from ..permissions.privatethreads import (
    check_edit_private_thread_post_permission,
)
from ..permissions.threads import (
    check_edit_thread_post_permission,
)
from ..permissions.proxy import UserPermissionsProxy
from .hooks import (
    get_posts_feed_item_user_ids_hook,
    get_posts_feed_users_hook,
    set_posts_feed_item_users_hook,
)
from .models import Post, Thread

if TYPE_CHECKING:
    from ..users.models import User
else:
    User = get_user_model()


class PostsFeed:
    template_name: str = "misago/posts_feed/index.html"
    post_template_name: str = "misago/posts_feed/post.html"

    request: HttpRequest
    thread: Thread
    posts: list[Post]

    animate: set[int]
    unread: set[int]

    allow_edit_thread: bool
    is_moderator: bool
    counter_start: int

    def __init__(
        self, request: HttpRequest, thread: Thread, posts: list[Post] | None = None
    ):
        self.request = request
        self.thread = thread
        self.posts = posts or []

        self.animate = set()
        self.unread = set()

        self.allow_edit_thread = False
        self.is_moderator = False
        self.counter_start = 0

    def set_animated_posts(self, ids: Iterable[int]):
        self.animate = set(ids)

    def set_unread_posts(self, ids: Iterable[int]):
        self.unread = set(ids)

    def set_counter_start(self, counter_start: int):
        self.counter_start = counter_start

    def set_allow_edit_thread(self, allow_edit_thread: bool):
        self.allow_edit_thread = allow_edit_thread

    def get_context_data(self, context: dict | None = None) -> dict:
        context_data = {
            "template_name": self.template_name,
            "items": self.get_feed_data(),
        }

        if context:
            context_data.update(context)

        return context_data

    def get_feed_data(self) -> list[dict]:
        feed: list[dict] = []
        for i, post in enumerate(self.posts):
            feed.append(self.get_post_data(post, i + self.counter_start + 1))

        loader = get_posts_feed_data_loader(
            self.request.settings,
            self.request.user_permissions,
            posts=self.posts,
            categories=[self.thread.category],
            threads=[self.thread],
        )
        data = loader.load_data()

        # raise Exception(data)

        # self.populate_feed_users(feed)

        return feed

    def get_post_data(self, post: Post, counter: int = 1) -> dict:
        edit_url: str | None = None

        if self.allow_edit_post(post):
            if post.id == self.thread.first_post_id and self.allow_edit_thread:
                edit_url = self.get_edit_thread_post_url()
            else:
                edit_url = self.get_edit_post_url(post)

        return {
            "template_name": self.post_template_name,
            "animate": post.id in self.animate,
            "type": "post",
            "post": post,
            "counter": counter,
            "poster": None,
            "poster_name": post.poster_name,
            "unread": post.id in self.unread,
            "edit_url": edit_url,
            "moderation": False,
        }

    def allow_edit_post(self, post: Post) -> bool:
        return False

    def get_edit_thread_post_url(self) -> str | None:
        return None

    def get_edit_post_url(self, post: Post) -> str | None:
        return None

    def populate_feed_users(self, feed: list[dict]) -> None:
        user_ids: set[int] = set()
        for item in feed:
            self.get_feed_item_users_ids(item, user_ids)
            get_posts_feed_item_user_ids_hook(item, user_ids)

        if not user_ids:
            return

        users = get_posts_feed_users_hook(self.get_feed_users, self.request, user_ids)

        for item in feed:
            set_posts_feed_item_users_hook(self.set_feed_item_users, users, item)

    def get_feed_item_users_ids(self, item: dict, user_ids: set[int]):
        if item["type"] == "post":
            user_ids.add(item["post"].poster_id)

    def get_feed_users(
        self, request: HttpRequest, user_ids: set[int]
    ) -> dict[int, "User"]:
        users: dict[int, "User"] = {}
        for user in User.objects.filter(id__in=user_ids):
            if user.is_active or (
                request.user.is_authenticated and request.user.is_misago_admin
            ):
                users[user.id] = user

        prefetch_related_objects(list(users.values()), "group")
        return users

    def set_feed_item_users(self, users: dict[int, "User"], item: dict):
        if item["type"] == "post":
            item["poster"] = users.get(item["post"].poster_id)


class ThreadPostsFeed(PostsFeed):
    def allow_edit_post(self, post: Post) -> bool:
        if self.request.user.is_anonymous:
            return False

        with check_permissions() as can_edit_post:
            check_edit_thread_post_permission(
                self.request.user_permissions, self.thread.category, self.thread, post
            )

        return can_edit_post

    def get_edit_thread_post_url(self) -> str | None:
        return reverse(
            "misago:edit-thread",
            kwargs={"id": self.thread.id, "slug": self.thread.slug},
        )

    def get_edit_post_url(self, post: Post) -> str | None:
        return reverse(
            "misago:edit-thread",
            kwargs={"id": self.thread.id, "slug": self.thread.slug, "post": post.id},
        )


class PrivateThreadPostsFeed(PostsFeed):
    def allow_edit_post(self, post: Post) -> bool:
        with check_permissions() as can_edit_post:
            check_edit_private_thread_post_permission(
                self.request.user_permissions, self.thread, post
            )

        return can_edit_post

    def get_edit_thread_post_url(self) -> str | None:
        return reverse(
            "misago:edit-private-thread",
            kwargs={"id": self.thread.id, "slug": self.thread.slug},
        )

    def get_edit_post_url(self, post: Post) -> str | None:
        return reverse(
            "misago:edit-private-thread",
            kwargs={"id": self.thread.id, "slug": self.thread.slug, "post": post.id},
        )


class DataLoaderOperation(Protocol):
    def __call__(
        self,
        data: dict,
        settings: DynamicSettings,
        permissions: UserPermissionsProxy,
    ) -> None:
        pass


class PostsFeedDataLoader:
    ops: list[DataLoaderOperation]

    settings: DynamicSettings
    permissions: User

    categories: list[Category]
    threads: list[Thread]
    posts: list[Post]
    users: list[User]

    def __init__(
        self,
        settings: DynamicSettings,
        permissions: UserPermissionsProxy,
        *,
        posts: Iterable[Post],
        categories: Iterable[Category] | None = None,
        threads: Iterable[Thread] | None = None,
        attachments: Iterable[Attachment] | None = None,
        users: Iterable[User] | None = None,
    ):
        self.ops = []

        self.settings = settings
        self.permissions = permissions

        self.categories = categories or []
        self.threads = threads or []
        self.posts = list(posts)
        self.attachments = attachments or []
        self.users = users or []

    def add_operation(
        self,
        op: DataLoaderOperation,
        *,
        after: DataLoaderOperation | None = None,
        before: DataLoaderOperation | None = None,
    ):
        if after and before:
            raise ValueError("'after' and 'before' option's can't be used together")

        if after:
            inserted = False
            new_ops: list[DataLoaderOperation] = []

            for existing_step in self.ops:
                new_ops.append(existing_step)
                if existing_step == after:
                    new_ops.append(op)
                    inserted = True
            self.ops = new_ops

            if not inserted:
                raise ValueError(
                    f"Operation '{after}' doesn't exist in this loader instance"
                )

        elif before:
            prepended = False
            new_ops: list[DataLoaderOperation] = []

            for existing_step in self.ops:
                if existing_step == before:
                    new_ops.append(op)
                    prepended = True
                new_ops.append(existing_step)
            self.ops = new_ops

            if not prepended:
                raise ValueError(
                    f"Operation '{after}' doesn't exist in this loader instance"
                )

        else:
            self.ops.append(op)

    def load_data(self) -> dict:
        data = {
            "categories_ids": set(),
            "threads_ids": set(),
            "posts_ids": set(),
            "attachments_ids": set(),
            "categories": {c.id: c for c in self.categories},
            "threads": {t.id: t for t in self.threads},
            "posts": {p.id: p for p in self.posts},
            "attachments": {a.id: a for a in self.attachments},
            "users": {u.id: u for u in self.users},
        }

        for op in self.ops:
            op(data, self.settings, self.permissions)

        return data


def get_posts_feed_data_loader(
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
    *,
    posts: Iterable[Post],
    categories: Iterable[Category] | None = None,
    threads: Iterable[Thread] | None = None,
    attachments: Iterable[Attachment] | None = None,
    users: Iterable[User] | None = None,
) -> PostsFeedDataLoader:
    loader = PostsFeedDataLoader(
        settings,
        permissions,
        posts=posts,
        categories=categories,
        threads=threads,
        attachments=attachments,
        users=users,
    )

    loader.add_operation(find_attachments_ids)
    loader.add_operation(load_attachments)
    loader.add_operation(find_categories_ids)
    loader.add_operation(find_threads_ids)
    loader.add_operation(find_posts_ids)
    loader.add_operation(find_users_ids)
    loader.add_operation(load_categories)
    loader.add_operation(load_threads)
    loader.add_operation(load_posts)
    loader.add_operation(load_users)

    return loader


def find_categories_ids(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    pass


def find_threads_ids(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    pass


def find_posts_ids(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    pass


def find_attachments_ids(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    for post in data["posts"].values():
        data["attachments_ids"].update(post.metadata.get("attachments", []))


def find_users_ids(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    pass


def load_categories(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    pass


def load_threads(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    pass


def load_posts(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    pass


def load_attachments(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    pass


def load_users(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    pass
