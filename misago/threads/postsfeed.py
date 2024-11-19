from typing import TYPE_CHECKING, Iterable

from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.db.models import prefetch_related_objects
from django.http import Http404, HttpRequest
from django.urls import reverse

from ..permissions.privatethreads import (
    check_edit_private_thread_post_permission,
)
from ..permissions.threads import (
    check_edit_post_permission,
)
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

    def set_animate_posts(self, ids: Iterable[int]):
        self.animate = set(ids)

    def set_unread_posts(self, ids: Iterable[int]):
        self.unread = set(ids)

    def set_allow_edit_thread(self, allow_edit_thread: bool):
        self.allow_edit_thread = allow_edit_thread

    def set_moderation(self, is_moderator: bool):
        self.is_moderator = is_moderator

    def get_context_data(self, context) -> dict:
        context_data = {
            "template_name": self.template_name,
            "items": self.get_feed_data(),
        }

        if context:
            context_data.update(context)

        return context_data

    def get_feed_data(self) -> list[dict]:
        feed: list[dict] = []
        for post in self.posts:
            feed.append(self.get_post_data(post))

        self.populate_feed_users(feed)

        return feed

    def get_post_data(self, post: Post) -> dict:
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

        try:
            check_edit_post_permission(
                self.request.user_permissions, self.thread.category, self.thread, post
            )
            return True
        except (Http404, PermissionDenied):
            return False

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
        try:
            check_edit_private_thread_post_permission(
                self.request.user_permissions, self.thread, post
            )
            return True
        except (Http404, PermissionDenied):
            return False

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
