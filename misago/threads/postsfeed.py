from html import escape
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
from ..threadupdates.models import ThreadUpdate
from ..threadupdates.actions import thread_updates_renderer
from .hooks import (
    set_posts_feed_related_objects_hook,
)
from .models import Post, Thread
from .prefetch import prefetch_posts_feed_related_objects


class PostsFeed:
    template_name: str = "misago/posts_feed/index.html"
    template_name_htmx_append: str = "misago/posts_feed/htmx_append.html"
    post_template_name: str = "misago/posts_feed/post.html"
    thread_update_template_name: str = "misago/posts_feed/thread_update.html"

    request: HttpRequest
    thread: Thread
    posts: list[Post]
    updates: list[ThreadUpdate]

    animate_posts: set[int]
    animate_thread_updates: set[int]

    unread_posts: set[int]

    allow_edit_thread: bool
    is_moderator: bool
    counter_start: int

    def __init__(
        self,
        request: HttpRequest,
        thread: Thread,
        posts: list[Post] | None = None,
        thread_updates: list[ThreadUpdate] | None = None,
    ):
        self.request = request
        self.thread = thread
        self.posts = posts or []
        self.thread_updates = thread_updates or []

        self.animate_posts = set()
        self.animate_thread_updates = set()

        self.unread_posts = set()

        self.allow_edit_thread = False
        self.is_moderator = self.get_moderator_status()
        self.counter_start = 0

    def set_animated_posts(self, ids: Iterable[int]):
        self.animate_posts = set(ids)

    def set_animated_thread_updates(self, ids: Iterable[int]):
        self.animate_thread_updates = set(ids)

    def set_unread_posts(self, ids: Iterable[int]):
        self.unread_posts = set(ids)

    def set_counter_start(self, counter_start: int):
        self.counter_start = counter_start

    def get_moderator_status(self) -> bool:
        return False

    def set_allow_edit_thread(self, allow_edit_thread: bool):
        self.allow_edit_thread = allow_edit_thread

    def get_context_data(self, context: dict | None = None) -> dict:
        context_data = {
            "template_name": self.template_name,
            "template_name_htmx_append": self.template_name_htmx_append,
            "items": self.get_feed_data(),
        }

        if context:
            context_data.update(context)

        return context_data

    def get_feed_data(self) -> list[dict]:
        feed: list[dict] = []
        for i, post in enumerate(self.posts):
            feed.append(self.get_post_data(post, i + self.counter_start + 1))
        for update in self.thread_updates:
            feed.append(self.get_thread_update_data(update))

        feed.sort(key=lambda item: item["ordering"])

        previous_item = None
        for item in feed:
            item["previous_item"] = previous_item
            if item["type"] == "post":
                previous_item = f"post-{item['post'].id}"
            elif item["type"] == "thread_update":
                previous_item = f"update-{item['thread_update'].id}"

        related_objects = prefetch_posts_feed_related_objects(
            self.request.settings,
            self.request.user_permissions,
            self.posts,
            categories=[self.thread.category],
            threads=[self.thread],
            thread_updates=self.thread_updates,
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
            "animate": post.id in self.animate_posts,
            "type": "post",
            "ordering": post.posted_on,
            "post": post,
            "counter": counter,
            "poster": None,
            "poster_name": post.poster_name,
            "unread": post.id in self.unread_posts,
            "rich_text_data": None,
            "attachments": [],
            "edit_url": edit_url,
            "moderation": self.is_moderator,
        }

    def allow_edit_post(self, post: Post) -> bool:
        return False

    def get_edit_thread_post_url(self) -> str | None:
        return None

    def get_edit_post_url(self, post: Post) -> str | None:
        return None

    def get_thread_update_data(self, thread_update: ThreadUpdate) -> dict:
        hide_url: str | None = None
        unhide_url: str | None = None
        delete_url: str | None = None

        if self.is_moderator:
            if thread_update.is_hidden:
                unhide_url = self.get_unhide_thread_update_url(thread_update)
            else:
                hide_url = self.get_hide_thread_update_url(thread_update)

            delete_url = self.get_delete_thread_update_url(thread_update)

        return {
            "template_name": self.thread_update_template_name,
            "animate": thread_update.id in self.animate_thread_updates,
            "ordering": thread_update.created_at,
            "type": "thread_update",
            "thread_update": thread_update,
            "icon": "",
            "description": "",
            "actor": None,
            "actor_name": thread_update.actor_name,
            "context_object": None,
            "hide_url": hide_url,
            "unhide_url": unhide_url,
            "delete_url": delete_url,
            "moderation": self.is_moderator,
        }

    def get_hide_thread_update_url(self, thread_update: ThreadUpdate) -> str | None:
        return None

    def get_unhide_thread_update_url(self, thread_update: ThreadUpdate) -> str | None:
        return None

    def get_delete_thread_update_url(self, thread_update: ThreadUpdate) -> str | None:
        return None

    def set_feed_related_objects(self, feed: list[dict], related_objects: dict) -> None:
        for item in feed:
            if item["type"] == "post":
                self.set_post_related_objects(item, item["post"], related_objects)
            if item["type"] == "thread_update":
                self.set_thread_update_related_objects(
                    item, item["thread_update"], related_objects
                )

    def set_post_related_objects(
        self, item: dict, post: Post, related_objects: dict
    ) -> None:
        item["rich_text_data"] = related_objects

        if post.poster_id:
            item["poster"] = related_objects["users"].get(post.poster_id)

        embedded_attachments = post.metadata.get("attachments", [])
        for attachment in related_objects["attachments"].values():
            if (
                attachment.post_id == post.id
                and attachment.id not in embedded_attachments
            ):
                item["attachments"].append(attachment)

        if item["attachments"]:
            item["attachments"].sort(reverse=True, key=lambda a: a.id)

    def set_thread_update_related_objects(
        self, item: dict, thread_update: ThreadUpdate, related_objects: dict
    ) -> None:
        if thread_update.actor_id:
            item["actor"] = related_objects["users"].get(thread_update.actor_id)

        if thread_update.context_type and thread_update.context_id:
            relation_name = None
            if thread_update.context_type == "misago_attachments.attachment":
                relation_name = "attachment"
            if thread_update.context_type == "misago_categories.category":
                relation_name = "categories"
            if thread_update.context_type == "misago_threads.thread":
                relation_name = "threads"
            if thread_update.context_type == "misago_threads.post":
                relation_name = "posts"
            if thread_update.context_type == "misago_users.user":
                relation_name = "users"

            if relation_name:
                item["context_object"] = related_objects[relation_name].get(
                    thread_update.context_id
                )

        if thread_update_data := thread_updates_renderer.render_thread_update(
            thread_update, related_objects
        ):
            item.update(thread_update_data)
        else:
            item.update(
                {"icon": "broken_image", "description": escape(thread_update.action)}
            )


class ThreadPostsFeed(PostsFeed):
    def get_moderator_status(self) -> bool:
        return self.request.user_permissions.is_category_moderator(
            self.thread.category_id
        )

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

    def get_hide_thread_update_url(self, thread_update: ThreadUpdate) -> str | None:
        return reverse(
            "misago:hide-thread-update",
            kwargs={
                "id": self.thread.id,
                "slug": self.thread.slug,
                "thread_update": thread_update.id,
            },
        )

    def get_unhide_thread_update_url(self, thread_update: ThreadUpdate) -> str | None:
        return reverse(
            "misago:unhide-thread-update",
            kwargs={
                "id": self.thread.id,
                "slug": self.thread.slug,
                "thread_update": thread_update.id,
            },
        )

    def get_delete_thread_update_url(self, thread_update: ThreadUpdate) -> str | None:
        return reverse(
            "misago:delete-thread-update",
            kwargs={
                "id": self.thread.id,
                "slug": self.thread.slug,
                "thread_update": thread_update.id,
            },
        )


class PrivateThreadPostsFeed(PostsFeed):
    def get_moderator_status(self) -> bool:
        return self.request.user_permissions.is_private_threads_moderator

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

    def get_hide_thread_update_url(self, thread_update: ThreadUpdate) -> str | None:
        return reverse(
            "misago:hide-private-thread-update",
            kwargs={
                "id": self.thread.id,
                "slug": self.thread.slug,
                "thread_update": thread_update.id,
            },
        )

    def get_unhide_thread_update_url(self, thread_update: ThreadUpdate) -> str | None:
        return reverse(
            "misago:unhide-private-thread-update",
            kwargs={
                "id": self.thread.id,
                "slug": self.thread.slug,
                "thread_update": thread_update.id,
            },
        )

    def get_delete_thread_update_url(self, thread_update: ThreadUpdate) -> str | None:
        return reverse(
            "misago:delete-private-thread-update",
            kwargs={
                "id": self.thread.id,
                "slug": self.thread.slug,
                "thread_update": thread_update.id,
            },
        )
