from django.http import HttpRequest
from django.utils.translation import pgettext

from ...categories.models import Category
from ...permissions.attachments import (
    can_upload_private_threads_attachments,
    can_upload_threads_attachments,
)
from ...permissions.checkutils import check_permissions
from ...permissions.polls import check_start_poll_permission
from ..enums import ThreadStartFormsetTabs
from ..forms import (
    create_members_form,
    create_poll_form,
    create_post_form,
    create_title_form,
)
from ..hooks import get_private_thread_start_formset_hook, get_thread_start_formset_hook
from .formset import Formset, TabbedFormset


class ThreadStartFormset(TabbedFormset):
    pass


class PrivateThreadStartFormset(Formset):
    pass


def get_thread_start_formset(
    request: HttpRequest, category: Category
) -> ThreadStartFormset:
    return get_thread_start_formset_hook(
        _get_thread_start_formset_action, request, category
    )


def _get_thread_start_formset_action(
    request: HttpRequest, category: Category
) -> ThreadStartFormset:
    formset = ThreadStartFormset()
    formset.add_tab(
        ThreadStartFormsetTabs.CONTENT, pgettext("start thread form tab", "Content")
    )

    formset.add_form(
        ThreadStartFormsetTabs.CONTENT,
        create_title_form(request),
    )
    formset.add_form(
        ThreadStartFormsetTabs.CONTENT,
        create_post_form(
            request,
            can_upload_attachments=can_upload_threads_attachments(
                request.user_permissions, category
            ),
        ),
    )

    with check_permissions() as can_start_poll:
        check_start_poll_permission(request.user_permissions)

    if can_start_poll:
        formset.add_tab(
            ThreadStartFormsetTabs.POLL, pgettext("start thread form tab", "Poll")
        )
        formset.add_form(
            ThreadStartFormsetTabs.POLL,
            create_poll_form(request),
        )

    return formset


def get_private_thread_start_formset(
    request: HttpRequest, category: Category
) -> PrivateThreadStartFormset:
    return get_private_thread_start_formset_hook(
        _get_private_thread_start_formset_action, request, category
    )


def _get_private_thread_start_formset_action(
    request: HttpRequest, category: Category
) -> PrivateThreadStartFormset:
    can_upload_attachments = False
    if request.settings.allow_private_threads_attachments:
        can_upload_attachments = can_upload_private_threads_attachments(
            request.user_permissions
        )

    formset = PrivateThreadStartFormset()
    formset.add_form(create_members_form(request))
    formset.add_form(create_title_form(request))
    formset.add_form(
        create_post_form(
            request,
            can_upload_attachments=can_upload_attachments,
        )
    )

    return formset
