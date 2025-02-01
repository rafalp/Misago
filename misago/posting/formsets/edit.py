from django.http import HttpRequest

from ...attachments.models import Attachment
from ...permissions.attachments import (
    can_upload_private_threads_attachments,
    can_upload_threads_attachments,
)
from ...threads.models import Post
from ..forms import create_post_form, create_title_form
from ..hooks import (
    get_edit_private_thread_formset_hook,
    get_edit_private_thread_post_formset_hook,
    get_edit_thread_formset_hook,
    get_edit_thread_post_formset_hook,
)
from .formset import PostingFormset


class EditThreadPostFormset(PostingFormset):
    pass


class EditPrivateThreadPostFormset(PostingFormset):
    pass


def get_edit_thread_post_formset(
    request: HttpRequest, post: Post
) -> EditThreadPostFormset:
    return get_edit_thread_post_formset_hook(
        _get_edit_thread_post_formset_action, request, post
    )


def _get_edit_thread_post_formset_action(
    request: HttpRequest, post: Post
) -> EditThreadPostFormset:
    formset = EditThreadPostFormset()
    formset.add_form(
        create_post_form(
            request,
            initial=post.original,
            attachments=get_post_attachments(post),
            can_upload_attachments=can_upload_threads_attachments(
                request.user_permissions, post.category
            ),
        )
    )
    return formset


def get_edit_private_thread_post_formset(
    request: HttpRequest, post: Post
) -> EditPrivateThreadPostFormset:
    return get_edit_private_thread_post_formset_hook(
        _get_edit_private_thread_post_formset_action, request, post
    )


def _get_edit_private_thread_post_formset_action(
    request: HttpRequest, post: Post
) -> EditPrivateThreadPostFormset:
    can_upload_attachments = False
    if request.settings.allow_private_threads_attachments:
        can_upload_attachments = can_upload_private_threads_attachments(
            request.user_permissions
        )

    formset = EditPrivateThreadPostFormset()
    formset.add_form(
        create_post_form(
            request,
            initial=post.original,
            attachments=get_post_attachments(post),
            can_upload_attachments=can_upload_attachments,
        )
    )
    return formset


class EditThreadFormset(PostingFormset):
    pass


class EditPrivateThreadFormset(PostingFormset):
    pass


def get_edit_thread_formset(request: HttpRequest, post: Post) -> EditThreadFormset:
    return get_edit_thread_formset_hook(_get_edit_thread_formset_action, request, post)


def _get_edit_thread_formset_action(
    request: HttpRequest, post: Post
) -> EditThreadFormset:
    formset = EditThreadFormset()
    formset.add_form(create_title_form(request, initial=post.thread.title))
    formset.add_form(
        create_post_form(
            request,
            initial=post.original,
            attachments=get_post_attachments(post),
            can_upload_attachments=can_upload_threads_attachments(
                request.user_permissions, post.category
            ),
        )
    )
    return formset


def get_edit_private_thread_formset(
    request: HttpRequest, post: Post
) -> EditPrivateThreadFormset:
    return get_edit_private_thread_formset_hook(
        _get_edit_private_thread_formset_action, request, post
    )


def _get_edit_private_thread_formset_action(
    request: HttpRequest, post: Post
) -> EditPrivateThreadFormset:
    can_upload_attachments = False
    if request.settings.allow_private_threads_attachments:
        can_upload_attachments = can_upload_private_threads_attachments(
            request.user_permissions
        )

    formset = EditPrivateThreadFormset()
    formset.add_form(create_title_form(request, initial=post.thread.title))
    formset.add_form(
        create_post_form(
            request,
            initial=post.original,
            attachments=get_post_attachments(post),
            can_upload_attachments=can_upload_attachments,
        )
    )
    return formset


def get_post_attachments(post: Post) -> list[Attachment]:
    return list(Attachment.objects.filter(post=post, is_deleted=False).order_by("-id"))
