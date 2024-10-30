from django.http import HttpRequest

from ...threads.models import Post
from ..forms import create_post_form
from .formset import PostingFormset


class EditThreadReplyFormset(PostingFormset):
    pass


def get_edit_thread_reply_formset(
    request: HttpRequest, post: Post
) -> EditThreadReplyFormset:
    return get_edit_thread_reply_formset_hook(
        _get_edit_thread_reply_formset_action, request, post
    )


def _get_edit_thread_reply_formset_action(
    request: HttpRequest, post: Post
) -> EditThreadReplyFormset:
    formset = EditThreadReplyFormset()
    formset.add_form(create_post_form(request))
    return formset


class EditPrivateThreadReplyFormset(PostingFormset):
    pass


def get_edit_private_thread_reply_formset(
    request: HttpRequest, post: Post
) -> EditPrivateThreadReplyFormset:
    return get_edit_private_thread_reply_formset_hook(
        _get_edit_private_thread_reply_formset_action, request, post
    )


def _get_edit_private_thread_reply_formset_action(
    request: HttpRequest, post: Post
) -> EditPrivateThreadReplyFormset:
    formset = EditPrivateThreadReplyFormset()
    formset.add_form(create_post_form(request))
    return formset
