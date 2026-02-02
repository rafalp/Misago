from django.http import HttpRequest

from ...permissions.attachments import (
    can_upload_private_threads_attachments,
    can_upload_threads_attachments,
)
from ...threads.models import Thread
from ..forms import create_post_form
from ..hooks import (
    get_private_thread_reply_formset_hook,
    get_thread_reply_formset_hook,
)
from .formset import Formset


class ThreadReplyFormset(Formset):
    pass


class PrivateThreadReplyFormset(Formset):
    pass


def get_thread_reply_formset(
    request: HttpRequest, thread: Thread, initial: dict | None = None
) -> ThreadReplyFormset:
    return get_thread_reply_formset_hook(
        _get_thread_reply_formset_action, request, thread, initial
    )


def _get_thread_reply_formset_action(
    request: HttpRequest, thread: Thread, initial: dict | None
) -> ThreadReplyFormset:
    formset = ThreadReplyFormset()
    formset.add_form(
        create_post_form(
            request,
            can_upload_attachments=can_upload_threads_attachments(
                request.user_permissions, thread.category
            ),
            initial=initial.get("post") if initial else None,
        )
    )
    return formset


def get_private_thread_reply_formset(
    request: HttpRequest, thread: Thread, initial: dict | None = None
) -> PrivateThreadReplyFormset:
    return get_private_thread_reply_formset_hook(
        _get_private_thread_reply_formset_action, request, thread, initial
    )


def _get_private_thread_reply_formset_action(
    request: HttpRequest, thread: Thread, initial: dict | None
) -> PrivateThreadReplyFormset:
    can_upload_attachments = False
    if request.settings.allow_private_threads_attachments:
        can_upload_attachments = can_upload_private_threads_attachments(
            request.user_permissions
        )

    formset = PrivateThreadReplyFormset()
    formset.add_form(
        create_post_form(
            request,
            can_upload_attachments=can_upload_attachments,
            initial=initial.get("post") if initial else None,
        )
    )
    return formset
