from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpRequest, HttpResponse
from django.db.models import QuerySet
from django.shortcuts import redirect
from django.utils.translation import pgettext
from django.views import View

from ...posts.models import Post
from ...readtracker.readtime import get_default_read_time
from ...threads.models import Thread
from ..redirect import redirect_to_post


class PostView(View):
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

    def post(self, request: HttpRequest, id: int, slug: str, **kwargs) -> HttpResponse:
        return self.get(request, id, slug, **kwargs)

    def get_post(
        self, request: HttpRequest, thread: Thread, queryset: QuerySet, kwargs: dict
    ) -> Post | None:
        try:
            if not kwargs.get("post_id"):
                raise Post.DoesNotExist()

            return queryset.get(id=kwargs["post_id"])
        except Post.DoesNotExist:
            raise Http404(pgettext("post not found error", "Post not found"))


class PostLastView(PostView):
    def get_post(self, *args) -> None:
        return None  # Redirect to last post is default


class PostUnreadView(PostView):
    thread_annotate_read_time = True

    def get_post(
        self, request: HttpRequest, thread: Thread, queryset: QuerySet, kwargs: dict
    ) -> Post | None:
        if request.user.is_anonymous:
            return None

        read_times = [get_default_read_time(request.settings, request.user)]
        if user_readthread := getattr(thread, "user_readthread", None):
            read_times.append(user_readthread.read_time)
        if thread.user_readcategory_time:
            read_times.append(thread.user_readcategory_time)

        read_time = max(read_times)
        return queryset.filter(posted_at__gt=read_time).first()


class PostSolutionView(PostView):
    thread_annotate_read_time = True

    def get_post(
        self, request: HttpRequest, thread: Thread, queryset: QuerySet, kwargs: dict
    ) -> Post | None:
        if not thread.best_answer_id:
            return None

        return queryset.filter(id=thread.best_answer_id).first()


class PostUnapprovedView(PostView):
    def raise_permission_denied_error(self):
        raise PermissionDenied(
            pgettext(
                "unapproved post redirect",
                "You must be a moderator to view unapproved posts.",
            )
        )


def post(request: HttpRequest, id: int) -> HttpResponse:
    try:
        post_obj = Post.objects.get(id=id)
        return redirect_to_post(request, post_obj)
    except (PermissionDenied, Post.DoesNotExist) as error:
        # "Post not found" or permission error would leak post's existence
        raise Http404(pgettext("post not found error", "Thread not found")) from error
