from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from django.utils import dateparse
from django.urls import reverse

from ..attachments.filetypes import filetypes
from ..permissions.edits import check_see_post_edit_history_permission
from ..permissions.privatethreads import check_see_private_thread_post_permission
from ..permissions.threads import check_see_thread_post_permission
from ..privatethreads.views.generic import PrivateThreadView
from ..threads.models import Post, Thread
from ..threads.views.generic import ThreadView
from .diff import diff_text
from .models import PostEdit


class PostEditsView:
    template_name: str
    template_name_partial = "misago/post_edits/partial.html"
    template_name_modal = "misago/post_edits/modal/htmx.html"

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

        if not request.is_htmx and thread.slug != slug:
            return redirect(self.get_post_edits_url(thread, post), permanent=True)

        queryset = (
            PostEdit.objects.filter(post=post)
            .select_related("user", "user__group")
            .order_by("id")
        )
        paginator = Paginator(queryset, per_page=1)

        if not page or page > paginator.num_pages:
            return redirect(self.get_post_edits_url(thread, post, paginator.num_pages))

        page_obj = paginator.get_page(page)

        if page_obj.object_list:
            post_edit = page_obj.object_list[0]
        else:
            post_edit = None

        if request.is_htmx:
            if request.GET.get("modal"):
                template_name = self.template_name_modal
            else:
                template_name = self.template_name_partial
        else:
            template_name = self.template_name

        return render(
            request,
            template_name,
            {
                "template_name": self.template_name_partial,
                "category": thread.category,
                "thread": thread,
                "post": post,
                "post_number": self.get_post_number(request, thread, post),
                "paginator": paginator,
                "page": page_obj,
                "post_edit": post_edit,
                "edit_diff": self.get_edit_diff(post_edit),
                "edits_url": self.get_post_edits_url(thread, post),
            },
        )

    def get_post_edits_url(
        self, thread: Thread, post: Post, page: int | None = None
    ) -> str:
        raise NotImplementedError()

    def get_edit_diff(self, post_edit: PostEdit | None):
        if not post_edit:
            return None

        diff = {
            "title": None,
            "content": None,
            "attachments": [],
        }

        if post_edit.old_title != post_edit.new_title:
            diff["title"] = diff_text(post_edit.old_title, post_edit.new_title)
        if post_edit.old_content != post_edit.new_content:
            diff["content"] = diff_text(post_edit.old_content, post_edit.new_content)

        for attachment in post_edit.attachments:
            new_attachment = attachment.copy()

            new_attachment["uploaded_at"] = dateparse.parse_datetime(
                new_attachment["uploaded_at"]
            )

            try:
                new_attachment["filetype"] = filetypes.get_filetype(
                    attachment["filetype_id"]
                )
            except ValueError:
                new_attachment["filetype"] = None

            diff["attachments"].append(new_attachment)

        return diff


class ThreadPostEditsView(ThreadView, PostEditsView):
    template_name = "misago/thread_post_edits/index.html"

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
        if page:
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
    template_name = "misago/private_thread_post_edits/index.html"

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
        if page:
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
