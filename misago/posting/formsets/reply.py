from django.http import HttpRequest

from ...permissions.attachments import (
    can_upload_private_threads_attachments,
    can_upload_threads_attachments,
)
from ...threads.models import Thread
from ..forms import create_post_form
from ..hooks import get_reply_private_thread_formset_hook, get_reply_thread_formset_hook
from .formset import PostingFormset


class ReplyThreadFormset(PostingFormset):
    pass


class ReplyPrivateThreadFormset(PostingFormset):
    pass


def get_reply_thread_formset(
    request: HttpRequest, thread: Thread
) -> ReplyThreadFormset:
    return get_reply_thread_formset_hook(
        _get_reply_thread_formset_action, request, thread
    )


def _get_reply_thread_formset_action(
    request: HttpRequest, thread: Thread
) -> ReplyThreadFormset:
    formset = ReplyThreadFormset()
    formset.add_form(
        create_post_form(
            request,
            can_upload_attachments=can_upload_threads_attachments(
                request.user_permissions, thread.category
            ),
        )
    )
    return formset


def get_reply_private_thread_formset(
    request: HttpRequest, thread: Thread
) -> ReplyPrivateThreadFormset:
    return get_reply_private_thread_formset_hook(
        _get_reply_private_thread_formset_action, request, thread
    )


def _get_reply_private_thread_formset_action(
    request: HttpRequest, thread: Thread
) -> ReplyPrivateThreadFormset:
    can_upload_attachments = False
    if request.settings.allow_private_threads_attachments:
        can_upload_attachments = can_upload_private_threads_attachments(
            request.user_permissions
        )

    formset = ReplyPrivateThreadFormset()
    formset.add_form(
        create_post_form(
            request,
            can_upload_attachments=can_upload_attachments,
        )
    )
    return formset
