from datetime import datetime
from typing import TYPE_CHECKING

from django.db.models import QuerySet
from django.http import HttpRequest
from django.urls import reverse

from ...categories.models import Category
from ...permissions.checkutils import check_permissions
from ...permissions.privatethreads import (
    check_edit_private_thread_permission,
    check_reply_private_thread_permission,
)
from ...posting.formsets import (
    PrivateThreadReplyFormset,
    get_private_thread_reply_formset,
)
from ...readtracker.privatethreads import unread_private_threads_exist
from ...threads.models import Thread
from ...threads.views.detail import DetailView
from ..hooks import (
    get_private_thread_detail_view_context_data_hook,
    get_private_thread_detail_view_posts_queryset_hook,
    get_private_thread_detail_view_thread_queryset_hook,
)
from .backend import private_thread_backend
from .generic import PrivateThreadView
from .members import get_private_thread_members_context_data

if TYPE_CHECKING:
    from ...users.models import User


class PrivateThreadDetailView(DetailView, PrivateThreadView):
    backend = private_thread_backend

    thread_get_members = True
    template_name: str = "misago/private_thread/index.html"
    template_partial_name: str = "misago/private_thread/partial.html"

    def get_thread_queryset(self, request: HttpRequest) -> Thread:
        return get_private_thread_detail_view_thread_queryset_hook(
            super().get_thread_queryset, request
        )

    def get_context_data(
        self, request: HttpRequest, thread: Thread, page: int | None = None
    ) -> dict:
        return get_private_thread_detail_view_context_data_hook(
            self.get_context_data_action, request, thread, page
        )

    def get_context_data_action(
        self, request: HttpRequest, thread: Thread, page: int | None = None
    ) -> dict:
        context = super().get_context_data_action(request, thread, page)
        context["members"] = self.get_thread_members_context_data(request, thread)

        return context

    def get_thread_members_context_data(
        self, request: HttpRequest, thread: Thread
    ) -> dict:
        return get_private_thread_members_context_data(
            request, thread, self.owner, self.members
        )

    def get_thread_posts_queryset(
        self, request: HttpRequest, thread: Thread
    ) -> QuerySet:
        return get_private_thread_detail_view_posts_queryset_hook(
            super().get_thread_posts_queryset, request, thread
        )

    def allow_edit_thread(self, request: HttpRequest, thread: Thread) -> bool:
        if request.user.is_anonymous:
            return False

        with check_permissions() as can_edit_thread:
            check_edit_private_thread_permission(request.user_permissions, thread)

        return can_edit_thread

    def update_thread_read_time(
        self,
        request: HttpRequest,
        thread: Thread,
        read_time: datetime,
    ):
        unread_private_threads = request.user.unread_private_threads
        if read_time >= thread.last_posted_at and request.user.unread_private_threads:
            request.user.unread_private_threads -= 1

        super().update_thread_read_time(request, thread, read_time)

        if request.user.unread_private_threads != unread_private_threads:
            request.user.save(update_fields=["unread_private_threads"])

    def is_category_read(
        self,
        request: HttpRequest,
        category: Category,
        category_read_time: datetime | None,
    ) -> bool:
        return not unread_private_threads_exist(request, category, category_read_time)

    def mark_category_read(
        self,
        user: "User",
        category: Category,
        *,
        force_update: bool,
    ):
        super().mark_category_read(user, category, force_update=force_update)

        user.clear_unread_private_threads()

    def check_reply_thread_permission(self, request: HttpRequest, thread: Thread):
        check_reply_private_thread_permission(request.user_permissions, thread)

    def get_reply_url(self, request: HttpRequest, thread: Thread) -> str:
        return reverse(
            "misago:private-thread-reply",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )

    def get_reply_formset(
        self, request: HttpRequest, thread: Thread
    ) -> PrivateThreadReplyFormset:
        return get_private_thread_reply_formset(request, thread)
