from typing import Iterable

from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.urls import reverse
from django.views import View

from ...categories.models import Category
from ...permissions.proxy import UserPermissionsProxy
from ...permissions.threads import (
    check_see_thread_permission,
    filter_thread_posts_queryset,
    filter_thread_updates_queryset,
)
from ...readtracker.tracker import (
    threads_annotate_user_readcategory_time,
    threads_select_related_user_readthread,
)
from ...threadevents.models import ThreadEvent
from ..models import Post, Thread
from ..nexturl import get_next_thread_url
from ..paginator import ThreadPostsPaginator
from ..postfeed import PostFeed, ThreadPostFeed
from .backend import ViewBackend


class GenericThreadView(View):
    backend: ViewBackend

    # Querysets and DB getters

    def get_thread(
        self,
        request: HttpRequest,
        thread_id: int,
        *,
        annotate_read_time: bool = False,
        select_related: bool | Iterable[str] | None = None,
        for_update: bool = False,
        **kwargs,
    ) -> Thread:
        return self.backend.get_thread(
            request,
            thread_id,
            annotate_read_time=annotate_read_time,
            select_related=select_related,
            for_update=for_update,
            **kwargs,
        )

    def get_posts_queryset(
        self,
        request: HttpRequest,
        thread: Thread,
        *,
        select_related: bool | Iterable[str] = False,
        for_update: bool = False,
        **kwargs,
    ) -> QuerySet:
        return self.backend.get_posts_queryset(
            request,
            thread,
            select_related=select_related,
            for_update=for_update,
            **kwargs,
        )

    def get_post(
        self,
        request: HttpRequest,
        thread: Thread,
        post_id: int,
        *,
        select_related: bool | Iterable[str] = False,
        for_content: bool = False,
        for_update: bool = False,
        **kwargs,
    ) -> Post:
        return self.backend.get_post(
            request,
            thread,
            post_id,
            select_related=select_related,
            for_content=for_content,
            for_update=for_update,
            **kwargs,
        )

    def get_thread_updates_queryset(
        self,
        request: HttpRequest,
        thread: Thread,
        *,
        select_related: bool | Iterable[str] = False,
    ) -> QuerySet:
        return self.backend.get_thread_events_queryset(
            request,
            thread,
            select_related=select_related,
        )

    def get_thread_update(
        self,
        request: HttpRequest,
        thread: Thread,
        thread_event_id: int,
        *,
        select_related: bool | Iterable[str] = False,
    ) -> ThreadEvent:
        return self.backend.get_thread_event(
            request,
            thread,
            thread_event_id,
            select_related=select_related,
        )

    # Thread utils

    def get_category_breadcrumbs(
        self, request: HttpRequest, category: Category
    ) -> dict:
        return self.backend.get_category_breadcrumbs(request, category)

    def get_thread_breadcrumbs(self, request: HttpRequest, thread: Thread) -> dict:
        return self.backend.get_thread_breadcrumbs(request, thread)

    def has_moderator_permission(
        self, user_permissions: UserPermissionsProxy, thread: Thread
    ) -> bool:
        return self.backend.has_moderator_permission(user_permissions, thread)

    # Post utils

    def get_post_feed(
        self,
        request: HttpRequest,
        thread: Thread,
        posts: list[Post],
        thread_events: list[ThreadEvent] | None = None,
    ) -> PostFeed:
        return self.backend.get_post_feed(request, thread, posts, thread_events)

    def get_posts_paginator(
        self,
        request: HttpRequest,
        queryset: QuerySet,
    ) -> ThreadPostsPaginator:
        return self.backend.get_posts_paginator(request, queryset)

    def get_post_number(self, request: HttpRequest, post: Post) -> int:
        return self.backend.get_post_number(request, post)

    def get_post_redirect(
        self,
        request: HttpRequest,
        post: Post,
        permanent: bool = False,
    ) -> HttpResponse:
        return self.backend.get_post_redirect(request, post, permanent)

    # URLs

    def get_thread_parent_url(self, request: HttpRequest, thread: Thread) -> str:
        return self.backend.get_thread_parent_url(request, thread)

    def get_thread_url(
        self,
        thread: Thread,
        page: int = 1,
    ) -> str:
        return self.backend.get_thread_url(thread, page)

    def get_next_thread_url(
        self, request: HttpRequest, thread: Thread, strip_qs: bool = False
    ) -> str:
        return get_next_thread_url(
            request, thread, self.backend.thread_url_name, strip_qs
        )

    def get_post_url(self, post: Post) -> str:
        return self.backend.get_post_url(post)

    def get_post_edits_url(
        self,
        post: Post,
        page: int | None = None,
    ) -> str:
        return self.backend.get_post_edits_url(post, page)

    def get_post_unapproved_url(self, thread: Thread) -> str:
        return self.backend.get_post_unapproved_url(thread)

    def get_post_last_url(self, thread: Thread) -> str:
        return self.backend.get_post_last_url(thread)

    def get_post_redirect_url(self, post: Post, page: int = 1) -> str:
        return self.backend.get_post_last_url(post, page)
