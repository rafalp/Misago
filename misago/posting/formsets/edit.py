from django.http import HttpRequest

from ...attachments.models import Attachment
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
    attachments_permissions = request.user_permissions.get_attachment_permissions(
        post.category_id
    )

    formset = EditThreadPostFormset()
    formset.add_form(
        create_post_form(
            request,
            initial=post.original,
            attachments=list(Attachment.objects.filter(post=post)),
            attachments_permissions=attachments_permissions,
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
    formset = EditPrivateThreadPostFormset()
    formset.add_form(create_post_form(request, initial=post.original))
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
    attachments_permissions = request.user_permissions.get_attachment_permissions(
        post.category_id
    )

    formset = EditThreadFormset()
    formset.add_form(create_title_form(request, initial=post.thread.title))
    formset.add_form(
        create_post_form(
            request,
            initial=post.original,
            attachments=list(Attachment.objects.filter(post=post)),
            attachments_permissions=attachments_permissions,
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
    formset = EditPrivateThreadFormset()
    formset.add_form(create_title_form(request, initial=post.thread.title))
    formset.add_form(create_post_form(request, initial=post.original))
    return formset
