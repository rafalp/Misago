from datetime import datetime
from typing import TYPE_CHECKING, Any

from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from ...categories.models import Category
from ...core.exceptions import OutdatedSlug
from ...notifications.threads import update_watched_thread_read_time
from ...permissions.checkutils import check_permissions
from ...permissions.privatethreads import (
    check_edit_private_thread_permission,
    check_reply_private_thread_permission,
)
from ...permissions.threads import (
    check_edit_thread_permission,
    check_reply_thread_permission,
)
from ...posting.formsets import (
    ReplyPrivateThreadFormset,
    ReplyThreadFormset,
    get_reply_private_thread_formset,
    get_reply_thread_formset,
)
from ...readtracker.tracker import (
    get_unread_posts,
    mark_category_read,
    mark_thread_read,
)
from ...readtracker.privatethreads import unread_private_threads_exist
from ...readtracker.threads import is_category_read
from ..hooks import (
    get_private_thread_replies_page_context_data_hook,
    get_private_thread_replies_page_posts_queryset_hook,
    get_private_thread_replies_page_thread_queryset_hook,
    get_thread_replies_page_context_data_hook,
    get_thread_replies_page_posts_queryset_hook,
    get_thread_replies_page_thread_queryset_hook,
)
from ..models import Post, Thread
from .generic import PrivateThreadView, ThreadView

if TYPE_CHECKING:
    from ...users.models import User
else:
    User = get_user_model()


class PageOutOfRangeError(Exception):
    redirect_to: str

    def __init__(self, redirect_to: str):
        self.redirect_to = redirect_to


class RepliesView(View):
    thread_annotate_read_time: bool = True
    template_name: str
    template_partial_name: str
    feed_template_name: str = "misago/posts_feed/index.html"
    feed_post_template_name: str = "misago/posts_feed/post.html"
    reply_error_template_name: str = "misago/thread/reply_error.html"
    reply_template_name: str = "misago/quick_reply/form.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            return super().dispatch(request, *args, **kwargs)
        except PageOutOfRangeError as exc:
            return redirect(exc.redirect_to)

    def get(
        self, request: HttpRequest, id: int, slug: str, page: int | None = None
    ) -> HttpResponse:
        thread = self.get_thread(request, id)

        if not request.is_htmx and thread.slug != slug:
            raise OutdatedSlug(thread)

        context = self.get_context_data(request, thread, page)

        if request.is_htmx:
            template_name = self.template_partial_name
        else:
            template_name = self.template_name

        return render(request, template_name, context)

    def get_context_data(
        self, request: HttpRequest, thread: Thread, page: int | None = None
    ) -> dict:
        return self.get_context_data_action(request, thread, page)

    def get_context_data_action(
        self, request: HttpRequest, thread: Thread, page: int | None = None
    ) -> dict:
        return {
            "thread": thread,
            "thread_url": self.get_thread_url(thread),
            "feed": self.get_posts_feed_data(request, thread, page),
            "reply": self.get_reply_context_data(request, thread),
        }

    def get_posts_feed_data(
        self, request: HttpRequest, thread: Thread, page: int | None = None
    ) -> dict:
        queryset = self.get_thread_posts_queryset(request, thread)
        paginator = self.get_thread_posts_paginator(request, queryset)

        if page and page > paginator.num_pages:
            if not request.is_htmx:
                raise PageOutOfRangeError(
                    self.get_thread_url(thread, paginator.num_pages)
                )

            page = paginator.num_pages

        page_obj = paginator.get_page(page)
        posts = list(page_obj.object_list)

        feed = self.get_posts_feed(request, thread, posts)
        feed.set_counter_start(page_obj.start_index() - 1)

        unread = get_unread_posts(request, thread, posts)
        feed.set_unread_posts(unread)

        allow_edit_thread = self.allow_edit_thread(request, thread)
        feed.set_allow_edit_thread(allow_edit_thread)

        if unread:
            self.update_thread_read_time(request, thread, posts[-1].posted_on)

        if request.user.is_authenticated and request.user.unread_notifications:
            self.read_user_notifications(request.user, posts)

        return feed.get_context_data({"paginator": page_obj})

    def allow_edit_thread(self, request: HttpRequest, thread: Thread) -> bool:
        return False

    def update_thread_read_time(
        self,
        request: HttpRequest,
        thread: Thread,
        read_time: datetime,
    ):
        mark_thread_read(request.user, thread, read_time)
        update_watched_thread_read_time(request.user, thread, read_time)

        if self.is_category_read(request, thread.category, thread.category_read_time):
            self.mark_category_read(
                request.user,
                thread.category,
                force_update=bool(thread.category_read_time),
            )

    def is_category_read(
        self,
        request: HttpRequest,
        category: Category,
        category_read_time: datetime | None,
    ) -> bool:
        raise NotImplementedError()

    def mark_category_read(
        self,
        user: "User",
        category: Category,
        *,
        force_update: bool,
    ):
        mark_category_read(user, category, force_update=force_update)

    def read_user_notifications(self, user: "User", posts: list[Post]):
        updated_notifications = user.notification_set.filter(
            post__in=posts, is_read=False
        ).update(is_read=True)

        if updated_notifications:
            new_unread_notifications = max(
                [0, user.unread_notifications - updated_notifications]
            )

            if user.unread_notifications != new_unread_notifications:
                user.unread_notifications = new_unread_notifications
                user.save(update_fields=["unread_notifications"])

    def get_reply_context_data(self, request: HttpRequest, thread: Thread) -> dict:
        try:
            self.check_reply_thread_permission(request, thread)
        except PermissionDenied as exc:
            return {
                "permission": False,
                "template_name": self.reply_error_template_name,
                "error": exc,
            }

        return {
            "permission": True,
            "template_name": self.reply_template_name,
            "formset": self.get_reply_formset(request, thread),
            "url": self.get_reply_url(request, thread),
        }

    def check_reply_thread_permission(self, request: HttpRequest, thread: Thread):
        raise NotImplementedError()

    def get_reply_url(self, request: HttpRequest, thread: Thread) -> str:
        raise NotImplementedError()

    def get_reply_formset(
        self, request: HttpRequest, thread: Thread
    ) -> ReplyThreadFormset:
        raise NotImplementedError


class ThreadRepliesView(RepliesView, ThreadView):
    template_name: str = "misago/thread/index.html"
    template_partial_name: str = "misago/thread/partial.html"

    def get_thread_queryset(self, request: HttpRequest) -> Thread:
        return get_thread_replies_page_thread_queryset_hook(
            super().get_thread_queryset, request
        )

    def get_context_data(
        self, request: HttpRequest, thread: Thread, page: int | None = None
    ) -> dict:
        return get_thread_replies_page_context_data_hook(
            self.get_context_data_action, request, thread, page
        )

    def get_context_data_action(
        self, request: HttpRequest, thread: Thread, page: int | None = None
    ) -> dict:
        context = super().get_context_data_action(request, thread, page)

        context.update(
            {
                "category": thread.category,
            }
        )

        return context

    def get_thread_posts_queryset(
        self, request: HttpRequest, thread: Thread
    ) -> QuerySet:
        return get_thread_replies_page_posts_queryset_hook(
            super().get_thread_posts_queryset, request, thread
        )

    def allow_edit_thread(self, request: HttpRequest, thread: Thread) -> bool:
        if request.user.is_anonymous:
            return False

        with check_permissions() as can_edit_thread:
            check_edit_thread_permission(
                request.user_permissions, thread.category, thread
            )

        return can_edit_thread

    def is_category_read(
        self,
        request: HttpRequest,
        category: Category,
        category_read_time: datetime | None,
    ) -> bool:
        return is_category_read(request, category, category_read_time)

    def check_reply_thread_permission(self, request: HttpRequest, thread: Thread):
        check_reply_thread_permission(request.user_permissions, thread.category, thread)

    def get_reply_url(self, request: HttpRequest, thread: Thread) -> str:
        return reverse(
            "misago:reply-thread", kwargs={"id": thread.id, "slug": thread.slug}
        )

    def get_reply_formset(
        self, request: HttpRequest, thread: Thread
    ) -> ReplyThreadFormset:
        return get_reply_thread_formset(request, thread)


class PrivateThreadRepliesView(RepliesView, PrivateThreadView):
    template_name: str = "misago/private_thread/index.html"
    template_partial_name: str = "misago/private_thread/partial.html"

    def get_thread_queryset(self, request: HttpRequest) -> Thread:
        return get_private_thread_replies_page_thread_queryset_hook(
            super().get_thread_queryset, request
        )

    def get_context_data(
        self, request: HttpRequest, thread: Thread, page: int | None = None
    ) -> dict:
        return get_private_thread_replies_page_context_data_hook(
            self.get_context_data_action, request, thread, page
        )

    def get_context_data_action(
        self, request: HttpRequest, thread: Thread, page: int | None = None
    ) -> dict:
        context = super().get_context_data_action(request, thread, page)

        context.update(
            {
                "participants": None,
            }
        )

        return context

    def get_thread_posts_queryset(
        self, request: HttpRequest, thread: Thread
    ) -> QuerySet:
        return get_private_thread_replies_page_posts_queryset_hook(
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
        if read_time >= thread.last_post_on and request.user.unread_private_threads:
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
            "misago:reply-private-thread", kwargs={"id": thread.id, "slug": thread.slug}
        )

    def get_reply_formset(
        self, request: HttpRequest, thread: Thread
    ) -> ReplyPrivateThreadFormset:
        return get_reply_private_thread_formset(request, thread)


thread_replies = ThreadRepliesView.as_view()
private_thread_replies = PrivateThreadRepliesView.as_view()
