from django.http import HttpRequest

from ...categories.models import Category
from ..hooks import get_start_private_thread_formset_hook, get_start_thread_formset_hook
from .formset import PostingFormset


class StartThreadFormset(PostingFormset):
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
    pass


class StartPrivateThreadFormset(PostingFormset):
    pass


def get_start_private_thread_formset(
    request: HttpRequest, category: Category
) -> StartPrivateThreadFormset:
    return get_start_private_thread_formset_hook(
        _get_start_private_thread_formset_action, request, category
    )


def _get_start_private_thread_formset_action(
    request: HttpRequest, category: Category
) -> StartPrivateThreadFormset:
    pass
