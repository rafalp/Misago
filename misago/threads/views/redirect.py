from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet
from django.shortcuts import redirect
from django.views import View

from ...readtracker.readtime import get_default_read_time
from ..models import Post, Thread
from .generic import PrivateThreadView, ThreadView


class RedirectView(View):
    def get(self, request: HttpRequest, id: int, slug: str, **kwargs) -> HttpResponse:
        thread = self.get_thread(request, id)
        queryset = self.get_thread_posts_queryset(request, thread)
        post = self.get_post(request, thread, queryset, kwargs)
        paginator = self.get_thread_posts_paginator(request, queryset)

        if post:
            post_id = post.id
            offset = queryset.filter(id__lt=post_id).count()
            page = paginator.get_item_page(offset)
        else:
            post_id = queryset.last().id
            page = paginator.num_pages

        thread_url = self.get_thread_url(thread, page) + f"#post-{post_id}"
        return redirect(thread_url)

    def get_post(
        self, request: HttpRequest, thread: Thread, queryset: QuerySet, kwargs: dict
    ) -> Post | None:
        raise NotImplementedError()


class LastPostRedirectView(RedirectView):
    def get_post(self, *args) -> None:
        return None  # Redirect to last post is default


class ThreadLastPostRedirectView(LastPostRedirectView, ThreadView):
    pass


class PrivateThreadLastPostRedirectView(LastPostRedirectView, PrivateThreadView):
    pass


class UnreadPostRedirectView(RedirectView):
    thread_annotate_read_time = True

    def get_post(
        self, request: HttpRequest, thread: Thread, queryset: QuerySet, kwargs: dict
    ) -> Post | None:
        if request.user.is_anonymous:
            return None

        read_times = [get_default_read_time(request.settings, request.user)]
        if thread.read_time:
            read_times.append(thread.read_time)
        if thread.category_read_time:
            read_times.append(thread.category_read_time)

        read_time = max(read_times)
        return queryset.filter(posted_on__gt=read_time).first()


class ThreadUnreadPostRedirectView(UnreadPostRedirectView, ThreadView):
    pass


class PrivateThreadUnreadPostRedirectView(UnreadPostRedirectView, PrivateThreadView):
    pass


class ThreadUnapprovedPostRedirectView(RedirectView, ThreadView):
    def get_post(
        self, request: HttpRequest, thread: Thread, queryset: QuerySet, kwargs: dict
    ) -> Post | None:
        if request.user.is_anonymous:
            return None

        if not (
            request.user_permissions.is_global_moderator
            or thread.category in request.categories_moderator
        ):
            return None

        return queryset.filter(is_unapproved=True).first()


class PrivateThreadUnapprovedPostRedirectView(RedirectView, PrivateThreadView):
    def get_post(
        self, request: HttpRequest, thread: Thread, queryset: QuerySet, kwargs: dict
    ) -> Post | None:
        if not request.user_permissions.private_threads_moderator:
            return None

        return queryset.filter(is_unapproved=True).first()
