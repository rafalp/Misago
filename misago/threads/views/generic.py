from typing import Iterable

from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import Resolver404, resolve, reverse
from django.views import View

from ...permissions.privatethreads import (
    check_see_private_thread_permission,
    filter_private_thread_posts_queryset,
    filter_private_thread_updates_queryset,
)
from ...permissions.threads import (
    check_see_thread_permission,
    filter_thread_posts_queryset,
    filter_thread_updates_queryset,
)
from ...readtracker.tracker import (
    threads_annotate_user_readcategory_time,
    threads_select_related_user_readthread,
)
from ...threadupdates.models import ThreadUpdate
from ..models import Post, Thread
from ..paginator import ThreadRepliesPaginator
from ..postsfeed import PostsFeed, PrivateThreadPostsFeed, ThreadPostsFeed


class GenericView(View):
    thread_select_related: Iterable[str] | True | None = None
    thread_annotate_read_time: bool = False
    thread_url_name: str
    post_select_related: Iterable[str] | True | None = None
    thread_update_select_related: Iterable[str] | True | None = None

    def get_thread(self, request: HttpRequest, thread_id: int) -> Thread:
        queryset = self.get_thread_queryset(request)
        return get_object_or_404(queryset, id=thread_id)

    def get_thread_queryset(self, request: HttpRequest) -> Thread:
        queryset = Thread.objects
        if self.thread_annotate_read_time:
            queryset = threads_annotate_user_readcategory_time(queryset, request.user)
            queryset = threads_select_related_user_readthread(queryset, request.user)
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
        self,
        request: HttpRequest,
        thread: Thread,
        posts: list[Post],
        thread_updates: list[ThreadUpdate] | None = None,
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

    def clean_thread_url(self, thread: Thread, url_to_clean: str | None = None) -> str:
        thread_url = self.get_thread_url(thread)

        if url_to_clean:
            try:
                url_path = url_to_clean
                if "#" in url_path:
                    url_path = url_path[: url_path.index("#")]
                if "?" in url_path:
                    url_path = url_path[: url_path.index("?")]

                reverse_match = resolve(url_path)
                if reverse_match.view_name == self.thread_url_name:
                    return url_to_clean
            except Resolver404:
                pass

        return thread_url

    def get_thread_updates_queryset(
        self,
        request: HttpRequest,
        thread: Thread,
    ) -> QuerySet:
        return ThreadUpdate.objects.filter(thread=thread).order_by("-id")

    def get_thread_update(
        self, request: HttpRequest, thread: Thread, thread_update_id: int
    ) -> ThreadUpdate:
        queryset = self.get_thread_updates_queryset(request, thread)
        if self.thread_update_select_related is True:
            queryset = queryset.select_related()
        elif self.thread_update_select_related:
            queryset = queryset.select_related(*self.thread_update_select_related)

        thread_update = get_object_or_404(queryset, id=thread_update_id)

        if self.thread_select_related and (
            self.thread_select_related is True
            or "category" in self.thread_select_related
        ):
            thread_update.category = thread.category

        thread_update.thread = thread

        return thread_update


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

    def get_thread_updates_queryset(
        self,
        request: HttpRequest,
        thread: Thread,
    ) -> QuerySet:
        queryset = super().get_thread_updates_queryset(request, thread)
        return filter_thread_updates_queryset(
            request.user_permissions, thread, queryset
        )

    def get_posts_feed(
        self,
        request: HttpRequest,
        thread: Thread,
        posts: list[Post],
        thread_updates: list[ThreadUpdate] | None = None,
    ) -> PostsFeed:
        return ThreadPostsFeed(request, thread, posts, thread_updates)


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

    def get_thread_updates_queryset(
        self,
        request: HttpRequest,
        thread: Thread,
    ) -> QuerySet:
        queryset = super().get_thread_updates_queryset(request, thread)
        return filter_private_thread_updates_queryset(
            request.user_permissions, thread, queryset
        )

    def get_posts_feed(
        self,
        request: HttpRequest,
        thread: Thread,
        posts: list[Post],
        thread_updates: list[ThreadUpdate] | None = None,
    ) -> PostsFeed:
        return PrivateThreadPostsFeed(request, thread, posts, thread_updates)
