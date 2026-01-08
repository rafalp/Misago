from datetime import datetime
from typing import TYPE_CHECKING, Any

from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseNotAllowed,
)
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from ...categories.models import Category
from ...notifications.threads import update_watched_thread_read_time
from ...permissions.checkutils import check_permissions
from ...permissions.polls import check_start_thread_poll_permission
from ...permissions.threads import (
    check_edit_thread_permission,
    check_reply_thread_permission,
)
from ...polls.enums import PollTemplate
from ...polls.models import Poll
from ...polls.views import dispatch_thread_poll_view, get_poll_context_data
from ...polls.votes import get_user_poll_votes
from ...posting.formsets import (
    ThreadReplyFormset,
    get_thread_reply_formset,
)
from ...readtracker.tracker import (
    get_unread_posts,
    mark_category_read,
    mark_thread_read,
)
from ...readtracker.threads import is_category_read
from ...threadupdates.models import ThreadUpdate
from ..hooks import (
    get_thread_replies_page_context_data_hook,
    get_thread_replies_page_posts_queryset_hook,
    get_thread_replies_page_thread_queryset_hook,
)
from ..models import Post, Thread
from ..paginator import ThreadPostsPaginator
from .backend import ViewBackend, thread_backend
from .generic import ThreadView

if TYPE_CHECKING:
    from ...users.models import User


class PageOutOfRangeError(Exception):
    redirect_to: str

    def __init__(self, redirect_to: str):
        self.redirect_to = redirect_to


class DetailView(View):
    backend: ViewBackend

    thread_annotate_read_time: bool = True
    template_name: str
    template_partial_name: str
    feed_template_name: str = "misago/post_feed/index.html"
    feed_post_template_name: str = "misago/post_feed/post.html"
    reply_error_template_name: str = "misago/thread/reply_error.html"
    reply_template_name: str = "misago/quick_reply/form.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            return super().dispatch(request, *args, **kwargs)
        except PageOutOfRangeError as exc:
            return redirect(exc.redirect_to)

    def get(
        self, request: HttpRequest, thread_id: int, slug: str, page: int | None = None
    ) -> HttpResponse:
        thread = self.get_thread(request, thread_id)

        if not request.is_htmx and (thread.slug != slug or page == 1):
            return redirect(self.get_thread_url(thread), permanent=thread.slug != slug)

        context = self.get_context_data(request, thread, page)

        if request.is_htmx:
            template_name = self.template_partial_name
        else:
            template_name = self.template_name

        return render(request, template_name, context)

    def post(
        self, request: HttpRequest, thread_id: int, slug: str, page: int | None = None
    ) -> HttpResponse:
        return HttpResponseNotAllowed(["GET", "POST"])

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
            "feed": self.get_post_feed_data(request, thread, page),
            "reply": self.get_reply_context_data(request, thread),
            "post_edits_modal_template": self.backend.post_edits_modal_template,
            "post_likes_modal_template": self.backend.post_likes_modal_template,
        }

    def get_post_feed_data(
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
        thread_updates = self.get_thread_updates(request, thread, page_obj, posts)

        feed = self.get_post_feed(request, thread, posts, thread_updates)
        feed.set_counter_start(page_obj.start_index() - 1)

        unread = get_unread_posts(request, thread, posts)
        feed.set_unread_posts(unread)

        allow_edit_thread = self.allow_edit_thread(request, thread)
        feed.set_allow_edit_thread(allow_edit_thread)

        if unread:
            self.update_thread_read_time(request, thread, posts[-1].posted_at)

        if request.user.is_authenticated and request.user.unread_notifications:
            self.read_user_notifications(request.user, posts)

        return feed.get_context_data({"paginator": page_obj})

    def get_thread_updates(
        self,
        request: HttpRequest,
        thread: Thread,
        page: ThreadPostsPaginator,
        posts: list[Post],
    ) -> list[ThreadUpdate]:
        queryset = self.get_thread_updates_queryset(request, thread)
        if page.number > 1:
            queryset = queryset.filter(created_at__gt=posts[0].posted_at)
        if page.next_page_first_item:
            queryset = queryset.filter(
                created_at__lt=page.next_page_first_item.posted_at
            )
        return list(reversed(queryset[: request.settings.thread_updates_per_page]))

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

        if self.is_category_read(
            request, thread.category, thread.user_readcategory_time
        ):
            self.mark_category_read(
                request.user,
                thread.category,
                force_update=bool(thread.user_readcategory_time),
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
    ) -> ThreadReplyFormset:
        raise NotImplementedError


class ThreadDetailView(DetailView, ThreadView):
    backend = thread_backend

    template_name: str = "misago/thread/index.html"
    template_partial_name: str = "misago/thread/partial.html"

    def get(
        self, request: HttpRequest, thread_id: int, slug: str, page: int | None = None
    ) -> HttpResponse:
        if request.is_htmx:
            if poll_response := dispatch_thread_poll_view(request, thread_id):
                return poll_response

        return super().get(request, thread_id, slug, page)

    def post(
        self, request: HttpRequest, thread_id: int, slug: str, page: int | None = None
    ) -> HttpResponse:
        if request.GET.get("poll"):
            if poll_response := dispatch_thread_poll_view(request, thread_id):
                return poll_response

        return super().post(request, thread_id, slug, page)

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

        context["category"] = thread.category

        poll = self.get_poll(request, thread)
        if poll:
            context["poll"] = self.get_poll_context_data(request, thread, poll)
            context["allow_start_poll"] = False
        else:
            with check_permissions() as allow_start_poll:
                check_start_thread_poll_permission(
                    request.user_permissions, thread.category, thread
                )

            context["allow_start_poll"] = allow_start_poll

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
            "misago:thread-reply", kwargs={"thread_id": thread.id, "slug": thread.slug}
        )

    def get_reply_formset(
        self, request: HttpRequest, thread: Thread
    ) -> ThreadReplyFormset:
        return get_thread_reply_formset(request, thread)

    def get_poll(self, request: HttpRequest, thread: Thread) -> Poll | None:
        if thread.has_poll:
            return Poll.objects.filter(thread=thread).first()

        return None

    def get_poll_context_data(
        self,
        request: HttpRequest,
        thread: Thread,
        poll: Poll,
    ) -> dict:
        user_poll_votes = get_user_poll_votes(request.user, poll)
        context = get_poll_context_data(
            request,
            thread,
            poll,
            user_poll_votes,
            fetch_voters=request.GET.get("poll") == "voters",
        )

        template_name = PollTemplate.RESULTS
        if (
            context["allow_vote"]
            and request.GET.get("poll") not in ("results", "voters")
            and (request.GET.get("poll") == "vote" or not user_poll_votes)
        ):
            template_name = PollTemplate.VOTE

        context["template_name"] = template_name
        return context
