from typing import Iterable

from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View

from ...permissions.privatethreads import (
    check_see_private_thread_permission,
    filter_private_thread_posts_queryset,
)
from ...permissions.threads import (
    check_see_thread_permission,
    filter_thread_posts_queryset,
)
from ...readtracker.tracker import annotate_threads_read_time
from ..models import Post, Thread
from ..paginator import ThreadRepliesPaginator
from ..postsfeed import PostsFeed, PrivateThreadPostsFeed, ThreadPostsFeed


class GenericView(View):
    thread_select_related: Iterable[str] | True | None = None
    thread_annotate_read_time: bool = False
    thread_url_name: str
    post_select_related: Iterable[str] | True | None = None

    def get_thread(self, request: HttpRequest, thread_id: int) -> Thread:
        queryset = self.get_thread_queryset(request)
        return get_object_or_404(queryset, id=thread_id)

    def get_thread_queryset(self, request: HttpRequest) -> Thread:
        queryset = Thread.objects
        if self.thread_annotate_read_time:
            queryset = annotate_threads_read_time(request.user, queryset)
        if self.thread_select_related is True:
            return queryset.select_related()
        elif self.thread_select_related:
            return queryset.select_related(*self.thread_select_related)
        return queryset

    def get_thread_posts_queryset(
        self, request: HttpRequest, thread: Thread
    ) -> QuerySet:
        return thread.post_set.order_by("id")

    def get_thread_post(
        self, request: HttpRequest, thread: Thread, post_id: int
    ) -> Post:
        queryset = self.get_thread_posts_queryset(request, thread)
        if self.post_select_related is True:
            queryset = queryset.select_related()
        elif self.post_select_related:
            queryset = queryset.select_related(*self.post_select_related)

        post = get_object_or_404(queryset, id=post_id)

        if self.thread_select_related and (
            self.thread_select_related is True
            or "category" in self.thread_select_related
        ):
            post.category = thread.category

        post.thread = thread

        return post

    def get_thread_posts_paginator(
        self,
        request: HttpRequest,
        queryset: QuerySet,
    ) -> Paginator:
        return ThreadRepliesPaginator(
            queryset.order_by("id"),
            request.settings.posts_per_page,
            request.settings.posts_per_page_orphans,
        )

    def get_posts_feed(
        self, request: HttpRequest, thread: Thread, posts: list[Post]
    ) -> PostsFeed:
        raise NotImplementedError()

    def get_thread_url(self, thread: Thread, page: int | None = None) -> str:
        if page and page > 1:
            return reverse(
                self.thread_url_name,
                kwargs={"id": thread.id, "slug": thread.slug, "page": page},
            )

        return reverse(
            self.thread_url_name,
            kwargs={"id": thread.id, "slug": thread.slug},
        )


class ThreadView(GenericView):
    thread_select_related: Iterable[str] | True | None = ("category",)
    thread_url_name: str = "misago:thread"

    def get_thread(self, request: HttpRequest, thread_id: int) -> Thread:
        thread = super().get_thread(request, thread_id)
        check_see_thread_permission(request.user_permissions, thread.category, thread)
        return thread

    def get_thread_posts_queryset(
        self, request: HttpRequest, thread: Thread
    ) -> QuerySet:
        queryset = super().get_thread_posts_queryset(request, thread)
        return filter_thread_posts_queryset(request.user_permissions, thread, queryset)

    def get_posts_feed(
        self, request: HttpRequest, thread: Thread, posts: list[Post]
    ) -> PostsFeed:
        return ThreadPostsFeed(request, thread, posts)


class PrivateThreadView(GenericView):
    thread_url_name: str = "misago:private-thread"

    def get_thread(self, request: HttpRequest, thread_id: int) -> Thread:
        thread = super().get_thread(request, thread_id)
        check_see_private_thread_permission(request.user_permissions, thread)
        return thread

    def get_thread_posts_queryset(
        self, request: HttpRequest, thread: Thread
    ) -> QuerySet:
        queryset = super().get_thread_posts_queryset(request, thread)
        return filter_private_thread_posts_queryset(
            request.user_permissions, thread, queryset
        )

    def get_posts_feed(
        self, request: HttpRequest, thread: Thread, posts: list[Post]
    ) -> PostsFeed:
        return PrivateThreadPostsFeed(request, thread, posts)
