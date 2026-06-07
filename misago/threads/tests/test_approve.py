from ..approve import (
    approve_thread,
    remove_thread_replies_approval,
    require_thread_replies_approval,
)


def test_approve_thread_approves_thread(unapproved_thread):
    assert approve_thread(unapproved_thread)
    assert not unapproved_thread.is_unapproved

    unapproved_thread.refresh_from_db()
    assert not unapproved_thread.is_unapproved


def test_approve_thread_doesnt_approve_approved_thread(
    django_assert_num_queries, thread
):
    with django_assert_num_queries(0):
        assert not approve_thread(thread)
        assert not thread.is_unapproved

    thread.refresh_from_db()
    assert not thread.is_unapproved


def test_approve_thread_doesnt_save_thread_if_commit_is_false(
    django_assert_num_queries, unapproved_thread
):
    with django_assert_num_queries(0):
        assert approve_thread(unapproved_thread, commit=False)
        assert not unapproved_thread.is_unapproved

    unapproved_thread.refresh_from_db()
    assert unapproved_thread.is_unapproved


def test_require_thread_replies_approval_sets_reply_approval_requirement(thread):
    assert require_thread_replies_approval(thread)
    assert thread.require_replies_approval

    thread.refresh_from_db()
    assert thread.require_replies_approval


def test_require_thread_replies_approval_doesnt_set_present_reply_approval_requirement(
    django_assert_num_queries, thread
):
    thread.require_replies_approval = True
    thread.save()

    with django_assert_num_queries(0):
        assert not require_thread_replies_approval(thread)
        assert thread.require_replies_approval

    thread.refresh_from_db()
    assert thread.require_replies_approval


def test_require_thread_replies_approval_doesnt_save_thread_if_commit_is_false(
    django_assert_num_queries, thread
):
    with django_assert_num_queries(0):
        assert require_thread_replies_approval(thread, commit=False)
        assert thread.require_replies_approval

    thread.refresh_from_db()
    assert not thread.require_replies_approval


def test_remove_thread_replies_approval_removes_approval_requirement(thread):
    thread.require_replies_approval = True
    thread.save()

    assert remove_thread_replies_approval(thread)
    assert not thread.require_replies_approval

    thread.refresh_from_db()
    assert not thread.require_replies_approval


def test_remove_thread_replies_approval_doesnt_remove_not_set_requirement(
    django_assert_num_queries, thread
):
    with django_assert_num_queries(0):
        assert not remove_thread_replies_approval(thread)
        assert not thread.require_replies_approval

    thread.refresh_from_db()
    assert not thread.require_replies_approval


def test_remove_thread_replies_approval_doesnt_save_thread_if_commit_is_false(
    django_assert_num_queries, thread
):
    thread.require_replies_approval = True
    thread.save()

    with django_assert_num_queries(0):
        assert remove_thread_replies_approval(thread, commit=False)
        assert not thread.require_replies_approval

    thread.refresh_from_db()
    assert thread.require_replies_approval
