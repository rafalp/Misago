from typing import Any, Iterable

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
from ..models import Post, Thread
from ..paginator import ThreadRepliesPaginator


class GenericView(View):
    thread_select_related: Iterable[str] | True | None = None
    post_select_related: Iterable[str] | None = None
    thread_url_name: str

    def get_thread(self, request: HttpRequest, thread_id: int) -> Thread:
        queryset = self.get_thread_queryset(request)
        return get_object_or_404(queryset, id=thread_id)

    def get_thread_queryset(self, request: HttpRequest) -> Thread:
        queryset = Thread.objects
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
        return queryset.get(id=post_id)

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
