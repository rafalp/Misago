from datetime import datetime
from typing import TYPE_CHECKING, Any

from django.contrib.auth import get_user_model
from django.db.models import QuerySet, prefetch_related_objects
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from ...core.exceptions import OutdatedSlug
from ...readtracker.threads import get_thread_posts_new_status
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

        posts_new = get_thread_posts_new_status(request, thread, page_obj.object_list)

        items: list[dict] = []
        for post in page_obj.object_list:
            items.append(
                {
                    "template_name": self.feed_post_template_name,
                    "type": "post",
                    "post": post,
                    "poster": None,
                    "poster_name": post.poster_name,
                    "new": posts_new.get(post.id, False),
                }
            )

        self.set_posts_feed_users(request, items)

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


thread_replies = ThreadRepliesView.as_view()
private_thread_replies = PrivateThreadRepliesView.as_view()
