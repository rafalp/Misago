from django.http import HttpRequest

from ...threads.models import Post, Thread
from ..forms import create_post_form, create_title_form
from ..hooks import (
    get_edit_private_thread_post_formset_hook,
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
    formset.add_form(create_post_form(request, initial=post.original))
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


def get_edit_thread_formset(
    request: HttpRequest, thread: Thread, post: Post
) -> EditThreadFormset:
    return _get_edit_thread_formset_action(request, thread, post)


def _get_edit_thread_formset_action(
    request: HttpRequest, thread: Thread, post: Post
) -> EditThreadFormset:
    formset = EditThreadFormset()
    formset.add_form(create_title_form(request, initial=thread.title))
    formset.add_form(create_post_form(request, initial=post.original))
    return formset


def get_edit_private_thread_formset(
    request: HttpRequest, thread: Thread, post: Post
) -> EditPrivateThreadFormset:
    return _get_edit_private_thread_formset_action(request, thread, post)


def _get_edit_private_thread_formset_action(
    request: HttpRequest, thread: Thread, post: Post
) -> EditPrivateThreadFormset:
    formset = EditPrivateThreadFormset()
    formset.add_form(create_title_form(request, initial=thread.title))
    formset.add_form(create_post_form(request, initial=post.original))
    return formset
