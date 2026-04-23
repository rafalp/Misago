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
from ..permissions.solutions import (
    check_change_thread_solution_permission,
    check_clear_thread_solution_permission,
    check_lock_thread_solution_permission,
    check_select_thread_solution_permission,
    check_unlock_thread_solution_permission,
)
from ..permissions.threads import (
    check_edit_thread_post_permission,
    check_reply_thread_permission,
)
from ..permissions.proxy import UserPermissionsProxy
from ..solutions.validators import is_valid_thread_solution
from ..threadupdates.models import ThreadUpdate
from ..threadupdates.actions import thread_updates_renderer
from .hooks import (
    populate_post_feed_data_hook,
)
from .models import Post, Thread
from .prefetch import prefetch_post_feed_data


class PostFeed:
    template_name: str = "misago/post_feed/index.html"
    template_name_htmx_append: str = "misago/post_feed/htmx_append.html"
    template_name_htmx_like: str = "misago/post_feed/htmx_like.html"
    post_template_name: str = "misago/post_feed/post.html"
    post_locked_template_name: str = "misago/post_feed/post_locked.html"
    post_solved_template_name: str = "misago/post_feed/post_solved.html"
    post_solution_template_name = "misago/post_feed/post_solution.html"
    post_unapproved_template_name = "misago/post_feed/post_unapproved.html"
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
            if post.category_id == self.category.id:
                post.category = self.category
            if post.thread_id == self.thread.id:
                post.thread = self.thread

            feed.append(self.get_post_data(post, i + self.counter_start + 1))

        for update in self.thread_updates:
            if update.category_id == self.category.id:
                update.category = self.category
            if update.thread_id == self.thread.id:
                update.thread = self.thread

            feed.append(self.get_thread_update_data(update))

        feed.sort(key=lambda item: item["ordering"])

        previous_item = None
        for item in feed:
            item["previous_item"] = previous_item
            if item["type"] == "post":
                previous_item = f"post-{item['post'].id}"
            elif item["type"] == "thread_update":
                previous_item = f"update-{item['thread_update'].id}"

        prefetched_data = prefetch_post_feed_data(
            self.request.settings,
            self.request.user_permissions,
            self.posts,
            categories=[self.category],
            threads=[self.thread],
            thread_updates=self.thread_updates,
        )

        populate_post_feed_data_hook(
            self.populate_post_feed_data, feed, prefetched_data
        )

        return feed

    def get_post_data(self, post: Post, counter: int = 1) -> dict:
        is_visible = self.is_moderator or not post.is_hidden

        if self.request.user.is_authenticated:
            poster_is_current_user = post.poster_id == self.request.user.id
        else:
            poster_is_current_user = False

        data = {
            "template_name": self.post_template_name,
            "type": "post",
            "post": post,
            "animate": post.id in self.animate_posts,
            "ordering": post.posted_at,
            "counter": counter,
            "poster": None,
            "poster_name": post.poster_name,
            "poster_is_current_user": poster_is_current_user,
            "rich_text_data": None,
            "attachments": [],
            "bars": [],
            "edits": None,
            "updated_at": post.updated_at,
            "last_edit_reason": None,
            "edit_url": None,
            "quote_url": None,
            "select_solution_url": None,
            "clear_solution_url": None,
            "lock_solution_url": None,
            "unlock_solution_url": None,
            "moderation": self.is_moderator,
            "is_new": post.id in self.unread_posts,
            "is_solution": False,
            "is_hidden": post.is_hidden,
            "is_visible": is_visible,
            "post_body_top_components": [],
            "post_body_bottom_components": [],
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

    def populate_post_feed_data(self, feed: list[dict], prefetched_data: dict) -> None:
        for item in feed:
            if item["type"] == "post":
                self.populate_post_data(item, item["post"], prefetched_data)
            if item["type"] == "thread_update":
                self.populate_thread_update_data(
                    item, item["thread_update"], prefetched_data
                )

    def populate_post_data(self, item: dict, post: Post, prefetched_data: dict) -> None:
        item["rich_text_data"] = prefetched_data

        if post.poster_id:
            post.poster = prefetched_data["users"][post.poster_id]
            item["poster"] = prefetched_data["users"].get(post.poster_id)

        embedded_attachments = post.metadata.get("attachments", [])
        for attachment in prefetched_data["attachments"].values():
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
            post.id in prefetched_data["liked_posts"],
            self.get_post_likes_url(post),
            self.get_post_like_url(post),
            self.get_post_unlike_url(post),
        )

        if post.is_locked and (
            self.is_moderator
            or (post.poster_id and post.poster_id == self.request.user.id)
        ):
            item["post_body_top_components"].append(
                self.get_post_locked_data(),
            )

        if self.thread.solution_id and post.id == self.thread.first_post_id:
            item["post_body_bottom_components"].append(
                self.get_post_solved_data(),
            )

        if post.is_unapproved:
            item["post_body_top_components"].append(
                self.get_post_unapproved_data(),
            )

        item["is_solution"] = is_solution = post.id == self.thread.solution_id

        if not is_solution and is_valid_thread_solution(post, self.request):
            with check_permissions():
                if self.thread.solution_id:
                    check_change_thread_solution_permission(self.user_permissions, post)
                else:
                    check_select_thread_solution_permission(self.user_permissions, post)

                item["select_solution_url"] = reverse(
                    "misago:thread-solution-select",
                    kwargs={
                        "thread_id": self.thread.id,
                        "slug": self.thread.slug,
                        "post_id": post.id,
                    },
                )

        elif is_solution:
            item["post_body_top_components"].append(
                self.get_post_solution_data(),
            )

            with check_permissions():
                check_clear_thread_solution_permission(
                    self.user_permissions, self.thread
                )

                item["clear_solution_url"] = reverse(
                    "misago:thread-solution-clear",
                    kwargs={
                        "thread_id": self.thread.id,
                        "slug": self.thread.slug,
                    },
                )

            if self.thread.solution_is_locked:
                with check_permissions():
                    check_unlock_thread_solution_permission(
                        self.user_permissions, self.thread
                    )

                    item["unlock_solution_url"] = reverse(
                        "misago:thread-solution-unlock",
                        kwargs={
                            "thread_id": self.thread.id,
                            "slug": self.thread.slug,
                        },
                    )

            else:
                with check_permissions():
                    check_lock_thread_solution_permission(
                        self.user_permissions, self.thread
                    )

                    item["lock_solution_url"] = reverse(
                        "misago:thread-solution-lock",
                        kwargs={
                            "thread_id": self.thread.id,
                            "slug": self.thread.slug,
                        },
                    )

    def get_post_locked_data(self) -> dict:
        return {"template_name": self.post_locked_template_name}

    def get_post_solved_data(self) -> dict:
        thread = self.thread

        data = {
            "template_name": self.post_solved_template_name,
            "solved_at": thread.solution_posted_at,
            "solved_by": None,
            "solved_by_name": thread.solution_by_name,
            "solution_url": reverse(
                "misago:thread-post-solution",
                kwargs={"thread_id": thread.id, "slug": thread.slug},
            ),
        }

        if thread.solution_by_id:
            data["solved_by"] = {
                "id": thread.solution_by_id,
                "username": thread.solution_by_name,
                "slug": thread.solution_by_slug,
            }

        return data

    def get_post_solution_data(self) -> dict:
        thread = self.thread

        data = {
            "template_name": self.post_solution_template_name,
            "selected_at": thread.solution_selected_at,
            "selected_by": None,
            "selected_by_name": thread.solution_selected_by_name,
            "is_locked": thread.solution_is_locked,
            "locked_at": thread.solution_locked_at,
            "locked_by": None,
            "locked_by_name": thread.solution_locked_by_name,
            "lock_url": None,
            "unlock_url": None,
        }

        if thread.solution_selected_by_id:
            data["selected_by"] = {
                "id": thread.solution_selected_by_id,
                "username": thread.solution_selected_by_name,
                "slug": thread.solution_selected_by_slug,
            }

        if thread.solution_locked_by_id:
            data["selected_by"] = {
                "id": thread.solution_locked_by_id,
                "username": thread.solution_locked_by_name,
                "slug": thread.solution_locked_by_slug,
            }

        return data

    def get_post_unapproved_data(self) -> dict:
        return {"template_name": self.post_unapproved_template_name}

    def populate_thread_update_data(
        self, item: dict, thread_update: ThreadUpdate, prefetched_data: dict
    ) -> None:
        if thread_update.actor_id:
            thread_update.actor = prefetched_data["users"].get(thread_update.actor_id)
            item["actor"] = thread_update.actor

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
                item["context_object"] = prefetched_data[relation_name].get(
                    thread_update.context_id
                )

        if thread_update_data := thread_updates_renderer.render_thread_update(
            thread_update, prefetched_data
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
