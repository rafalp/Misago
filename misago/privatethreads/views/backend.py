from typing import Iterable

from django.db.models import QuerySet
from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import pgettext

from ...permissions.privatethreads import (
    check_private_threads_permission,
    check_see_private_thread_permission,
    check_see_private_thread_post_permission,
    filter_private_thread_posts_queryset,
)
from ...permissions.proxy import UserPermissionsProxy
from ...threads.models import Post, Thread
from ...threads.views.backend import ViewBackend
from ...threadupdates.models import ThreadUpdate
from ..members import get_private_thread_members
from ..postfeed import PrivateThreadPostFeed


class PrivateThreadViewBackend(ViewBackend):
    thread_url_name: str = "misago:private-thread"
    thread_post_url_name: str = "misago:private-thread-post"
    thread_post_edits_url_name: str = "misago:private-thread-post-edits"
    thread_post_unapproved_url_name: str = "misago:private-thread-post-unapproved"
    thread_post_last_url_name: str = "misago:private-thread-post-last"

    # Querysets and DB getters

    def get_thread(
        self,
        request: HttpRequest,
        thread_id: int,
        annotate_read_time: bool = False,
        select_related: bool | Iterable[str] = ("category",),
        select_members: bool = False,
        for_update: bool = False,
    ) -> Thread:
        check_private_threads_permission(request.user_permissions)

        thread = super().get_thread(
            request, thread_id, annotate_read_time, select_related, for_update
        )
        if select_members:
            owner, members = get_private_thread_members(thread)
            thread.owner_cache = owner
            thread.members_cache = members

        check_see_private_thread_permission(request.user_permissions, thread)
        return thread

    def get_posts_queryset(
        self,
        request: HttpRequest,
        thread: Thread,
        select_related: bool | Iterable[str] = False,
        for_update: bool = False,
    ) -> QuerySet:
        queryset = super().get_posts_queryset(
            request, thread, select_related, for_update
        )
        return filter_private_thread_posts_queryset(
            request.user_permissions, thread, queryset
        )

    def get_post(
        self,
        request: HttpRequest,
        thread: Thread,
        post_id: int,
        select_related: bool | Iterable[str] = False,
        for_content: bool = False,
        for_update: bool = False,
    ) -> Post:
        post = super().get_post(
            request, thread, post_id, select_related, for_content, for_update
        )
        if for_content:
            check_see_private_thread_post_permission(
                request.user_permissions, thread, post
            )
        return post

    # Thread utils

    def get_breadcrumbs(
        self, request: HttpRequest, thread: Thread, full: bool = True
    ) -> list[dict]:
        breadcrumbs = [
            {
                "type": "home",
                "url": reverse("misago:index"),
                "label": pgettext("breadcrumb label", "Home"),
            },
            {
                "type": "private_threads",
                "url": reverse("misago:private-threads"),
                "label": pgettext("breadcrumb label", "Private threads"),
            },
        ]

        if full:
            breadcrumbs.append(
                {
                    "type": "thread",
                    "url": self.get_thread_url(thread),
                    "label": thread.title,
                }
            )

        return breadcrumbs

    def has_moderator_permission(
        self, user_permissions: UserPermissionsProxy, thread: Thread
    ) -> bool:
        return user_permissions.is_private_threads_moderator

    # Post utils

    def get_post_feed(
        self,
        request: HttpRequest,
        thread: Thread,
        posts: list[Post],
        thread_updates: list[ThreadUpdate] | None = None,
    ) -> PrivateThreadPostFeed:
        post_feed = PrivateThreadPostFeed(request, thread, posts, thread_updates)

        if self.has_moderator_permission(request, thread):
            post_feed.set_moderation(True)

        return post_feed

    # URLs

    def get_thread_parent_url(self, request: HttpRequest, thread: Thread) -> str:
        return reverse("misago:private-threads")


private_thread_backend = PrivateThreadViewBackend()
