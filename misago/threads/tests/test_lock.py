from ..lock import lock_thread, unlock_thread


def test_lock_thread_locks_thread(thread):
    assert lock_thread(thread)
    assert thread.is_locked

    thread.refresh_from_db()
    assert thread.is_locked


def test_lock_thread_doesnt_lock_locked_thread(django_assert_num_queries, thread):
    thread.is_locked = True
    thread.save()

    with django_assert_num_queries(0):
        assert not lock_thread(thread)
        assert thread.is_locked

    thread.refresh_from_db()
    assert thread.is_locked


def test_lock_thread_doesnt_save_thread_if_commit_is_false(
    django_assert_num_queries, thread
):
    with django_assert_num_queries(0):
        assert lock_thread(thread, commit=False)
        assert thread.is_locked

    thread.refresh_from_db()
    assert not thread.is_locked


def test_unlock_thread_unlocks_thread(thread):
    thread.is_locked = True
    thread.save()

    assert unlock_thread(thread)
    assert not thread.is_locked

    thread.refresh_from_db()
    assert not thread.is_locked


def test_unlock_thread_doesnt_unlock_unlocked_thread(django_assert_num_queries, thread):
    with django_assert_num_queries(0):
        assert not unlock_thread(thread)
        assert not thread.is_locked

    thread.refresh_from_db()
    assert not thread.is_locked


def test_unlock_thread_doesnt_save_thread_if_commit_is_false(
    django_assert_num_queries, thread
):
    thread.is_locked = True
    thread.save()

    with django_assert_num_queries(0):
        assert unlock_thread(thread, commit=False)
        assert not thread.is_locked

    thread.refresh_from_db()
    assert thread.is_locked
