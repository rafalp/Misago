from django.core.paginator import Paginator
from django.db import transaction
from django.http import Http404, HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from django.utils import dateparse
from django.urls import reverse
from django.views import View

from ..attachments.filetypes import filetypes
from ..permissions.checkutils import check_permissions
from ..permissions.edits import (
    check_delete_post_edit_permission,
    check_see_post_edit_history_permission,
)
from ..permissions.enums import CategoryPermission
from ..permissions.privatethreads import (
    check_edit_private_thread_post_permission,
    check_see_private_thread_post_permission,
)
from ..permissions.threads import (
    check_edit_thread_post_permission,
    check_see_thread_post_permission,
)
from ..privatethreads.views.backend import private_thread_backend
from ..privatethreads.views.generic import PrivateThreadView
from ..threads.models import Post, Thread
from ..threads.views.backend import ViewBackend, thread_backend
from ..threads.views.generic import ThreadView
from .delete import delete_post_edit
from .diff import diff_text
from .models import PostEdit


class PostEditViewBackend:
    post_edit_restore_url: str
    post_edit_hide_url: str
    post_edit_unhide_url: str
    post_edit_delete_url: str

    def get_thread_post_edit(self, post: Post, post_edit_id: int) -> PostEdit:
        try:
            post_edit = PostEdit.objects.get(id=post_edit_id, post=post_edit_id)
            post_edit.category = post.category
            post_edit.thread = post.thread
            post_edit.post = post
            return post_edit
        except PostEdit.DoesNotExist:
            raise Http404()

    def get_thread_post_edit_restore_url(self, post_edit: PostEdit) -> str:
        return reverse(
            self.post_edit_restore_url,
            kwargs={
                "thread_id": post_edit.thread_id,
                "slug": post_edit.thread.slug,
                "post_id": post_edit.post_id,
                "post_edit_id": post_edit.id,
            },
        )

    def get_thread_post_edit_hide_url(self, post_edit: PostEdit) -> str:
        return reverse(
            self.post_edit_hide_url,
            kwargs={
                "thread_id": post_edit.thread_id,
                "slug": post_edit.thread.slug,
                "post_id": post_edit.post_id,
                "post_edit_id": post_edit.id,
            },
        )

    def get_thread_post_edit_unhide_url(self, post_edit: PostEdit) -> str:
        return reverse(
            self.post_edit_unhide_url,
            kwargs={
                "thread_id": post_edit.thread_id,
                "slug": post_edit.thread.slug,
                "post_id": post_edit.post_id,
                "post_edit_id": post_edit.id,
            },
        )

    def get_thread_post_edit_delete_url(self, post_edit: PostEdit) -> str:
        return reverse(
            self.post_edit_delete_url,
            kwargs={
                "thread_id": post_edit.thread_id,
                "slug": post_edit.thread.slug,
                "post_id": post_edit.post_id,
                "post_edit_id": post_edit.id,
            },
        )


class ThreadPostEditViewBackend(PostEditViewBackend):
    post_edit_restore_url = "misago:thread-post-edit-restore"
    post_edit_hide_url = "misago:thread-post-edit-hide"
    post_edit_unhide_url = "misago:thread-post-edit-unhide"
    post_edit_delete_url = "misago:thread-post-edit-delete"


class PrivateThreadPostEditViewBackend(PostEditViewBackend):
    post_edit_restore_url = "misago:private-thread-post-edit-restore"
    post_edit_hide_url = "misago:private-thread-post-edit-hide"
    post_edit_unhide_url = "misago:private-thread-post-edit-unhide"
    post_edit_delete_url = "misago:private-thread-post-edit-delete"


thread_post_edit_backend = ThreadPostEditViewBackend()
private_thread_post_edit_backend = PrivateThreadPostEditViewBackend()


class PostEditsView(View):
    thread_backend: ViewBackend
    post_edit_backend: PostEditViewBackend

    template_name: str
    template_name_partial = "misago/post_edits/partial.html"
    template_name_modal = "misago/post_edits/modal/htmx.html"
    template_name_edit_diff = "misago/post_edits/edit_diff.html"

    def get(
        self,
        request: HttpRequest,
        thread_id: int,
        slug: str,
        post_id: int,
        page: int | None = None,
    ) -> HttpResponse:
        thread = self.thread_backend.get_thread(request, thread_id)
        post = self.thread_backend.get_thread_post(
            request, thread, post_id, for_content=True
        )

        check_see_post_edit_history_permission(
            request.user_permissions, thread.category, thread, post
        )

        if not request.is_htmx and thread.slug != slug:
            return redirect(
                self.thread_backend.get_thread_post_edits_url(thread, post),
                permanent=True,
            )

        queryset = (
            PostEdit.objects.filter(post=post)
            .select_related("user", "user__group")
            .order_by("id")
        )
        paginator = Paginator(queryset, per_page=1)

        if not page or page > paginator.num_pages:
            return redirect(
                self.thread_backend.get_thread_post_edits_url(
                    thread, post, paginator.num_pages
                )
            )

        page_obj = paginator.get_page(page)

        if page_obj.object_list:
            post_edit = page_obj.object_list[0]
            post_edit.category = thread.category
            post_edit.thread = thread
            post_edit.post = post
        else:
            post_edit = None

        if request.is_htmx:
            if request.GET.get("modal"):
                template_name = self.template_name_modal
            else:
                template_name = self.template_name_partial
        else:
            template_name = self.template_name

        with check_permissions() as can_restore:
            self.check_thread_post_edit_permission(request, thread, post)

        with check_permissions() as can_delete:
            check_delete_post_edit_permission(
                request.user_permissions, thread.category, thread, post, post_edit
            )

        return render(
            request,
            template_name,
            {
                "template_name": self.template_name_partial,
                "category": thread.category,
                "thread": thread,
                "post": post,
                "post_number": self.thread_backend.get_thread_post_number(
                    request, thread, post
                ),
                "paginator": paginator,
                "page": page_obj,
                "post_edit": post_edit,
                "edit_diff": self.get_edit_diff_data(request, thread, post, post_edit),
                "post_edits_url": self.thread_backend.get_thread_post_edits_url(
                    thread, post
                ),
                "show_options": can_restore or can_delete,
                "can_restore": can_restore,
                "can_delete": can_delete,
                "post_edit_restore_url": self.post_edit_backend.get_thread_post_edit_restore_url(
                    post_edit
                ),
                "post_edit_delete_url": self.post_edit_backend.get_thread_post_edit_delete_url(
                    post_edit
                ),
            },
        )

    def check_thread_post_edit_permission(
        self, request: HttpRequest, thread: Thread, post: Post
    ):
        raise NotImplementedError()

    def get_edit_diff_data(
        self,
        request: HttpRequest,
        thread: Thread,
        post: Post,
        post_edit: PostEdit | None,
    ) -> dict:
        if not post_edit:
            return None

        diff = {
            "template_name": self.template_name_edit_diff,
            "edit_reason": post_edit.edit_reason,
            "blank": True,
            "title": None,
            "content": None,
            "attachments": self.get_edit_diff_attachments(
                request, thread, post, post_edit
            ),
        }

        if post_edit.old_title != post_edit.new_title:
            diff["title"] = diff_text(post_edit.old_title, post_edit.new_title)

        if post_edit.old_content != post_edit.new_content:
            diff["content"] = diff_text(post_edit.old_content, post_edit.new_content)

        diff["blank"] = not bool(
            diff["title"] or diff["content"] or diff["attachments"]
        )

        return diff

    def get_edit_diff_attachments(
        self, request: HttpRequest, thread: Thread, post: Post, post_edit: PostEdit
    ) -> list:
        data = []

        for attachment in post_edit.attachments:
            new_attachment = attachment.copy()
            if not self.get_attachment_permission(
                request, thread, post, new_attachment
            ):
                continue

            new_attachment["uploaded_at"] = dateparse.parse_datetime(
                new_attachment["uploaded_at"]
            )

            try:
                new_attachment["filetype"] = filetypes.get_filetype(
                    attachment["filetype_id"]
                )
            except ValueError:
                new_attachment["filetype"] = None

            if new_attachment["dimensions"]:
                new_attachment["width"] = new_attachment["dimensions"][0]
                new_attachment["height"] = new_attachment["dimensions"][1]
            else:
                new_attachment["width"] = None
                new_attachment["height"] = None

            if request.user.is_authenticated and (
                request.user.is_misago_admin
                or request.user.id == new_attachment["uploader"]
            ):
                new_attachment["url"] = reverse(
                    "misago:attachment-details",
                    kwargs={
                        "id": new_attachment["id"],
                        "slug": new_attachment["slug"],
                    },
                )
            else:
                new_attachment["url"] = None

            data.append(new_attachment)

        return data

    def get_attachment_permission(
        self, request: HttpRequest, thread: Thread, post: Post, attachment: dict
    ) -> bool:
        raise NotImplementedError()


class ThreadPostEditsView(PostEditsView):
    thread_backend = thread_backend
    post_edit_backend = thread_post_edit_backend

    template_name = "misago/thread_post_edits/index.html"

    post_edit_restore_url = "misago:thread-post-edit-restore"
    post_edit_delete_url = "misago:thread-post-edit-delete"

    def check_thread_post_edit_permission(
        self, request: HttpRequest, thread: Thread, post: Post
    ):
        check_edit_thread_post_permission(
            request.user_permissions, thread.category, thread, post
        )

    def get_attachment_permission(
        self, request: HttpRequest, thread: Thread, post: Post, attachment: dict
    ) -> bool:
        if (
            request.user.is_authenticated
            and request.user.id == attachment["uploader_id"]
        ):
            return True

        return (
            thread.category_id
            in request.user_permissions.categories[CategoryPermission.ATTACHMENTS]
        )


class PrivateThreadPostEditsView(PostEditsView):
    thread_backend = private_thread_backend
    post_edit_backend = private_thread_post_edit_backend

    template_name = "misago/private_thread_post_edits/index.html"

    post_edit_restore_url = "misago:private-thread-post-edit-restore"
    post_edit_delete_url = "misago:private-thread-post-edit-delete"

    def check_thread_post_edit_permission(
        self, request: HttpRequest, thread: Thread, post: Post
    ):
        check_edit_private_thread_post_permission(
            request.user_permissions, thread, post
        )

    def get_attachment_permission(
        self, request: HttpRequest, thread: Thread, post: Post, attachment: dict
    ) -> bool:
        return True


class PostEditView:
    thread_backend: ViewBackend
    post_edit_backend: PostEditViewBackend

    template_name: str
    template_name_htmx = "misago/post_edit/htmx.html"
    template_name_modal = "misago/post_edit/modal/.html"

    def get(
        self,
        request: HttpRequest,
        thread_id: int,
        slug: str,
        post_id: int,
        post_edit_id: int,
    ) -> HttpResponse:
        thread = self.get_thread(request, thread_id)
        post = self.get_thread_post(request, thread, post_id)
        self.check_thread_post_permissions(request, thread, post)

        post_edit = self.get_thread_post_edit(request, post, post_edit_id)
        self.check_thread_post_edit_permission(request, thread, post, post_edit)

        return render(
            request,
            self.template_name,
            {
                "category": thread.category,
                "thread": thread,
                "post": post,
                "post_edit": post_edit,
            },
        )

    def post(
        self,
        request: HttpRequest,
        thread_id: int,
        slug: str,
        post_id: int,
        post_edit_id: int,
    ) -> HttpResponse:
        thread = self.get_thread(request, thread_id)
        post = self.get_thread_post(request, thread, post_id)
        self.check_thread_post_permissions(request, thread, post)

        post_edit = self.get_thread_post_edit(request, post, post_edit_id)
        self.check_thread_post_edit_permission(request, thread, post, post_edit)

    def get_thread_post_edit(
        self,
        request: HttpRequest,
        post: Post,
        post_edit_id: int,
    ) -> PostEdit:
        try:
            post_edit = PostEdit.objects.select_related("user", "user__group").get(
                id=post_edit_id, post=post
            )
            post_edit.category = post.category
            post_edit.thread = post.thread
            post_edit.post = post
            return post_edit
        except PostEdit.DoesNotExist:
            raise Http404()

    def check_thread_post_permission(
        self,
        request: HttpRequest,
        thread: Thread,
        post: Post,
        post_edit: PostEdit,
    ):
        raise NotImplementedError()

    def check_thread_post_edit_permission(
        self,
        request: HttpRequest,
        thread: Thread,
        post: Post,
        post_edit: PostEdit,
    ):
        raise NotImplementedError()


class PostEditHideView(PostEditView):
    def post(
        self,
        request: HttpRequest,
        thread_id: int,
        slug: str,
        post_id: int,
        post_edit_id: int,
    ) -> HttpResponse:
        thread = self.get_thread(request, thread_id)
        post = self.get_thread_post(request, thread, post_id)
        post_edit = self.get_thread_post_edit(request, post, post_edit_id)
        check_see_post_edit_history_permission(
            request.user_permissions, thread.category, thread, post
        )

        raise NotImplementedError()


class PostEditUnhideView(PostEditView):
    def post(
        self,
        request: HttpRequest,
        thread_id: int,
        slug: str,
        post_id: int,
        post_edit_id: int,
    ) -> HttpResponse:
        thread = self.get_thread(request, thread_id)
        post = self.get_thread_post(request, thread, post_id)
        post_edit = self.get_thread_post_edit(request, post, post_edit_id)

        raise NotImplementedError()


class PostEditDeleteView(PostEditView):
    template_name = "misago/post_edit_delete/index.html"

    def post(
        self,
        request: HttpRequest,
        thread_id: int,
        slug: str,
        post_id: int,
        post_edit_id: int,
    ) -> HttpResponse:
        thread = self.get_thread(request, thread_id)
        post = self.get_thread_post(request, thread, post_id)
        check_see_post_edit_history_permission(
            request.user_permissions, thread.category, thread, post
        )

        post_edit = self.get_thread_post_edit(request, post, post_edit_id)

        if not self.check_permission(request, post_edit):
            pass

        delete_post_edit(post_edit, request=request)

        # Return redirect to somewhere


class ThreadPostEditDeleteView(PostEditDeleteView, ThreadView):
    pass


class PrivateThreadPostEditDeleteView(PostEditDeleteView, PrivateThreadView):
    pass


class PostEditRestoreView(PostEditView):
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


class ThreadPostEditRestoreView(PostEditRestoreView, ThreadView):
    def get_thread_post(
        self, request: HttpRequest, thread: Thread, post_id: int
    ) -> Post:
        post = super().get_thread_post(request, thread, post_id)
        check_see_thread_post_permission(
            request.user_permissions, post.category, post.thread, post
        )
        return post


class PrivateThreadPostEditRestoreView(PostEditRestoreView, PrivateThreadView):
    def get_thread_post(
        self, request: HttpRequest, thread: Thread, post_id: int
    ) -> Post:
        post = super().get_thread_post(request, thread, post_id)
        check_see_private_thread_post_permission(
            request.user_permissions, post.thread, post
        )
        return post
