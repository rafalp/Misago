from typing import Iterable

from django.db.models import QuerySet
from django.http import HttpRequest

from ...permissions.privatethreads import (
    check_private_threads_permission,
    check_see_private_thread_permission,
    check_see_private_thread_post_permission,
    filter_private_thread_posts_queryset,
)
from ...permissions.proxy import UserPermissionsProxy
from ...threads.models import Post, Thread
from ...threads.views.backend import ViewBackend
from ..members import get_private_thread_members


class PrivateThreadViewBackend(ViewBackend):
    thread_url_name: str = "misago:private-thread"
    thread_post_url_name: str = "misago:private-thread-post"
    thread_post_edits_url_name: str = "misago:private-thread-post-edits"

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
        return filter_private_thread_posts_queryset(
            request.user_permissions, thread, queryset
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
        post = super().get_thread_post(
            request, thread, post_id, select_related, for_content, for_update
        )
        if for_content:
            check_see_private_thread_post_permission(
                request.user_permissions, thread, post
            )
        return post

    def get_thread_moderator_permission(
        self, user_permissions: UserPermissionsProxy, thread: Thread
    ) -> bool:
        return user_permissions.is_private_threads_moderator


private_thread_backend = PrivateThreadViewBackend()
