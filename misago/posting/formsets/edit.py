from django.http import HttpRequest

from ...attachments.models import Attachment
from ...permissions.attachments import (
    can_upload_private_threads_attachments,
    can_upload_threads_attachments,
)
from ...threads.models import Post
from ..forms import create_edit_reason_form, create_post_form, create_title_form
from ..hooks import (
    get_private_thread_edit_formset_hook,
    get_private_thread_post_edit_formset_hook,
    get_thread_edit_formset_hook,
    get_thread_post_edit_formset_hook,
)
from .formset import Formset


class ThreadPostEditFormset(Formset):
    pass


class PrivateThreadPostEditFormset(Formset):
    pass


def get_thread_post_edit_formset(
    request: HttpRequest, post: Post
) -> ThreadPostEditFormset:
    return get_thread_post_edit_formset_hook(
        _get_thread_post_edit_formset_action, request, post
    )


def _get_thread_post_edit_formset_action(
    request: HttpRequest, post: Post
) -> ThreadPostEditFormset:
    formset = ThreadPostEditFormset()
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
    formset.add_form(create_edit_reason_form(request))
    return formset


def get_private_thread_post_edit_formset(
    request: HttpRequest, post: Post
) -> PrivateThreadPostEditFormset:
    return get_private_thread_post_edit_formset_hook(
        _get_private_thread_post_edit_formset_action, request, post
    )


def _get_private_thread_post_edit_formset_action(
    request: HttpRequest, post: Post
) -> PrivateThreadPostEditFormset:
    can_upload_attachments = False
    if request.settings.allow_private_threads_attachments:
        can_upload_attachments = can_upload_private_threads_attachments(
            request.user_permissions
        )

    formset = PrivateThreadPostEditFormset()
    formset.add_form(
        create_post_form(
            request,
            initial=post.original,
            attachments=get_post_attachments(post),
            can_upload_attachments=can_upload_attachments,
        )
    )
    formset.add_form(create_edit_reason_form(request))
    return formset


class ThreadEditFormset(Formset):
    pass


class PrivateThreadEditFormset(Formset):
    pass


def get_thread_edit_formset(request: HttpRequest, post: Post) -> ThreadEditFormset:
    return get_thread_edit_formset_hook(_get_thread_edit_formset_action, request, post)


def _get_thread_edit_formset_action(
    request: HttpRequest, post: Post
) -> ThreadEditFormset:
    formset = ThreadEditFormset()
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
    formset.add_form(create_edit_reason_form(request))
    return formset


def get_private_thread_edit_formset(
    request: HttpRequest, post: Post
) -> PrivateThreadEditFormset:
    return get_private_thread_edit_formset_hook(
        _get_private_thread_edit_formset_action, request, post
    )


def _get_private_thread_edit_formset_action(
    request: HttpRequest, post: Post
) -> PrivateThreadEditFormset:
    can_upload_attachments = False
    if request.settings.allow_private_threads_attachments:
        can_upload_attachments = can_upload_private_threads_attachments(
            request.user_permissions
        )

    formset = PrivateThreadEditFormset()
    formset.add_form(create_title_form(request, initial=post.thread.title))
    formset.add_form(
        create_post_form(
            request,
            initial=post.original,
            attachments=get_post_attachments(post),
            can_upload_attachments=can_upload_attachments,
        )
    )
    formset.add_form(create_edit_reason_form(request))
    return formset


def get_post_attachments(post: Post) -> list[Attachment]:
    return list(Attachment.objects.filter(post=post, is_deleted=False).order_by("-id"))
