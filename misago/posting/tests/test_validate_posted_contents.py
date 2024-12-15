from ..formsets import (
    get_edit_private_thread_formset,
    get_edit_private_thread_post_formset,
    get_edit_thread_formset,
    get_edit_thread_post_formset,
    get_reply_private_thread_formset,
    get_reply_thread_formset,
    get_start_private_thread_formset,
    get_start_thread_formset,
)
from ..state import (
    EditPrivateThreadPostState,
    EditThreadPostState,
    ReplyPrivateThreadState,
    ReplyThreadState,
    StartPrivateThreadState,
    StartThreadState,
)
from ..validators import validate_posted_contents


def test_validate_posted_contents_validates_new_thread(user_request, default_category):
    formset = get_start_thread_formset(user_request, default_category)
    state = StartThreadState(user_request, default_category)
    assert validate_posted_contents(formset, state)


def test_validate_posted_contents_validates_new_private_thread(
    user_request, private_threads_category
):
    formset = get_start_private_thread_formset(user_request, private_threads_category)
    state = StartPrivateThreadState(user_request, private_threads_category)
    assert validate_posted_contents(formset, state)


def test_validate_posted_contents_validates_new_thread_reply(
    user_request, other_user_thread
):
    formset = get_reply_thread_formset(user_request, other_user_thread)
    state = ReplyThreadState(user_request, other_user_thread)
    assert validate_posted_contents(formset, state)


def test_validate_posted_contents_validates_new_private_thread_reply(
    user_request, user_private_thread
):
    formset = get_reply_private_thread_formset(user_request, user_private_thread)
    state = ReplyPrivateThreadState(user_request, user_private_thread)
    assert validate_posted_contents(formset, state)


def test_validate_posted_contents_validates_edited_thread(user_request, user_thread):
    formset = get_edit_thread_formset(user_request, user_thread.first_post)
    state = EditThreadPostState(user_request, user_thread.first_post)
    assert validate_posted_contents(formset, state)


def test_validate_posted_contents_validates_edited_private_thread(
    user_request, user_private_thread
):
    formset = get_edit_private_thread_formset(
        user_request, user_private_thread.first_post
    )
    state = EditPrivateThreadPostState(user_request, user_private_thread.first_post)
    assert validate_posted_contents(formset, state)


def test_validate_posted_contents_validates_edited_thread_post(
    user_request, user_thread
):
    formset = get_edit_thread_post_formset(user_request, user_thread.first_post)
    state = EditThreadPostState(user_request, user_thread.first_post)
    assert validate_posted_contents(formset, state)


def test_validate_posted_contents_validates_edited_private_thread_post(
    user_request, user_private_thread
):
    formset = get_edit_private_thread_post_formset(
        user_request, user_private_thread.first_post
    )
    state = EditPrivateThreadPostState(user_request, user_private_thread.first_post)
    assert validate_posted_contents(formset, state)
