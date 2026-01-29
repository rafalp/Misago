from typing import Iterable

from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View

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
from ..nexturl import get_next_thread_url
from ..paginator import ThreadPostsPaginator
from ..postfeed import PostFeed, ThreadPostFeed
from .backend import ViewBackend


class GenericThreadView(View):
    backend: ViewBackend

    def get_thread(
        self,
        request: HttpRequest,
        thread_id: int,
        annotate_read_time: bool = False,
        select_related: bool | Iterable[str] = ("category",),
        for_update: bool = False,
    ) -> Thread:
        return self.backend.get_thread(
            request, thread_id, annotate_read_time, select_related, for_update
        )

    def get_thread_queryset(
        self,
        request: HttpRequest,
        annotate_read_time: bool = False,
        select_related: bool | Iterable[str] = False,
    ) -> QuerySet:
        return self.backend.get_thread_posts_queryset(
            request, annotate_read_time, select_related
        )

    def get_thread_posts_queryset(
        self,
        request: HttpRequest,
        thread: Thread,
        select_related: bool | Iterable[str] = False,
        for_update: bool = False,
    ) -> QuerySet:
        return self.backend.get_thread_posts_queryset(
            request, thread, select_related, for_update
        )

    def get_thread_post(
        self,
        request: HttpRequest,
        thread: Thread,
        post_id: int,
        select_related: bool | Iterable[str] = False,
        for_content: bool = False,
        for_update: bool = False,
    ) -> Post:
        return self.backend.get_thread_post(
            request, thread, post_id, select_related, for_content, for_update
        )

    def get_thread_post_number(self, request: HttpRequest, post: Post) -> int:
        return self.backend.get_thread_post_number(request, post)

    def get_thread_posts_paginator(
        self,
        request: HttpRequest,
        queryset: QuerySet,
    ) -> ThreadPostsPaginator:
        return self.backend.get_thread_posts_paginator(request, queryset)

    def get_thread_url(
        self,
        thread: Thread,
        page: int = 1,
    ) -> str:
        return self.backend.get_thread_url(thread, page)

    def get_thread_post_url(self, post: Post) -> str:
        return self.backend.get_thread_post_url(post)

    def get_thread_post_edits_url(
        self,
        post: Post,
        page: int | None = None,
    ) -> str:
        return self.backend.get_thread_post_edits_url(post, page)

    def get_thread_post_redirect(
        self,
        request: HttpRequest,
        post: Post,
        permanent: bool = False,
    ) -> HttpResponse:
        return self.backend.get_thread_post_redirect(request, post, permanent)

    def get_thread_post_redirect_url(self, post: Post, page: int = 1) -> str:
        return self.backend.get_thread_post_redirect_url(post, page)

    def get_thread_moderator_permission(
        self, request: HttpRequest, thread: Thread
    ) -> bool:
        return self.backend.get_thread_moderator_permission(request, thread)


class GenericView(View):
    thread_select_related: Iterable[str] | True | None = None
    thread_annotate_read_time: bool = False
    thread_url_name: str
    thread_post_url_name: str
    post_select_related: Iterable[str] | True | None = None
    thread_update_select_related: Iterable[str] | True | None = None
    next_page: str = "next"

    def get_thread(
        self, request: HttpRequest, thread_id: int, for_update: bool = False
    ) -> Thread:
        if for_update:
            queryset = Thread.objects.select_for_update()
        else:
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
        self,
        request: HttpRequest,
        thread: Thread,
        post_id: int,
        for_update: bool = False,
    ) -> Post:
        queryset = self.get_thread_posts_queryset(request, thread)
        if for_update:
            queryset = queryset.select_for_update()
        else:
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
        return ThreadPostsPaginator(
            queryset.order_by("id"),
            request.settings.posts_per_page,
            request.settings.posts_per_page_orphans,
        )

    def get_post_feed(
        self,
        request: HttpRequest,
        thread: Thread,
        posts: list[Post],
        thread_updates: list[ThreadUpdate] | None = None,
    ) -> PostFeed:
        raise NotImplementedError()

    def get_thread_post_number(
        self, request: HttpRequest, thread: Thread, post: Post
    ) -> int:
        queryset = self.get_thread_posts_queryset(request, thread)
        return queryset.filter(id__lte=post.id).count()

    def get_thread_url(self, thread: Thread, page: int | None = None) -> str:
        """Return the absolute URL to a thread."""
        if page and page > 1:
            return reverse(
                self.thread_url_name,
                kwargs={"thread_id": thread.id, "slug": thread.slug, "page": page},
            )

        return reverse(
            self.thread_url_name,
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )

    def get_thread_post_url(self, thread: Thread, post: Post) -> str:
        return reverse(
            self.thread_post_url_name,
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )

    def get_next_thread_url(
        self, request: HttpRequest, thread: Thread, strip_qs: bool = False
    ) -> str:
        """
        Attempt to return an absolute URL to a thread based on either the POST
        or GET query dict, falling back to get_thread_url if unavailable.
        """
        return get_next_thread_url(request, thread, self.thread_url_name, strip_qs)

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

    def get_moderator_status(self, request: HttpRequest, thread: Thread) -> bool:
        return False


class ThreadView(GenericView):
    thread_select_related: Iterable[str] | True | None = ("category",)
    thread_url_name: str = "misago:thread"
    thread_post_url_name: str = "misago:thread-post"

    def get_thread(
        self, request: HttpRequest, thread_id: int, for_update: bool = False
    ) -> Thread:
        thread = super().get_thread(request, thread_id, for_update)
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

    def get_post_feed(
        self,
        request: HttpRequest,
        thread: Thread,
        posts: list[Post],
        thread_updates: list[ThreadUpdate] | None = None,
    ) -> PostFeed:
        return ThreadPostFeed(request, thread, posts, thread_updates)

    def get_moderator_status(self, request: HttpRequest, thread: Thread) -> bool:
        return request.user_permissions.is_category_moderator(thread.category_id)
