from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse

from ..permissions.edits import check_see_post_edit_history_permission
from ..permissions.privatethreads import check_see_private_thread_post_permission
from ..permissions.threads import check_see_thread_post_permission
from ..privatethreads.views.generic import PrivateThreadView
from ..threads.models import Post, Thread
from ..threads.views.generic import ThreadView
from .models import PostEdit


class PostEditsView:
    def get(
        self,
        request: HttpRequest,
        thread_id: int,
        slug: str,
        post_id: int,
        page: int | None = None,
    ) -> HttpResponse:
        thread = self.get_thread(request, thread_id)
        post = self.get_thread_post(request, thread, post_id)

        check_see_post_edit_history_permission(
            request.user_permissions, thread.category, thread, post
        )

        if not request.is_htmx and (thread.slug != slug or page == 1):
            return redirect(
                self.get_post_edits_url(thread, post), permanent=thread.slug != slug
            )

        queryset = PostEdit.objects.filter(post=post).order_by("-id")
        paginator = Paginator(queryset, per_page=1)

        if page and page > paginator.num_pages:
            return redirect(self.get_post_edits_url(thread, post, paginator.num_pages))

        page_obj = paginator.get_page(page)
        post_edit = page_obj.object_list[0]

        raise NotImplementedError(post_edit)

    def get_post_edits_url(
        self, thread: Thread, post: Post, page: int | None = None
    ) -> str:
        raise NotImplementedError()


class ThreadPostEditsView(ThreadView, PostEditsView):
    def get_thread_post(
        self, request: HttpRequest, thread: Thread, post_id: int
    ) -> Post:
        post = super().get_thread_post(request, thread, post_id)
        check_see_thread_post_permission(
            request.user_permissions, post.category, post.thread, post
        )
        return post

    def get_post_edits_url(
        self, thread: Thread, post: Post, page: int | None = None
    ) -> str:
        if page and page > 1:
            return reverse(
                "misago:thread-post-edits",
                kwargs={
                    "thread_id": thread.id,
                    "slug": thread.slug,
                    "post_id": post.id,
                    "page": page,
                },
            )

        return reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        )


class PrivateThreadPostEditsView(PrivateThreadView, PostEditsView):
    def get_thread_post(
        self, request: HttpRequest, thread: Thread, post_id: int
    ) -> Post:
        post = super().get_thread_post(request, thread, post_id)
        check_see_private_thread_post_permission(
            request.user_permissions, post.thread, post
        )
        return post

    def get_post_edits_url(
        self, thread: Thread, post: Post, page: int | None = None
    ) -> str:
        if page and page > 1:
            return reverse(
                "misago:private-thread-post-edits",
                kwargs={
                    "thread_id": thread.id,
                    "slug": thread.slug,
                    "post_id": post.id,
                    "page": page,
                },
            )

        return reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        )


class PostRestoreView:
    def post(
        self,
        request: HttpRequest,
        thread_id: int,
        slug: str,
        post_id: int,
        post_edit_id: int,
    ) -> HttpResponse:
        thread = self.get_thread(request, thread_id)

        with transaction.atomic():
            post = self.get_thread_post(request, thread, post_id, for_update=True)

        raise NotImplementedError()


class ThreadPostRestoreView(PostRestoreView, PrivateThreadView):
    def get_thread_post(
        self, request: HttpRequest, thread: Thread, post_id: int
    ) -> Post:
        post = super().get_thread_post(request, thread, post_id)
        check_see_thread_post_permission(
            request.user_permissions, post.category, post.thread, post
        )
        return post


class PrivateThreadPostRestoreView(PostRestoreView, ThreadView):
    def get_thread_post(
        self, request: HttpRequest, thread: Thread, post_id: int
    ) -> Post:
        post = super().get_thread_post(request, thread, post_id)
        check_see_private_thread_post_permission(
            request.user_permissions, post.thread, post
        )
        return post
