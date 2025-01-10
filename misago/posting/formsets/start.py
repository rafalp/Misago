from django.http import HttpRequest

from ...categories.models import Category
from ...permissions.attachments import (
    get_private_threads_attachments_permissions,
    get_threads_attachments_permissions,
)
from ..forms import create_invite_users_form, create_post_form, create_title_form
from ..hooks import get_start_private_thread_formset_hook, get_start_thread_formset_hook
from .formset import PostingFormset


class StartThreadFormset(PostingFormset):
    pass


class StartPrivateThreadFormset(PostingFormset):
    pass


def get_start_thread_formset(
    request: HttpRequest, category: Category
) -> StartThreadFormset:
    return get_start_thread_formset_hook(
        _get_start_thread_formset_action, request, category
    )


def _get_start_thread_formset_action(
    request: HttpRequest, category: Category
) -> StartThreadFormset:
    attachments_permissions = get_threads_attachments_permissions(
        request.user_permissions, category.id
    )

    formset = StartThreadFormset()
    formset.add_form(create_title_form(request))
    formset.add_form(
        create_post_form(
            request,
            attachments_permissions=attachments_permissions,
        )
    )

    return formset


def get_start_private_thread_formset(
    request: HttpRequest, category: Category
) -> StartPrivateThreadFormset:
    return get_start_private_thread_formset_hook(
        _get_start_private_thread_formset_action, request, category
    )


def _get_start_private_thread_formset_action(
    request: HttpRequest, category: Category
) -> StartPrivateThreadFormset:
    attachments_permissions = None
    if request.settings.allow_private_threads_attachments:
        attachments_permissions = get_private_threads_attachments_permissions(
            request.user_permissions
        )

    formset = StartPrivateThreadFormset()
    formset.add_form(create_invite_users_form(request))
    formset.add_form(create_title_form(request))
    formset.add_form(
        create_post_form(
            request,
            attachments_permissions=attachments_permissions,
        )
    )

    return formset
