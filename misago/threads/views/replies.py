from datetime import datetime
from typing import TYPE_CHECKING, Any

from django.contrib.auth import get_user_model
from django.db.models import QuerySet, prefetch_related_objects
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from ...categories.models import Category
from ...core.exceptions import OutdatedSlug
from ...readtracker.tracker import (
    get_unread_posts,
    mark_category_read,
    mark_thread_read,
)
from ...readtracker.privatethreads import are_private_threads_read
from ...readtracker.threads import is_category_read
from ..hooks import (
    get_private_thread_replies_page_context_data_hook,
    get_private_thread_replies_page_posts_queryset_hook,
    get_private_thread_replies_page_thread_queryset_hook,
    get_thread_posts_feed_item_user_ids_hook,
    get_thread_posts_feed_users_hook,
    get_thread_replies_page_context_data_hook,
    get_thread_replies_page_posts_queryset_hook,
    get_thread_replies_page_thread_queryset_hook,
    set_thread_posts_feed_item_users_hook,
)
from ..models import Post, Thread
from .generic import PrivateThreadView, ThreadView

if TYPE_CHECKING:
    from ...users.models import User
else:
    User = get_user_model()


class PageOutOfRangeError(Exception):
    redirect_to: str

    def __init__(self, redirect_to: str):
        self.redirect_to = redirect_to


class RepliesView(View):
    thread_annotate_read_time: bool = True
    template_name: str
    template_partial_name: str
    feed_template_name: str = "misago/posts_feed/index.html"
    feed_post_template_name: str = "misago/posts_feed/post.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            return super().dispatch(request, *args, **kwargs)
        except PageOutOfRangeError as exc:
            return redirect(exc.redirect_to)

    def get(
        self, request: HttpRequest, id: int, slug: str, page: int | None = None
    ) -> HttpResponse:
        thread = self.get_thread(request, id)

        if not request.is_htmx and thread.slug != slug:
            raise OutdatedSlug(thread)

        context = self.get_context_data(request, thread, page)

        if request.is_htmx:
            template_name = self.template_partial_name
        else:
            template_name = self.template_name

        return render(request, template_name, context)

    def get_context_data(
        self, request: HttpRequest, thread: Thread, page: int | None = None
    ) -> dict:
        return self.get_context_data_action(request, thread, page)

    def get_context_data_action(
        self, request: HttpRequest, thread: Thread, page: int | None = None
    ) -> dict:
        return {
            "thread": thread,
            "thread_url": self.get_thread_url(thread),
            "feed": self.get_posts_feed_data(request, thread, page),
        }

    def get_posts_feed_data(
        self, request: HttpRequest, thread: Thread, page: int | None = None
    ) -> dict:
        queryset = self.get_thread_posts_queryset(request, thread)
        paginator = self.get_thread_posts_paginator(request, queryset)

        if page and page > paginator.num_pages:
            if not request.is_htmx:
                raise PageOutOfRangeError(
                    self.get_thread_url(thread, paginator.num_pages)
                )

            page = paginator.num_pages

        page_obj = paginator.get_page(page)
        posts = list(page_obj.object_list)

        unread = get_unread_posts(request, thread, posts)

        items: list[dict] = []
        for post in posts:
            items.append(
                {
                    "template_name": self.feed_post_template_name,
                    "type": "post",
                    "post": post,
                    "poster": None,
                    "poster_name": post.poster_name,
                    "unread": post.id in unread,
                }
            )

        self.set_posts_feed_users(request, items)

        if unread:
            self.update_thread_read_time(request, thread, posts[-1].posted_on)

        if request.user.is_authenticated and request.user.unread_notifications:
            self.read_user_notifications(request.user, posts)

        return {
            "template_name": self.feed_template_name,
            "items": items,
            "paginator": page_obj,
        }

    def set_posts_feed_users(self, request: HttpRequest, feed: list[dict]) -> None:
        user_ids: set[int] = set()
        for item in feed:
            self.get_posts_feed_item_user_ids(item, user_ids)
            get_thread_posts_feed_item_user_ids_hook(item, user_ids)

        if not user_ids:
            return

        users = get_thread_posts_feed_users_hook(
            self.get_posts_feed_users, request, user_ids
        )

        for item in feed:
            set_thread_posts_feed_item_users_hook(
                self.set_post_feed_item_users, users, item
            )

    def get_posts_feed_item_user_ids(self, item: dict, user_ids: set[int]):
        if item["type"] == "post":
            user_ids.add(item["post"].poster_id)

    def get_posts_feed_users(
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

    def set_post_feed_item_users(self, users: dict[int, "User"], item: dict):
        if item["type"] == "post":
            item["poster"] = users.get(item["post"].poster_id)

    def update_thread_read_time(
        self,
        request: HttpRequest,
        thread: Thread,
        read_time: datetime,
    ):
        mark_thread_read(request.user, thread, read_time)

        if self.is_category_read(request, thread.category, thread.category_read_time):
            self.mark_category_read(
                request,
                thread.category,
                force_update=bool(thread.category_read_time),
            )

    def is_category_read(
        self,
        request: HttpRequest,
        category: Category,
        category_read_time: datetime | None,
    ) -> bool:
        raise NotImplementedError()

    def mark_category_read(
        self,
        request: HttpRequest,
        category: Category,
        *,
        force_update: bool,
    ):
        mark_category_read(
            request,
            category,
            force_update=force_update,
        )

    def read_user_notifications(self, user: "User", posts: list[Post]):
        updated_notifications = user.notification_set.filter(
            post__in=posts, is_read=False
        ).update(is_read=True)

        if updated_notifications:
            new_unread_notifications = max(
                [0, user.unread_notifications - updated_notifications]
            )

            if user.unread_notifications != new_unread_notifications:
                user.unread_notifications = new_unread_notifications
                user.save(update_fields=["unread_notifications"])


class ThreadRepliesView(RepliesView, ThreadView):
    template_name: str = "misago/thread/index.html"
    template_partial_name: str = "misago/thread/partial.html"

    def get_thread_queryset(self, request: HttpRequest) -> Thread:
        return get_thread_replies_page_thread_queryset_hook(
            super().get_thread_queryset, request
        )

    def get_context_data(
        self, request: HttpRequest, thread: Thread, page: int | None = None
    ) -> dict:
        return get_thread_replies_page_context_data_hook(
            self.get_context_data_action, request, thread, page
        )

    def get_context_data_action(
        self, request: HttpRequest, thread: Thread, page: int | None = None
    ) -> dict:
        context = super().get_context_data_action(request, thread, page)

        context.update(
            {
                "category": thread.category,
            }
        )

        return context

    def get_thread_posts_queryset(
        self, request: HttpRequest, thread: Thread
    ) -> QuerySet:
        return get_thread_replies_page_posts_queryset_hook(
            super().get_thread_posts_queryset, request, thread
        )

    def is_category_read(
        self,
        request: HttpRequest,
        category: Category,
        category_read_time: datetime | None,
    ) -> bool:
        return is_category_read(request, category, category_read_time)


class PrivateThreadRepliesView(RepliesView, PrivateThreadView):
    template_name: str = "misago/private_thread/index.html"
    template_partial_name: str = "misago/private_thread/partial.html"

    def get_thread_queryset(self, request: HttpRequest) -> Thread:
        return get_private_thread_replies_page_thread_queryset_hook(
            super().get_thread_queryset, request
        )

    def get_context_data(
        self, request: HttpRequest, thread: Thread, page: int | None = None
    ) -> dict:
        return get_private_thread_replies_page_context_data_hook(
            self.get_context_data_action, request, thread, page
        )

    def get_context_data_action(
        self, request: HttpRequest, thread: Thread, page: int | None = None
    ) -> dict:
        context = super().get_context_data_action(request, thread, page)

        context.update(
            {
                "participants": None,
            }
        )

        return context

    def get_thread_posts_queryset(
        self, request: HttpRequest, thread: Thread
    ) -> QuerySet:
        return get_private_thread_replies_page_posts_queryset_hook(
            super().get_thread_posts_queryset, request, thread
        )

    def update_thread_read_time(
        self,
        request: HttpRequest,
        thread: Thread,
        read_time: datetime,
    ):
        unread_private_threads = request.user.unread_private_threads
        if read_time > thread.last_post_on and request.user.unread_private_threads:
            request.user.unread_private_threads -= 1

        super().update_thread_read_time(request, thread, read_time)

        if request.user.unread_private_threads != unread_private_threads:
            request.user.save(update_fields=["unread_private_threads"])

    def is_category_read(
        self,
        request: HttpRequest,
        category: Category,
        category_read_time: datetime | None,
    ) -> bool:
        return are_private_threads_read(request, category, category_read_time)

    def mark_category_read(
        self,
        request: HttpRequest,
        category: Category,
        *,
        force_update: bool,
    ):
        super().mark_category_read(
            request,
            category,
            force_update=force_update,
        )

        request.user.unread_private_threads = 0


thread_replies = ThreadRepliesView.as_view()
private_thread_replies = PrivateThreadRepliesView.as_view()
