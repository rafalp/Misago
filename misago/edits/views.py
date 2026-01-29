from django.contrib import messages
from django.core.paginator import Page, Paginator
from django.http import HttpResponse, HttpResponseNotAllowed, HttpRequest
from django.shortcuts import redirect, render
from django.utils import dateparse
from django.utils.translation import pgettext
from django.urls import reverse

from ..attachments.filetypes import filetypes
from ..permissions.checkutils import check_permissions
from ..permissions.edits import (
    check_delete_post_edit_permission,
    check_hide_post_edit_permission,
    check_see_post_edit_history_permission,
    check_unhide_post_edit_permission,
)
from ..privatethreads.views.backend import private_thread_backend
from ..threads.models import Post
from ..threads.views.backend import thread_backend
from ..threads.views.generic import GenericThreadView
from .delete import delete_post_edit
from .diff import diff_text
from .hide import hide_post_edit, unhide_post_edit
from .restore import restore_post_edit
from .models import PostEdit
from .viewbackends import (
    PostEditViewBackend,
    private_thread_post_edit_backend,
    thread_post_edit_backend,
)


class GenericPostEditView(GenericThreadView):
    post_edit_backend: PostEditViewBackend

    @property
    def partial_template_name(self) -> str:
        return self.post_edit_backend.partial_template_name

    @property
    def modal_template_name(self) -> str:
        return self.post_edit_backend.modal_template_name

    @property
    def edit_diff_template_name(self) -> str:
        return self.post_edit_backend.edit_diff_template_name

    def get_thread_post_edit(
        self, request: HttpRequest, post: Post, post_edit_id: int
    ) -> PostEdit:
        return self.post_edit_backend.get_thread_post_edit(request, post, post_edit_id)

    def get_thread_post_edit_index(self, post_edit: PostEdit) -> int | None:
        return self.post_edit_backend.get_thread_post_edit_index(post_edit)

    def check_restore_post_edit_permission(
        self, request: HttpRequest, post_edit: PostEdit
    ):
        self.post_edit_backend.check_restore_post_edit_permission(request, post_edit)

    def get_attachment_permission(
        self, request: HttpRequest, post: Post, attachment: dict
    ) -> bool:
        return self.post_edit_backend.get_attachment_permission(
            request, post, attachment
        )

    def get_thread_post_edit_restore_url(self, post_edit: PostEdit) -> str:
        return self.post_edit_backend.get_thread_post_edit_restore_url(post_edit)

    def get_thread_post_edit_hide_url(self, post_edit: PostEdit) -> str:
        return self.post_edit_backend.get_thread_post_edit_hide_url(post_edit)

    def get_thread_post_edit_unhide_url(self, post_edit: PostEdit) -> str:
        return self.post_edit_backend.get_thread_post_edit_unhide_url(post_edit)

    def get_thread_post_edit_delete_url(self, post_edit: PostEdit) -> str:
        return self.post_edit_backend.get_thread_post_edit_delete_url(post_edit)

    def get_thread_post_edit_context_data(
        self, request: HttpRequest, post: Post, page: Page
    ) -> dict:
        return self.post_edit_backend.get_context_data_hook(
            self._get_thread_post_edit_context_data_action, request, post, page
        )

    def _get_thread_post_edit_context_data_action(
        self, request: HttpRequest, post: Post, page: Page
    ) -> dict:
        if page.object_list:
            post_edit = page.object_list[0]
            post_edit.category = post.category
            post_edit.thread = post.thread
            post_edit.post = post
        else:
            post_edit = None

        context = {
            "category": post.category,
            "thread": post.thread,
            "post": post,
            "post_number": self.get_thread_post_number(request, post),
            "post_url": self.get_thread_post_url(post),
            "post_edits_url": self.get_thread_post_edits_url(post),
            "paginator": page.paginator,
            "page": page,
            "post_edit": post_edit,
            "edit_number": None,
            "edit_diff": None,
            "show_options": False,
            "post_edit_diff_plugins_top": [],
            "post_edit_diff_plugins_bottom": [],
        }

        if not post_edit:
            return context

        is_moderator = self.get_thread_moderator_permission(
            request.user_permissions, post_edit.thread
        )

        with check_permissions() as can_restore:
            self.check_restore_post_edit_permission(request, post_edit)

        can_hide = False
        can_unhide = False

        if post_edit.is_hidden:
            with check_permissions():
                check_unhide_post_edit_permission(request.user_permissions, post_edit)
                can_unhide = True
        else:
            with check_permissions():
                check_hide_post_edit_permission(request.user_permissions, post_edit)
                can_hide = True

        with check_permissions() as can_delete:
            check_delete_post_edit_permission(request.user_permissions, post_edit)

        context.update(
            {
                "is_moderator": is_moderator,
                "edit_number": page.number,
                "edit_diff": self._get_edit_diff_data(request, post_edit),
                "show_options": any((can_restore, can_hide, can_unhide, can_delete)),
                "can_restore": can_restore,
                "can_hide": can_hide,
                "can_unhide": can_unhide,
                "can_delete": can_delete,
                "post_edit_restore_url": self.get_thread_post_edit_restore_url(
                    post_edit
                ),
                "post_edit_hide_url": self.get_thread_post_edit_hide_url(post_edit),
                "post_edit_unhide_url": self.get_thread_post_edit_unhide_url(post_edit),
                "post_edit_delete_url": self.get_thread_post_edit_delete_url(post_edit),
            }
        )

        return context

    def _get_edit_diff_data(
        self,
        request: HttpRequest,
        post_edit: PostEdit | None,
    ) -> dict:
        if not post_edit:
            return None

        is_moderator = self.get_thread_moderator_permission(
            request.user_permissions, post_edit.thread
        )

        diff = {
            "template_name": self.edit_diff_template_name,
            "edit_reason": post_edit.edit_reason,
            "is_visible": not post_edit.is_hidden or is_moderator,
            "blank": True,
            "title": None,
            "content": None,
            "attachments": self._get_edit_diff_attachments(request, post_edit),
        }

        if post_edit.old_title != post_edit.new_title:
            diff["title"] = diff_text(post_edit.old_title, post_edit.new_title)

        if post_edit.old_content != post_edit.new_content:
            diff["content"] = diff_text(post_edit.old_content, post_edit.new_content)

        diff["blank"] = not bool(
            diff["title"] or diff["content"] or diff["attachments"]
        )

        return diff

    def _get_edit_diff_attachments(
        self, request: HttpRequest, post_edit: PostEdit
    ) -> list:
        data = []

        for attachment in post_edit.attachments:
            new_attachment = attachment.copy()
            if not self.get_attachment_permission(
                request, post_edit.post, new_attachment
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
                or request.user.id == new_attachment["uploader_id"]
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


class PostEditsView(GenericPostEditView):
    post_edit_backend: PostEditViewBackend

    template_name: str

    def get(
        self,
        request: HttpRequest,
        thread_id: int,
        slug: str,
        post_id: int,
        page: int | None = None,
    ) -> HttpResponse:
        thread = self.get_thread(request, thread_id)
        post = self.get_thread_post(request, thread, post_id, for_content=True)

        check_see_post_edit_history_permission(
            request.user_permissions, thread.category, thread, post
        )

        if not request.is_htmx and thread.slug != slug:
            return redirect(
                self.get_thread_post_edits_url(post, page),
                permanent=True,
            )

        queryset = (
            PostEdit.objects.filter(post=post)
            .select_related("user", "user__group")
            .order_by("id")
        )
        paginator = Paginator(queryset, per_page=1)

        if paginator.count and (not page or page > paginator.num_pages):
            redirect_url = self.get_thread_post_edits_url(post, paginator.num_pages)
            if request.GET.get("modal"):
                redirect_url += "?modal=true"
            return redirect(redirect_url)

        page_obj = paginator.get_page(page or 1)

        context_data = self.get_thread_post_edit_context_data(request, post, page_obj)

        if request.is_htmx:
            if request.GET.get("modal"):
                template_name = self.modal_template_name
            else:
                template_name = self.partial_template_name
        else:
            template_name = self.template_name
            context_data["partial_template_name"] = self.partial_template_name

        return render(request, template_name, context_data)


class ThreadPostEditsView(PostEditsView):
    backend = thread_backend
    post_edit_backend = thread_post_edit_backend

    template_name = "misago/thread_post_edits/index.html"


class PrivateThreadPostEditsView(PostEditsView):
    backend = private_thread_backend
    post_edit_backend = private_thread_post_edit_backend

    template_name = "misago/private_thread_post_edits/index.html"


class PostEditView(GenericPostEditView):
    post_edit_backend: PostEditViewBackend

    template_name: str | None = None

    def dispatch(
        self,
        request: HttpRequest,
        thread_id: int,
        slug: str,
        post_id: int,
        post_edit_id: int,
    ) -> HttpResponse:
        if request.method not in ("GET", "POST", "HEAD"):
            return HttpResponseNotAllowed(["GET", "POST", "HEAD"])
        if not self.template_name and request.method != "POST":
            return HttpResponseNotAllowed(["POST"])

        thread = self.get_thread(request, thread_id)
        post = self.get_thread_post(request, thread, post_id, for_content=True)

        check_see_post_edit_history_permission(
            request.user_permissions, thread.category, thread, post
        )

        post_edit = self.get_thread_post_edit(request, post, post_edit_id)
        self.check_post_edit_permission(request, post_edit)

        if request.method == "POST":
            return self.execute_action(request, post_edit)

        edit_index = self.get_thread_post_edit_index(post_edit)

        return render(
            request,
            self.template_name,
            {
                "category": thread.category,
                "thread": thread,
                "post": post,
                "post_number": self.get_thread_post_number(request, post),
                "post_edit": post_edit,
                "post_url": self.get_thread_post_url(post),
                "post_edit_number": edit_index,
                "post_edit_url": self.get_thread_post_edits_url(post, edit_index),
            },
        )

    def check_post_edit_permission(self, request: HttpRequest, post_edit: PostEdit):
        raise NotImplementedError()

    def execute_action(self, request: HttpRequest, post_edit: PostEdit) -> HttpResponse:
        raise NotImplementedError

    def get_action_response(
        self, request: HttpRequest, post: Post, page: int | None
    ) -> HttpResponse:
        queryset = (
            PostEdit.objects.filter(post=post)
            .select_related("user", "user__group")
            .order_by("id")
        )
        paginator = Paginator(queryset, per_page=1)
        page = min(paginator.num_pages, page or 1)

        if not request.is_htmx:
            return redirect(
                self.get_thread_post_edits_url(post, min(paginator.num_pages, page))
            )

        if request.GET.get("modal"):
            template_name = self.modal_template_name
        else:
            template_name = self.partial_template_name

        context_data = self.get_thread_post_edit_context_data(
            request, post, paginator.get_page(page)
        )

        return render(request, template_name, context_data)


class PostEditRestoreView(PostEditView):
    template_name = "misago/post_edit_restore/index.html"

    def check_post_edit_permission(self, request: HttpRequest, post_edit: PostEdit):
        self.check_restore_post_edit_permission(request, post_edit)

    def execute_action(self, request, post_edit: PostEdit) -> HttpResponse:
        restore_post_edit(post_edit, request.user, request=request)

        messages.success(
            request,
            pgettext("restore post edit", "Post contents restored"),
        )

        return self.get_thread_post_redirect(request, post_edit.post)


class ThreadPostEditRestoreView(PostEditRestoreView):
    backend = thread_backend
    post_edit_backend = thread_post_edit_backend


class PrivateThreadPostEditRestoreView(PostEditRestoreView):
    backend = private_thread_backend
    post_edit_backend = private_thread_post_edit_backend


class PostEditHideView(PostEditView):
    template_name = "misago/post_edit_hide/index.html"

    def check_post_edit_permission(self, request: HttpRequest, post_edit: PostEdit):
        check_hide_post_edit_permission(request.user_permissions, post_edit)

    def execute_action(self, request, post_edit: PostEdit) -> HttpResponse:
        if not post_edit.is_hidden:
            hide_post_edit(post_edit, request.user, request=request)

            messages.success(
                request,
                pgettext("hide post edit", "Post edit hidden"),
            )

        post_edit_index = self.get_thread_post_edit_index(post_edit)
        return self.get_action_response(request, post_edit.post, post_edit_index)


class ThreadPostEditHideView(PostEditHideView):
    backend = thread_backend
    post_edit_backend = thread_post_edit_backend


class PrivateThreadPostEditHideView(PostEditHideView):
    backend = private_thread_backend
    post_edit_backend = private_thread_post_edit_backend


class PostEditUnhideView(PostEditView):
    def check_post_edit_permission(self, request: HttpRequest, post_edit: PostEdit):
        check_unhide_post_edit_permission(request.user_permissions, post_edit)

    def execute_action(self, request, post_edit: PostEdit) -> HttpResponse:
        if post_edit.is_hidden:
            unhide_post_edit(post_edit, request=request)

            messages.success(
                request,
                pgettext("unhide post edit", "Post edit unhidden"),
            )

        post_edit_index = self.get_thread_post_edit_index(post_edit)
        return self.get_action_response(request, post_edit.post, post_edit_index)


class ThreadPostEditUnhideView(PostEditUnhideView):
    backend = thread_backend
    post_edit_backend = thread_post_edit_backend


class PrivateThreadPostEditUnhideView(PostEditUnhideView):
    backend = private_thread_backend
    post_edit_backend = private_thread_post_edit_backend


class PostEditDeleteView(PostEditView):
    template_name = "misago/post_edit_delete/index.html"

    def check_post_edit_permission(self, request: HttpRequest, post_edit: PostEdit):
        check_delete_post_edit_permission(request.user_permissions, post_edit)

    def execute_action(self, request, post_edit: PostEdit) -> HttpResponse:
        post_edit_index = self.get_thread_post_edit_index(post_edit)
        delete_post_edit(post_edit, request=request)

        messages.success(
            request,
            pgettext("delete post edit", "Post edit deleted"),
        )

        return self.get_action_response(request, post_edit.post, post_edit_index)


class ThreadPostEditDeleteView(PostEditDeleteView):
    backend = thread_backend
    post_edit_backend = thread_post_edit_backend


class PrivateThreadPostEditDeleteView(PostEditDeleteView):
    backend = private_thread_backend
    post_edit_backend = private_thread_post_edit_backend
