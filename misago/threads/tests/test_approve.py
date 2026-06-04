from ..approve import approve_thread


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
