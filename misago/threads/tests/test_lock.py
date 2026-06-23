from ..lock import lock_post, lock_thread, unlock_post, unlock_thread


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


def test_lock_post_locks_post(post):
    assert lock_post(post)
    assert post.is_locked

    post.refresh_from_db()
    assert post.is_locked


def test_lock_post_doesnt_lock_locked_post(django_assert_num_queries, post):
    post.is_locked = True
    post.save()

    with django_assert_num_queries(0):
        assert not lock_post(post)
        assert post.is_locked

    post.refresh_from_db()
    assert post.is_locked


def test_lock_post_doesnt_save_post_if_commit_is_false(django_assert_num_queries, post):
    with django_assert_num_queries(0):
        assert lock_post(post, commit=False)
        assert post.is_locked

    post.refresh_from_db()
    assert not post.is_locked


def test_unlock_post_unlocks_post(post):
    post.is_locked = True
    post.save()

    assert unlock_post(post)
    assert not post.is_locked

    post.refresh_from_db()
    assert not post.is_locked


def test_unlock_post_doesnt_unlock_unlocked_post(django_assert_num_queries, post):
    with django_assert_num_queries(0):
        assert not unlock_post(post)
        assert not post.is_locked

    post.refresh_from_db()
    assert not post.is_locked


def test_unlock_post_doesnt_save_post_if_commit_is_false(
    django_assert_num_queries, post
):
    post.is_locked = True
    post.save()

    with django_assert_num_queries(0):
        assert unlock_post(post, commit=False)
        assert not post.is_locked

    post.refresh_from_db()
    assert post.is_locked
