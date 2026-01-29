from django.core.paginator import Page
from django.http import Http404, HttpRequest
from django.urls import reverse

from ..permissions.edits import check_restore_post_edit_permission
from ..permissions.enums import CategoryPermission
from ..permissions.privatethreads import check_edit_private_thread_post_permission
from ..permissions.threads import check_edit_thread_post_permission
from ..threads.models import Post
from .hooks import (
    get_private_thread_post_edits_view_context_data_hook,
    get_thread_post_edits_view_context_data_hook,
)
from .models import PostEdit


class PostEditViewBackend:
    partial_template_name = "misago/post_edits/partial.html"
    modal_template_name = "misago/post_edits/modal/index.html"
    edit_diff_template_name = "misago/post_edits/edit_diff.html"

    post_edit_restore_url: str
    post_edit_hide_url: str
    post_edit_unhide_url: str
    post_edit_delete_url: str

    def get_thread_post_edit(
        self, request: HttpRequest, post: Post, post_edit_id: int
    ) -> PostEdit:
        try:
            post_edit = PostEdit.objects.get(id=post_edit_id, post=post)
            post_edit.category = post.category
            post_edit.thread = post.thread
            post_edit.post = post
            return post_edit
        except PostEdit.DoesNotExist:
            raise Http404()

    def get_thread_post_edit_index(self, post_edit: PostEdit) -> int | None:
        return (
            PostEdit.objects.filter(post=post_edit.post, id__lte=post_edit.id).count()
            or None
        )

    def check_restore_post_edit_permission(
        self, request: HttpRequest, post_edit: PostEdit
    ):
        raise NotImplementedError()

    def get_attachment_permission(
        self, request: HttpRequest, post: Post, attachment: dict
    ) -> bool:
        raise NotImplementedError()

    def get_context_data_hook(
        self, action, request: HttpRequest, post: Post, page: Page
    ) -> dict:
        raise NotImplementedError()

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

    def check_restore_post_edit_permission(
        self, request: HttpRequest, post_edit: PostEdit
    ):
        check_restore_post_edit_permission(request.user_permissions, post_edit)
        check_edit_thread_post_permission(
            request.user_permissions,
            post_edit.category,
            post_edit.thread,
            post_edit.post,
        )

    def get_attachment_permission(
        self, request: HttpRequest, post: Post, attachment: dict
    ) -> bool:
        if (
            request.user.is_authenticated
            and request.user.id == attachment["uploader_id"]
        ):
            return True

        return (
            post.category_id
            in request.user_permissions.categories[CategoryPermission.ATTACHMENTS]
        )

    def get_context_data_hook(
        self, action, request: HttpRequest, post: Post, page: Page
    ) -> dict:
        return get_thread_post_edits_view_context_data_hook(action, request, post, page)


class PrivateThreadPostEditViewBackend(PostEditViewBackend):
    post_edit_restore_url = "misago:private-thread-post-edit-restore"
    post_edit_hide_url = "misago:private-thread-post-edit-hide"
    post_edit_unhide_url = "misago:private-thread-post-edit-unhide"
    post_edit_delete_url = "misago:private-thread-post-edit-delete"

    def check_restore_post_edit_permission(
        self, request: HttpRequest, post_edit: PostEdit
    ):
        check_restore_post_edit_permission(request.user_permissions, post_edit)
        check_edit_private_thread_post_permission(
            request.user_permissions, post_edit.thread, post_edit.post
        )

    def get_attachment_permission(
        self, request: HttpRequest, post: Post, attachment: dict
    ) -> bool:
        return True

    def get_context_data_hook(
        self, action, request: HttpRequest, post: Post, page: Page
    ) -> dict:
        return get_private_thread_post_edits_view_context_data_hook(
            action, request, post, page
        )


thread_post_edit_backend = ThreadPostEditViewBackend()
private_thread_post_edit_backend = PrivateThreadPostEditViewBackend()
