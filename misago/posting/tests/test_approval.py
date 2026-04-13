from ..approval import (
    require_private_thread_approval,
    require_private_thread_reply_approval,
    require_thread_approval,
    require_thread_reply_approval,
)
from ..state import (
    PrivateThreadReplyState,
    PrivateThreadStartState,
    ThreadReplyState,
    ThreadStartState,
)


def test_require_thread_approval_returns_false_for_non_moderated_user(
    user_request, default_category
):
    state = ThreadStartState(user_request, default_category)
    assert not require_thread_approval(state)


def test_require_thread_approval_returns_true_for_category_requiring_threads_approval(
    user_request, default_category
):
    default_category.require_threads_approval = True
    default_category.save()

    state = ThreadStartState(user_request, default_category)
    assert require_thread_approval(state)


def test_require_thread_approval_returns_true_for_user_requiring_approval(
    user_request, user, default_category
):
    user.require_content_approval = True
    user.save()

    state = ThreadStartState(user_request, default_category)
    assert require_thread_approval(state)


def test_require_thread_approval_returns_false_for_category_requiring_threads_approval_and_user_bypass_approval(
    members_group, user_request, default_category
):
    members_group.bypass_content_approval = True
    members_group.save()

    default_category.require_threads_approval = True
    default_category.save()

    state = ThreadStartState(user_request, default_category)
    assert not require_thread_approval(state)


def test_require_thread_approval_returns_true_for_user_requiring_approval_with_bypass_approval(
    members_group, user_request, user, default_category
):
    members_group.bypass_content_approval = True
    members_group.save()

    user.require_content_approval = True
    user.save()

    state = ThreadStartState(user_request, default_category)
    assert require_thread_approval(state)


def test_require_thread_reply_approval_returns_false_for_non_moderated_user(
    user_request, thread
):
    state = ThreadReplyState(user_request, thread)
    assert not require_thread_reply_approval(state)


def test_require_thread_reply_approval_returns_true_for_category_requiring_replies_approval(
    user_request, thread
):
    thread.category.require_replies_approval = True
    thread.category.save()

    state = ThreadReplyState(user_request, thread)
    assert require_thread_reply_approval(state)


def test_require_thread_reply_approval_returns_true_for_thread_requiring_replies_approval(
    user_request, thread
):
    thread.require_replies_approval = True
    thread.save()

    state = ThreadReplyState(user_request, thread)
    assert require_thread_reply_approval(state)


def test_require_thread_reply_approval_returns_true_for_user_requiring_approval(
    user_request, user, thread
):
    user.require_content_approval = True
    user.save()

    state = ThreadReplyState(user_request, thread)
    assert require_thread_reply_approval(state)


def test_require_thread_reply_approval_returns_false_for_category_requiring_threads_approval_and_user_bypass_approval(
    members_group, user_request, thread
):
    members_group.bypass_content_approval = True
    members_group.save()

    thread.category.require_replies_approval = True
    thread.category.save()

    state = ThreadReplyState(user_request, thread)
    assert not require_thread_reply_approval(state)


def test_require_thread_reply_approval_returns_false_for_thread_requiring_threads_approval_and_user_bypass_approval(
    members_group, user_request, thread
):
    members_group.bypass_content_approval = True
    members_group.save()

    thread.require_replies_approval = True
    thread.save()

    state = ThreadReplyState(user_request, thread)
    assert not require_thread_reply_approval(state)


def test_require_thread_reply_approval_returns_true_for_user_requiring_approval_with_bypass_approval(
    members_group, user_request, user, thread
):
    members_group.bypass_content_approval = True
    members_group.save()

    user.require_content_approval = True
    user.save()

    state = ThreadReplyState(user_request, thread)
    assert require_thread_reply_approval(state)


def test_require_private_thread_approval_returns_false_for_non_moderated_user(
    user_request, private_threads_category
):
    state = PrivateThreadStartState(user_request, private_threads_category)
    assert not require_private_thread_approval(state)


def test_require_private_thread_approval_returns_true_for_user_requiring_approval(
    user_request, user, private_threads_category
):
    user.require_content_approval = True
    user.save()

    state = PrivateThreadStartState(user_request, private_threads_category)
    assert require_private_thread_approval(state)


def test_require_private_thread_approval_returns_true_for_user_requiring_approval_with_bypass_approval(
    members_group, user_request, user, private_threads_category
):
    members_group.bypass_content_approval = True
    members_group.save()

    user.require_content_approval = True
    user.save()

    state = PrivateThreadStartState(user_request, private_threads_category)
    assert require_private_thread_approval(state)


def test_require_private_thread_reply_approval_returns_false_for_non_moderated_user(
    user_request, other_user_private_thread
):
    state = PrivateThreadReplyState(user_request, other_user_private_thread)
    assert not require_private_thread_reply_approval(state)


def test_require_private_thread_reply_approval_returns_true_for_user_requiring_approval(
    user_request, user, other_user_private_thread
):
    user.require_content_approval = True
    user.save()

    state = PrivateThreadReplyState(user_request, other_user_private_thread)
    assert require_private_thread_reply_approval(state)


def test_require_private_thread_reply_approval_returns_true_for_user_requiring_approval_with_bypass_approval(
    members_group, user_request, user, other_user_private_thread
):
    members_group.bypass_content_approval = True
    members_group.save()

    user.require_content_approval = True
    user.save()

    state = PrivateThreadReplyState(user_request, other_user_private_thread)
    assert require_private_thread_reply_approval(state)
