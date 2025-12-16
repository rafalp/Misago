from typing import TYPE_CHECKING, Optional

from django.db.models import QuerySet
from django.http import HttpRequest

from ...permissions.privatethreads import (
    check_private_threads_permission,
    check_see_private_thread_permission,
    filter_private_thread_posts_queryset,
    filter_private_thread_updates_queryset,
)
from ...threads.views.generic import GenericView
from ...threads.models import Post, Thread
from ...threads.postfeed import PostFeed
from ...threadupdates.models import ThreadUpdate
from ..members import get_private_thread_members
from ..postfeed import PrivateThreadPostFeed

if TYPE_CHECKING:
    from ...users.models import User


class PrivateThreadView(GenericView):
    thread_url_name: str = "misago:private-thread"
    thread_post_url_name: str = "misago:private-thread-post"

    thread_get_members: bool = False

    owner: Optional["User"]
    members: list["User"]

    def __init__(self, *args, **kwargs):
        self.owner = None
        self.members = []

        super().__init__(*args, **kwargs)

    def get_thread(
        self, request: HttpRequest, thread_id: int, for_update: bool = False
    ) -> Thread:
        check_private_threads_permission(request.user_permissions)

        thread = super().get_thread(request, thread_id, for_update)
        if self.thread_get_members:
            self.owner, self.members = get_private_thread_members(thread)

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

    def get_post_feed(
        self,
        request: HttpRequest,
        thread: Thread,
        posts: list[Post],
        thread_updates: list[ThreadUpdate] | None = None,
    ) -> PostFeed:
        return PrivateThreadPostFeed(request, thread, posts, thread_updates)

    def get_moderator_status(self, request: HttpRequest, thread: Thread) -> bool:
        return request.user_permissions.is_private_threads_moderator

    def get_owner_status(self, request: HttpRequest, thread: Thread) -> bool:
        if not self.owner or not request.user.is_authenticated:
            return False

        return self.owner.id == request.user.id
