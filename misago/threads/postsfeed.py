from typing import Iterable

from django.http import HttpRequest
from django.urls import reverse

from ..permissions.checkutils import check_permissions
from ..permissions.privatethreads import (
    check_edit_private_thread_post_permission,
)
from ..permissions.threads import (
    check_edit_thread_post_permission,
)
from .hooks import (
    set_posts_feed_related_objects_hook,
)
from .models import Post, Thread
from .prefetch import prefetch_posts_related_objects


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

        related_objects = prefetch_posts_related_objects(
            self.request.settings,
            self.request.user_permissions,
            self.posts,
            categories=[self.thread.category],
            threads=[self.thread],
        )
        set_posts_feed_related_objects_hook(
            self.set_feed_related_objects, feed, related_objects
        )

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
            "attachments": [],
            "rich_text_data": None,
        }

    def allow_edit_post(self, post: Post) -> bool:
        return False

    def get_edit_thread_post_url(self) -> str | None:
        return None

    def get_edit_post_url(self, post: Post) -> str | None:
        return None

    def set_feed_related_objects(self, feed: list[dict], related_objects: dict) -> None:
        for item in feed:
            if item["type"] == "post":
                self.set_post_related_objects(item, item["post"], related_objects)

    def set_post_related_objects(
        self, item: dict, post: Post, related_objects: dict
    ) -> None:
        item["poster"] = related_objects["users"].get(post.poster_id)
        item["rich_text_data"] = related_objects

        embedded_attachments = post.metadata.get("attachments", [])
        for attachment in related_objects["attachments"].values():
            if (
                attachment.post_id == post.id
                and attachment.id not in embedded_attachments
            ):
                item["attachments"].append(attachment)

        if item["attachments"]:
            item["attachments"].sort(reverse=True, key=lambda a: a.id)


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
