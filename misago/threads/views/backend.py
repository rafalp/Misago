from abc import ABC, abstractmethod
from typing import Iterable

from django.db.models import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import pgettext

from ...permissions.proxy import UserPermissionsProxy
from ...permissions.threads import (
    check_see_thread_permission,
    check_see_thread_post_permission,
    filter_thread_posts_queryset,
    filter_thread_updates_queryset,
)
from ...readtracker.tracker import (
    threads_annotate_user_readcategory_time,
    threads_select_related_user_readthread,
)
from ...threadupdates.models import ThreadUpdate
from ..models import Post, Thread
from ..paginator import ThreadPostsPaginator
from ..postfeed import PostFeed, ThreadPostFeed


class ViewBackend(ABC):
    thread_url_name: str
    thread_post_url_name: str
    thread_post_edits_url_name: str
    thread_post_unapproved_url_name: str
    thread_post_last_url_name: str

    post_edits_modal_template: str = "misago/thread/post_edits_modal.html"
    post_likes_modal_template: str = "misago/thread/post_likes_modal.html"

    # Querysets and DB getters

    @abstractmethod
    def get_thread(
        self,
        request: HttpRequest,
        thread_id: int,
        *,
        annotate_read_time: bool = False,
        select_related: bool | Iterable[str] = ("category",),
        for_update: bool = False,
    ) -> Thread:
        queryset = Thread.objects
        if annotate_read_time:
            queryset = threads_annotate_user_readcategory_time(queryset, request.user)
            queryset = threads_select_related_user_readthread(queryset, request.user)
        if select_related is True:
            queryset = queryset.select_related()
        elif select_related:
            queryset = queryset.select_related(*select_related)
        if for_update:
            queryset = queryset.select_for_update()

        try:
            return queryset.get(id=thread_id)
        except Thread.DoesNotExist:
            raise Http404()

    @abstractmethod
    def get_posts_queryset(
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
    def get_post(
        self,
        request: HttpRequest,
        thread: Thread,
        post_id: int,
        *,
        select_related: bool | Iterable[str] = False,
        for_content: bool = False,
        for_update: bool = False,
    ) -> Post:
        queryset = self.get_posts_queryset(
            request,
            thread,
            select_related=select_related,
            for_update=for_update,
        )
        try:
            post = queryset.get(id=post_id)
            if Thread.category.is_cached(thread):
                post.category = thread.category
            post.thread = thread
            return post
        except Post.DoesNotExist:
            raise Http404()

    def get_post_number(self, request: HttpRequest, post: Post) -> int:
        queryset = self.get_posts_queryset(request, post.thread).filter(id__lte=post.id)
        return queryset.count()

    def get_thread_updates_queryset(
        self,
        request: HttpRequest,
        thread: Thread,
        *,
        select_related: bool | Iterable[str] = False,
    ) -> QuerySet:
        queryset = ThreadUpdate.objects.filter(thread=thread).order_by("-id")
        if select_related is True:
            queryset = queryset.select_related()
        elif select_related:
            queryset = queryset.select_related(*select_related)
        return queryset

    def get_thread_update(
        self,
        request: HttpRequest,
        thread: Thread,
        thread_update_id: int,
        *,
        select_related: bool | Iterable[str] = False,
    ) -> ThreadUpdate:
        queryset = self.get_thread_updates_queryset(
            request, thread, select_related=select_related
        )
        try:
            thread_update = queryset.get(id=thread_update_id)
        except ThreadUpdate.DoesNotExist:
            raise Http404()

        thread_update.category = thread.category
        thread_update.thread = thread

        return thread_update

    # Thread utils

    @abstractmethod
    def get_breadcrumbs(
        self, request: HttpRequest, thread: Thread, full: bool = True
    ) -> list[dict]:
        pass

    @abstractmethod
    def has_moderator_permission(
        self, user_permissions: UserPermissionsProxy, thread: Thread
    ) -> bool:
        pass

    # Post utils

    @abstractmethod
    def get_post_feed(
        self,
        request: HttpRequest,
        thread: Thread,
        posts: list[Post],
        thread_updates: list[ThreadUpdate] | None = None,
    ) -> PostFeed:
        pass

    def get_posts_paginator(
        self,
        request: HttpRequest,
        queryset: QuerySet,
    ) -> ThreadPostsPaginator:
        return ThreadPostsPaginator(
            queryset.order_by("id"),
            request.settings.posts_per_page,
            request.settings.posts_per_page_orphans,
        )

    def get_post_redirect(
        self,
        request: HttpRequest,
        post: Post,
        permanent: bool = False,
    ) -> HttpResponse:
        queryset = self.get_posts_queryset(request, post.thread)
        paginator = self.get_posts_paginator(request, queryset)
        offset = queryset.filter(id__lt=post.id).count()
        page = paginator.get_item_page(offset)

        return redirect(
            self.get_post_redirect_url(post, page),
            permanent=permanent,
        )

    # URLs

    @abstractmethod
    def get_thread_parent_url(self, request: HttpRequest, thread: Thread) -> str:
        pass

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

    def get_post_url(self, post: Post) -> str:
        return reverse(
            self.thread_post_url_name,
            kwargs={
                "thread_id": post.thread_id,
                "slug": post.thread.slug,
                "post_id": post.id,
            },
        )

    def get_post_edits_url(
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

    def get_post_unapproved_url(self, thread: Thread) -> str:
        return reverse(
            self.thread_post_unapproved_url_name,
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )

    def get_post_last_url(self, thread: Thread) -> str:
        return reverse(
            self.thread_post_last_url_name,
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )

    def get_post_redirect_url(self, post: Post, page: int = 1) -> str:
        thread_url = self.get_thread_url(post.thread, page)
        return f"{thread_url}#post-{post.id}"


class ThreadViewBackend(ViewBackend):
    thread_url_name: str = "misago:thread"
    thread_post_url_name: str = "misago:thread-post"
    thread_post_edits_url_name: str = "misago:thread-post-edits"
    thread_post_unapproved_url_name: str = "misago:thread-post-unapproved"
    thread_post_last_url_name: str = "misago:thread-post-last"

    # Querysets and DB getters

    def get_thread(
        self,
        request: HttpRequest,
        thread_id: int,
        *,
        annotate_read_time: bool = False,
        select_related: bool | Iterable[str] = ("category",),
        for_update: bool = False,
    ) -> Thread:
        thread = super().get_thread(
            request,
            thread_id,
            annotate_read_time=annotate_read_time,
            select_related=select_related,
            for_update=for_update,
        )

        check_see_thread_permission(request.user_permissions, thread.category, thread)

        return thread

    def get_posts_queryset(
        self,
        request: HttpRequest,
        thread: Thread,
        *,
        select_related: bool | Iterable[str] = False,
        for_update: bool = False,
    ) -> QuerySet:
        queryset = super().get_posts_queryset(
            request,
            thread,
            select_related=select_related,
            for_update=for_update,
        )
        return filter_thread_posts_queryset(request.user_permissions, thread, queryset)

    def get_post(
        self,
        request: HttpRequest,
        thread: Thread,
        post_id: int,
        *,
        select_related: bool | Iterable[str] = False,
        for_content: bool = False,
        for_update: bool = False,
    ) -> Post:
        post = super().get_post(
            request,
            thread,
            post_id,
            select_related=select_related,
            for_content=for_content,
            for_update=for_update,
        )

        if for_content:
            check_see_thread_post_permission(
                request.user_permissions, thread.category, thread, post
            )

        return post

    def get_thread_updates_queryset(
        self,
        request: HttpRequest,
        thread: Thread,
        *,
        select_related: bool | Iterable[str] = False,
    ) -> QuerySet:
        queryset = super().get_thread_updates_queryset(
            request,
            thread,
            select_related=select_related,
        )
        return filter_thread_updates_queryset(
            request.user_permissions, thread, queryset
        )

    # Thread utils

    def get_breadcrumbs(
        self, request: HttpRequest, thread: Thread, full: bool = True
    ) -> list[dict]:
        breadcrumbs = [
            {
                "type": "home",
                "label": pgettext("breadcrumb label", "Home"),
                "url": reverse("misago:index"),
            },
        ]

        for category in request.categories.get_category_path(thread.category_id):
            breadcrumbs.append(
                {
                    "type": "category",
                    "label": category["name"],
                    "short_label": category["short_name"],
                    "color": category["color"],
                    "css_class": category["css_class"],
                    "url": category["url"],
                }
            )

        if full:
            breadcrumbs.append(
                {
                    "type": "thread",
                    "label": thread.title,
                    "url": self.get_thread_url(thread),
                }
            )

        return breadcrumbs

    def has_moderator_permission(
        self, user_permissions: UserPermissionsProxy, thread: Thread
    ) -> bool:
        return user_permissions.is_category_moderator(thread.category_id)

    # Post utils

    def get_post_feed(
        self,
        request: HttpRequest,
        thread: Thread,
        posts: list[Post],
        thread_updates: list[ThreadUpdate] | None = None,
    ) -> PostFeed:
        post_feed = ThreadPostFeed(request, thread, posts, thread_updates)

        if self.has_moderator_permission(request.user_permissions, thread):
            post_feed.set_moderation(True)

        return post_feed

    # URLs

    def get_thread_parent_url(self, request: HttpRequest, thread: Thread) -> str:
        return reverse(
            "misago:category-thread-list",
            kwargs={
                "category_id": thread.category_id,
                "slug": thread.category.slug,
            },
        )


thread_backend = ThreadViewBackend()
