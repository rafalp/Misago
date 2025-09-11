from ..formsets import (
    get_private_thread_edit_formset,
    get_private_thread_post_edit_formset,
    get_private_thread_reply_formset,
    get_private_thread_start_formset,
    get_thread_edit_formset,
    get_thread_post_edit_formset,
    get_thread_reply_formset,
    get_thread_start_formset,
)
from ..state import (
    PrivateThreadPostEditState,
    PrivateThreadReplyState,
    PrivateThreadStartState,
    ThreadPostEditState,
    ThreadReplyState,
    ThreadStartState,
)
from ..validators import validate_posted_contents


def test_validate_posted_contents_validates_new_thread(user_request, default_category):
    formset = get_thread_start_formset(user_request, default_category)
    state = ThreadStartState(user_request, default_category)
    assert validate_posted_contents(formset, state)


def test_validate_posted_contents_validates_new_private_thread(
    user_request, private_threads_category
):
    formset = get_private_thread_start_formset(user_request, private_threads_category)
    state = PrivateThreadStartState(user_request, private_threads_category)
    assert validate_posted_contents(formset, state)


def test_validate_posted_contents_validates_new_thread_reply(
    user_request, other_user_thread
):
    formset = get_thread_reply_formset(user_request, other_user_thread)
    state = ThreadReplyState(user_request, other_user_thread)
    assert validate_posted_contents(formset, state)


def test_validate_posted_contents_validates_new_private_thread_reply(
    user_request, user_private_thread
):
    formset = get_private_thread_reply_formset(user_request, user_private_thread)
    state = PrivateThreadReplyState(user_request, user_private_thread)
    assert validate_posted_contents(formset, state)


def test_validate_posted_contents_validates_edited_thread(user_request, user_thread):
    formset = get_thread_edit_formset(user_request, user_thread.first_post)
    state = ThreadPostEditState(user_request, user_thread.first_post)
    assert validate_posted_contents(formset, state)


def test_validate_posted_contents_validates_edited_private_thread(
    user_request, user_private_thread
):
    formset = get_private_thread_edit_formset(
        user_request, user_private_thread.first_post
    )
    state = PrivateThreadPostEditState(user_request, user_private_thread.first_post)
    assert validate_posted_contents(formset, state)


def test_validate_posted_contents_validates_edited_thread_post(
    user_request, user_thread
):
    formset = get_thread_post_edit_formset(user_request, user_thread.first_post)
    state = ThreadPostEditState(user_request, user_thread.first_post)
    assert validate_posted_contents(formset, state)


def test_validate_posted_contents_validates_edited_private_thread_post(
    user_request, user_private_thread
):
    formset = get_private_thread_post_edit_formset(
        user_request, user_private_thread.first_post
    )
    state = PrivateThreadPostEditState(user_request, user_private_thread.first_post)
    assert validate_posted_contents(formset, state)
