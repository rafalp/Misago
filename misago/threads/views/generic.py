from typing import Any, Iterable

from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View

from ...permissions.threads import check_see_thread_permission
from ..models import Post, Thread, ThreadParticipant


class GenericView(View):
    thread_select_related: Iterable[str] | True | None = None
    post_select_related: Iterable[str] | None = None

    def get_thread(self, request: HttpRequest, thread_id: int) -> Thread:
        queryset = Thread.objects
        if self.thread_select_related is True:
            queryset = queryset.select_related()
        elif self.thread_select_related:
            queryset = queryset.select_related(*self.thread_select_related)

        return get_object_or_404(queryset, id=thread_id)

    def get_thread_posts_queryset(
        self, request: HttpRequest, thread: Thread
    ) -> QuerySet:
        raise NotImplementedError()

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
        return Paginator(
            queryset.order_by("id"),
            request.settings.posts_per_page,
            request.settings.posts_per_page_orphans,
        )


class ThreadView(GenericView):
    thread_select_related: Iterable[str] | True | None = ("category",)

    def get_thread(self, request: HttpRequest, thread_id: int) -> Thread:
        thread = super().get_thread(request, thread_id)
        check_see_thread_permission(request.user_permissions, thread.category, thread)
        return thread


class PrivateThreadView(GenericView):
    def get_thread_participants(
        self,
        request: HttpRequest,
        thread: Thread,
    ) -> dict[int, ThreadParticipant]:
        pass
