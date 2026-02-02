from html import escape
from typing import Iterable

from django.http import HttpRequest
from django.urls import reverse

from ..categories.models import Category
from ..likes.postfeed import get_post_feed_post_likes_data
from ..permissions.checkutils import check_permissions
from ..permissions.edits import (
    can_see_post_edit_count,
    check_see_post_edit_history_permission,
)
from ..permissions.threads import (
    check_edit_thread_post_permission,
    check_reply_thread_permission,
)
from ..permissions.proxy import UserPermissionsProxy
from ..threadupdates.models import ThreadUpdate
from ..threadupdates.actions import thread_updates_renderer
from .hooks import (
    set_post_feed_related_objects_hook,
)
from .models import Post, Thread
from .prefetch import prefetch_post_feed_related_objects


class PostFeed:
    template_name: str = "misago/post_feed/index.html"
    template_name_htmx_append: str = "misago/post_feed/htmx_append.html"
    template_name_htmx_like: str = "misago/post_feed/htmx_like.html"
    post_template_name: str = "misago/post_feed/post.html"
    thread_update_template_name: str = "misago/post_feed/thread_update.html"

    request: HttpRequest
    user_permissions: UserPermissionsProxy

    category: Category
    thread: Thread
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
        self.user_permissions = request.user_permissions

        self.category = thread.category
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

        related_objects = prefetch_post_feed_related_objects(
            self.request.settings,
            self.request.user_permissions,
            self.posts,
            categories=[self.thread.category],
            threads=[self.thread],
            thread_updates=self.thread_updates,
        )

        set_post_feed_related_objects_hook(
            self.set_post_feed_related_objects, feed, related_objects
        )

        return feed

    def get_post_data(self, post: Post, counter: int = 1) -> dict:
        is_visible = self.is_moderator or not post.is_hidden

        data = {
            "template_name": self.post_template_name,
            "animate": post.id in self.animate_posts,
            "type": "post",
            "ordering": post.posted_at,
            "post": post,
            "counter": counter,
            "poster": None,
            "poster_name": post.poster_name,
            "is_new": post.id in self.unread_posts,
            "rich_text_data": None,
            "attachments": [],
            "edits": None,
            "updated_at": post.updated_at,
            "last_edit_reason": None,
            "edit_url": None,
            "quote_url": None,
            "moderation": self.is_moderator,
            "is_hidden": post.is_hidden,
            "is_visible": is_visible,
        }

        if self.allow_reply_thread() and is_visible:
            data["quote_url"] = self.get_quote_post_url(post)

        if self.allow_edit_post(post) and is_visible:
            if post.id == self.thread.first_post_id and self.allow_edit_thread:
                data["edit_url"] = self.get_edit_thread_post_url()
            else:
                data["edit_url"] = self.get_edit_post_url(post)

        if post.edits and is_visible:
            if can_see_post_edit_count(
                self.user_permissions, self.category, self.thread, post
            ):
                data["edits"] = post.edits

            with check_permissions():
                check_see_post_edit_history_permission(
                    self.user_permissions, self.category, self.thread, post
                )
                data["last_edited_at"] = post.updated_at
                data["show_last_editor"] = (
                    post.last_editor_id and post.last_editor_id != post.poster_id
                )
                data["last_editor_name"] = post.last_editor_name
                data["last_edit_reason"] = post.last_edit_reason
                data["edits_url"] = self.get_post_edits_url(post)

        return data

    def allow_reply_thread(self) -> bool:
        return False

    def get_quote_post_url(self, post: Post) -> str | None:
        return None

    def allow_edit_post(self, post: Post) -> bool:
        return False

    def get_edit_thread_post_url(self) -> str | None:
        return None

    def get_edit_post_url(self, post: Post) -> str | None:
        return None

    def get_post_edits_url(self, post: Post) -> str | None:
        return None

    def get_post_likes_url(self, post: Post) -> str | None:
        return None

    def get_post_like_url(self, post: Post) -> str | None:
        return None

    def get_post_unlike_url(self, post: Post) -> str | None:
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

    def set_post_feed_related_objects(
        self, feed: list[dict], related_objects: dict
    ) -> None:
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

        item["likes"] = get_post_feed_post_likes_data(
            self.request,
            post,
            post.id in related_objects["liked_posts"],
            self.get_post_likes_url(post),
            self.get_post_like_url(post),
            self.get_post_unlike_url(post),
        )

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

    def get_like_context_data(self, post: Post, is_liked: bool) -> dict:
        return {
            "template_name": self.template_name_htmx_like,
            "post": post,
            "likes": get_post_feed_post_likes_data(
                self.request,
                post,
                is_liked,
                self.get_post_likes_url(post),
                self.get_post_like_url(post),
                self.get_post_unlike_url(post),
            ),
        }


class ThreadPostFeed(PostFeed):
    def get_moderator_status(self) -> bool:
        return self.request.user_permissions.is_category_moderator(
            self.thread.category_id
        )

    def allow_reply_thread(self) -> bool:
        if self.request.user.is_anonymous:
            return False

        with check_permissions() as can_reply_thread:
            check_reply_thread_permission(
                self.request.user_permissions, self.thread.category, self.thread
            )

        return can_reply_thread

    def get_quote_post_url(self, post: Post) -> str:
        return (
            reverse(
                "misago:thread-reply",
                kwargs={"thread_id": self.thread.id, "slug": self.thread.slug},
            )
            + f"?quote={post.id}"
        )

    def allow_edit_post(self, post: Post) -> bool:
        if self.request.user.is_anonymous:
            return False

        with check_permissions() as can_edit_post:
            check_edit_thread_post_permission(
                self.request.user_permissions, self.thread.category, self.thread, post
            )

        return can_edit_post

    def get_edit_thread_post_url(self) -> str:
        return reverse(
            "misago:thread-edit",
            kwargs={"thread_id": self.thread.id, "slug": self.thread.slug},
        )

    def get_edit_post_url(self, post: Post) -> str | None:
        return reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": self.thread.id,
                "slug": self.thread.slug,
                "post_id": post.id,
            },
        )

    def get_post_edits_url(self, post: Post) -> str | None:
        return reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": self.thread.id,
                "slug": self.thread.slug,
                "post_id": post.id,
            },
        )

    def get_post_likes_url(self, post: Post) -> str | None:
        return reverse(
            "misago:thread-post-likes",
            kwargs={
                "thread_id": self.thread.id,
                "slug": self.thread.slug,
                "post_id": post.id,
            },
        )

    def get_post_like_url(self, post: Post) -> str | None:
        return reverse(
            "misago:thread-post-like",
            kwargs={
                "thread_id": self.thread.id,
                "slug": self.thread.slug,
                "post_id": post.id,
            },
        )

    def get_post_unlike_url(self, post: Post) -> str | None:
        return reverse(
            "misago:thread-post-unlike",
            kwargs={
                "thread_id": self.thread.id,
                "slug": self.thread.slug,
                "post_id": post.id,
            },
        )

    def get_hide_thread_update_url(self, thread_update: ThreadUpdate) -> str | None:
        return reverse(
            "misago:thread-update-hide",
            kwargs={
                "thread_id": self.thread.id,
                "slug": self.thread.slug,
                "thread_update_id": thread_update.id,
            },
        )

    def get_unhide_thread_update_url(self, thread_update: ThreadUpdate) -> str | None:
        return reverse(
            "misago:thread-update-unhide",
            kwargs={
                "thread_id": self.thread.id,
                "slug": self.thread.slug,
                "thread_update_id": thread_update.id,
            },
        )

    def get_delete_thread_update_url(self, thread_update: ThreadUpdate) -> str | None:
        return reverse(
            "misago:thread-update-delete",
            kwargs={
                "thread_id": self.thread.id,
                "slug": self.thread.slug,
                "thread_update_id": thread_update.id,
            },
        )
