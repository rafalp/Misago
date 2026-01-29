from abc import ABC, abstractmethod
from typing import Iterable

from django.db.models import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from ...permissions.proxy import UserPermissionsProxy
from ...permissions.threads import (
    check_see_thread_permission,
    check_see_thread_post_permission,
    filter_thread_posts_queryset,
)
from ...readtracker.tracker import (
    threads_annotate_user_readcategory_time,
    threads_select_related_user_readthread,
)
from ..paginator import ThreadPostsPaginator
from ..models import Post, Thread


class ViewBackend(ABC):
    thread_url_name: str
    thread_post_url_name: str
    thread_post_edits_url_name: str

    post_edits_modal_template: str = "misago/thread/post_edits_modal.html"
    post_likes_modal_template: str = "misago/thread/post_likes_modal.html"

    @abstractmethod
    def get_thread(
        self,
        request: HttpRequest,
        thread_id: int,
        annotate_read_time: bool = False,
        select_related: bool | Iterable[str] = ("category",),
        for_update: bool = False,
    ) -> Thread:
        queryset = self.get_thread_queryset(request, annotate_read_time, select_related)
        if for_update:
            queryset = queryset.select_for_update()

        try:
            return queryset.get(id=thread_id)
        except Thread.DoesNotExist:
            raise Http404()

    def get_thread_queryset(
        self,
        request: HttpRequest,
        annotate_read_time: bool = False,
        select_related: bool | Iterable[str] = False,
    ) -> QuerySet:
        queryset = Thread.objects
        if annotate_read_time:
            queryset = threads_annotate_user_readcategory_time(queryset, request.user)
            queryset = threads_select_related_user_readthread(queryset, request.user)
        if select_related is True:
            queryset = queryset.select_related()
        elif select_related:
            queryset = queryset.select_related(*select_related)
        return queryset

    @abstractmethod
    def get_thread_posts_queryset(
        self,
        request: HttpRequest,
        thread: Thread,
        select_related: bool | Iterable[str] = False,
        for_update: bool = False,
    ) -> QuerySet:
        queryset = Post.objects.filter(thread=thread).order_by("id")
        if select_related is True:
            queryset = queryset.select_related()
        elif select_related:
            queryset = queryset.select_related(*select_related)
        if for_update:
            queryset = queryset.select_for_update()
        return queryset

    @abstractmethod
    def get_thread_post(
        self,
        request: HttpRequest,
        thread: Thread,
        post_id: int,
        select_related: bool | Iterable[str] = False,
        for_content: bool = False,
        for_update: bool = False,
    ) -> Post:
        queryset = self.get_thread_posts_queryset(
            request, thread, select_related, for_update
        )
        try:
            post = queryset.get(id=post_id)
            if Thread.category.is_cached(thread):
                post.category = thread.category
            post.thread = thread
            return post
        except Post.DoesNotExist:
            raise Http404()

    def get_thread_post_number(self, request: HttpRequest, post: Post) -> int:
        queryset = self.get_thread_posts_queryset(request, post.thread).filter(
            id__lte=post.id
        )
        return queryset.count()

    def get_thread_posts_paginator(
        self,
        request: HttpRequest,
        queryset: QuerySet,
    ) -> ThreadPostsPaginator:
        return ThreadPostsPaginator(
            queryset.order_by("id"),
            request.settings.posts_per_page,
            request.settings.posts_per_page_orphans,
        )

    def get_thread_url(
        self,
        thread: Thread,
        page: int = 1,
    ) -> str:
        if page and page > 1:
            return reverse(
                self.thread_url_name,
                kwargs={
                    "thread_id": thread.id,
                    "slug": thread.slug,
                    "page": page,
                },
            )

        return reverse(
            self.thread_url_name,
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )

    def get_thread_post_url(self, post: Post) -> str:
        return reverse(
            self.thread_post_url_name,
            kwargs={
                "thread_id": post.thread_id,
                "slug": post.thread.slug,
                "post_id": post.id,
            },
        )

    def get_thread_post_edits_url(
        self,
        post: Post,
        page: int | None = None,
    ) -> str:
        if page:
            return reverse(
                self.thread_post_edits_url_name,
                kwargs={
                    "thread_id": post.thread_id,
                    "slug": post.thread.slug,
                    "post_id": post.id,
                    "page": page,
                },
            )

        return reverse(
            self.thread_post_edits_url_name,
            kwargs={
                "thread_id": post.thread_id,
                "slug": post.thread.slug,
                "post_id": post.id,
            },
        )

    def get_thread_post_redirect(
        self,
        request: HttpRequest,
        post: Post,
        permanent: bool = False,
    ) -> HttpResponse:
        queryset = self.get_thread_posts_queryset(request, post.thread)
        paginator = self.get_thread_posts_paginator(request, queryset)
        offset = queryset.filter(id__lt=post.id).count()
        page = paginator.get_item_page(offset)

        return redirect(
            self.get_thread_post_redirect_url(post, page),
            permanent=permanent,
        )

    def get_thread_post_redirect_url(self, post: Post, page: int = 1) -> str:
        thread_url = self.get_thread_url(post.thread, page)
        return f"{thread_url}#post-{post.id}"

    @abstractmethod
    def get_thread_moderator_permission(
        self, user_permissions: UserPermissionsProxy, thread: Thread
    ) -> bool:
        pass


class ThreadViewBackend(ViewBackend):
    thread_url_name: str = "misago:thread"
    thread_post_url_name: str = "misago:thread-post"
    thread_post_edits_url_name: str = "misago:thread-post-edits"

    def get_thread(
        self,
        request: HttpRequest,
        thread_id: int,
        annotate_read_time: bool = False,
        select_related: bool | Iterable[str] = ("category",),
        for_update: bool = False,
    ) -> Thread:
        thread = super().get_thread(
            request, thread_id, annotate_read_time, select_related, for_update
        )
        check_see_thread_permission(request.user_permissions, thread.category, thread)
        return thread

    def get_thread_posts_queryset(
        self,
        request: HttpRequest,
        thread: Thread,
        select_related: bool | Iterable[str] = False,
        for_update: bool = False,
    ) -> QuerySet:
        queryset = super().get_thread_posts_queryset(
            request, thread, select_related, for_update
        )
        return filter_thread_posts_queryset(request.user_permissions, thread, queryset)

    def get_thread_post(
        self,
        request: HttpRequest,
        thread: Thread,
        post_id: int,
        select_related: bool | Iterable[str] = False,
        for_content: bool = False,
        for_update: bool = False,
    ) -> Post:
        post = super().get_thread_post(
            request, thread, post_id, select_related, for_content, for_update
        )
        if for_content:
            check_see_thread_post_permission(
                request.user_permissions, thread.category, thread, post
            )
        return post

    def get_thread_moderator_permission(
        self, user_permissions: UserPermissionsProxy, thread: Thread
    ) -> bool:
        return user_permissions.is_category_moderator(thread.category_id)


thread_backend = ThreadViewBackend()
