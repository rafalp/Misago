from typing import TYPE_CHECKING, Any

from django.contrib.auth import get_user_model
from django.db.models import prefetch_related_objects
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from ...core.exceptions import OutdatedSlug
from ..models import Thread
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
    template_name: str
    template_partial_name: str
    feed_template_name: str = "misago/thread_feed/index.html"
    feed_post_template_name: str = "misago/thread_feed/post.html"

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
        return {
            "thread": thread,
            "thread_url": self.get_thread_url(thread),
            "feed": self.get_thread_feed_data(request, thread, page),
        }

    def get_thread_feed_data(
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

        items: list[dict] = []
        for post in page_obj.object_list:
            items.append(
                {
                    "template_name": self.feed_post_template_name,
                    "type": "post",
                    "post": post,
                    "poster": None,
                }
            )

        self.populate_feed_items_users(request, items)

        return {
            "template_name": self.feed_template_name,
            "items": items,
            "paginator": page_obj,
        }

    def populate_feed_items_users(
        self, request: HttpRequest, items: list[dict]
    ) -> None:
        users_ids: set[int] = set()

        # first pass: populate users ids
        for item in items:
            if item["type"] == "post":
                users_ids.add(item["post"].poster_id)

        # fetch users
        users: dict[int, "User"] = {}
        if not users_ids:
            return

        for user in User.objects.filter(id__in=users_ids):
            users[user.id] = user

        if users:
            prefetch_related_objects(list(users.values()), "group")

        # second pass: set users on feed items
        for item in items:
            if item["type"] == "post":
                item["poster"] = users.get(item["post"].poster_id)


class ThreadRepliesView(RepliesView, ThreadView):
    template_name: str = "misago/thread/index.html"
    template_partial_name: str = "misago/thread/partial.html"

    def get_context_data(
        self, request: HttpRequest, thread: Thread, page: int | None = None
    ) -> dict:
        context = super().get_context_data(request, thread, page)

        context.update(
            {
                "category": thread.category,
            }
        )

        return context


class PrivateThreadRepliesView(RepliesView, PrivateThreadView):
    template_name: str = "misago/private_thread/index.html"
    template_partial_name: str = "misago/private_thread/partial.html"


thread_replies = ThreadRepliesView.as_view()
private_thread_replies = PrivateThreadRepliesView.as_view()
