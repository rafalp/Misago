from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpRequest, HttpResponse
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import pgettext
from django.views import View

from ...categories.enums import CategoryTree
from ...readtracker.readtime import get_default_read_time
from ..hooks import get_redirect_to_post_response_hook
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

    def post(self, request: HttpRequest, id: int, slug: str, **kwargs) -> HttpResponse:
        return self.get(request, id, slug, **kwargs)

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


class SolutionRedirectView(RedirectView):
    thread_annotate_read_time = True

    def get_post(
        self, request: HttpRequest, thread: Thread, queryset: QuerySet, kwargs: dict
    ) -> Post | None:
        if not thread.best_answer_id:
            return None

        return queryset.filter(id=thread.best_answer_id).first()


class ThreadSolutionRedirectView(SolutionRedirectView, ThreadView):
    pass


class UnapprovedPostRedirectView(RedirectView):
    def raise_permission_denied_error(self):
        raise PermissionDenied(
            pgettext(
                "unaproved post redirect",
                "You must be a moderator to view unapproved posts.",
            )
        )


class ThreadUnapprovedPostRedirectView(UnapprovedPostRedirectView, ThreadView):
    def get_post(
        self, request: HttpRequest, thread: Thread, queryset: QuerySet, kwargs: dict
    ) -> Post | None:
        if not request.user_permissions.is_category_moderator(thread.category_id):
            self.raise_permission_denied_error()

        return queryset.filter(is_unapproved=True).first()


class PrivateThreadUnapprovedPostRedirectView(
    UnapprovedPostRedirectView, PrivateThreadView
):
    def get_post(
        self, request: HttpRequest, thread: Thread, queryset: QuerySet, kwargs: dict
    ) -> Post | None:
        if not request.user_permissions.is_private_threads_moderator:
            self.raise_permission_denied_error()

        return queryset.filter(is_unapproved=True).first()


class PostRedirectView(View):
    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        return self.real_dispatch(request, id)

    def post(self, request: HttpRequest, id: int) -> HttpResponse:
        return self.real_dispatch(request, id)

    def real_dispatch(self, request: HttpRequest, id: int) -> HttpResponse:
        queryset = Post.objects.select_related("category")
        post = get_object_or_404(queryset, id=id)
        return get_redirect_to_post_response(request, post)


def get_redirect_to_post_response(request: HttpRequest, post: Post) -> HttpResponse:
    try:
        return get_redirect_to_post_response_hook(
            _get_redirect_to_post_response_action, request, post
        )
    except PermissionDenied:
        raise Http404()


def _get_redirect_to_post_response_action(
    request: HttpRequest, post: Post
) -> HttpResponse:
    if post.category.tree_id == CategoryTree.THREADS:
        return thread_post_redirect(request, post.thread_id, "", post=post.id)

    if post.category.tree_id == CategoryTree.PRIVATE_THREADS:
        return private_thread_post_redirect(request, post.thread_id, "", post=post.id)

    raise Http404()


class GetPostRedirectView(RedirectView):
    def get_post(
        self, request: HttpRequest, thread: Thread, queryset: QuerySet, kwargs: dict
    ) -> Post | None:
        return get_object_or_404(queryset, id=kwargs["post"])


class ThreadPostRedirectView(GetPostRedirectView, ThreadView):
    pass


class PrivateThreadPostRedirectView(GetPostRedirectView, PrivateThreadView):
    pass


thread_post_redirect = ThreadPostRedirectView.as_view()
private_thread_post_redirect = PrivateThreadPostRedirectView.as_view()
