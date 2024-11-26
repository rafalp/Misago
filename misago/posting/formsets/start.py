from django.http import HttpRequest

from ...categories.models import Category
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
    formset = StartThreadFormset()

    formset.add_form(create_title_form(request))
    formset.add_form(create_post_form(request))

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
    formset = StartPrivateThreadFormset()

    formset.add_form(create_invite_users_form(request))
    formset.add_form(create_title_form(request))
    formset.add_form(create_post_form(request))

    return formset
