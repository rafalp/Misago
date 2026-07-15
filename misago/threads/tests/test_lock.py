from ..lock import lock_post, lock_thread, unlock_post, unlock_thread


def test_lock_thread_locks_thread(thread, user):
    assert lock_thread(thread, user)
    assert thread.is_locked
    assert thread.locked_at
    assert thread.locked_by == user
    assert thread.locked_by_name == user.username
    assert thread.locked_by_slug == user.slug
    assert thread.lock_reason is None

    thread.refresh_from_db()
    assert thread.is_locked
    assert thread.locked_at
    assert thread.locked_by == user
    assert thread.locked_by_name == user.username
    assert thread.locked_by_slug == user.slug
    assert thread.lock_reason is None


def test_lock_thread_locks_thread_by_deleted_user(thread):
    assert lock_thread(thread, "DeletedUser")
    assert thread.is_locked
    assert thread.locked_at
    assert thread.locked_by is None
    assert thread.locked_by_name == "DeletedUser"
    assert thread.locked_by_slug == "deleteduser"
    assert thread.lock_reason is None

    thread.refresh_from_db()
    assert thread.is_locked
    assert thread.locked_at
    assert thread.locked_by is None
    assert thread.locked_by_name == "DeletedUser"
    assert thread.locked_by_slug == "deleteduser"
    assert thread.lock_reason is None


def test_lock_thread_locks_thread_with_reason(thread, user):
    assert lock_thread(thread, user, "Lorem ipsum")
    assert thread.is_locked
    assert thread.locked_at
    assert thread.locked_by == user
    assert thread.locked_by_name == user.username
    assert thread.locked_by_slug == user.slug
    assert thread.lock_reason == "Lorem ipsum"

    thread.refresh_from_db()
    assert thread.is_locked
    assert thread.locked_at
    assert thread.locked_by == user
    assert thread.locked_by_name == user.username
    assert thread.locked_by_slug == user.slug
    assert thread.lock_reason == "Lorem ipsum"


def test_lock_thread_doesnt_lock_locked_thread(django_assert_num_queries, thread, user):
    thread.is_locked = True
    thread.save()

    with django_assert_num_queries(0):
        assert not lock_thread(thread, user, "Reason")
        assert thread.is_locked

    thread.refresh_from_db()
    assert thread.is_locked
    assert thread.locked_at is None
    assert thread.locked_by is None
    assert thread.locked_by_name is None
    assert thread.locked_by_slug is None
    assert thread.lock_reason is None


def test_lock_thread_doesnt_save_thread_if_commit_is_false(
    django_assert_num_queries, thread, user
):
    with django_assert_num_queries(0):
        assert lock_thread(thread, user, "Reason", commit=False)
        assert thread.is_locked

    assert thread.locked_at
    assert thread.locked_by == user
    assert thread.locked_by_name == user.username
    assert thread.locked_by_slug == user.slug
    assert thread.lock_reason == "Reason"

    thread.refresh_from_db()
    assert not thread.is_locked
    assert thread.locked_at is None
    assert thread.locked_by is None
    assert thread.locked_by_name is None
    assert thread.locked_by_slug is None
    assert thread.lock_reason is None


def test_unlock_thread_unlocks_thread(thread, user):
    lock_thread(thread, user, "Reason")

    assert unlock_thread(thread)
    assert not thread.is_locked
    assert thread.locked_at is None
    assert thread.locked_by is None
    assert thread.locked_by_name is None
    assert thread.locked_by_slug is None
    assert thread.lock_reason is None

    thread.refresh_from_db()
    assert not thread.is_locked
    assert thread.locked_at is None
    assert thread.locked_by is None
    assert thread.locked_by_name is None
    assert thread.locked_by_slug is None
    assert thread.lock_reason is None


def test_unlock_thread_doesnt_unlock_unlocked_thread(django_assert_num_queries, thread):
    with django_assert_num_queries(0):
        assert not unlock_thread(thread)
        assert not thread.is_locked

    thread.refresh_from_db()
    assert not thread.is_locked


def test_unlock_thread_doesnt_save_thread_if_commit_is_false(
    django_assert_num_queries, thread, user
):
    lock_thread(thread, user, "Reason")

    with django_assert_num_queries(0):
        assert unlock_thread(thread, commit=False)
        assert not thread.is_locked

    assert thread.locked_at is None
    assert thread.locked_by is None
    assert thread.locked_by_name is None
    assert thread.locked_by_slug is None
    assert thread.lock_reason is None

    thread.refresh_from_db()
    assert thread.is_locked
    assert thread.locked_at
    assert thread.locked_by == user
    assert thread.locked_by_name == user.username
    assert thread.locked_by_slug == user.slug
    assert thread.lock_reason == "Reason"


def test_lock_post_locks_post(post, user):
    assert lock_post(post, user)
    assert post.is_locked
    assert post.locked_at
    assert post.locked_by == user
    assert post.locked_by_name == user.username
    assert post.locked_by_slug == user.slug
    assert post.lock_reason is None

    post.refresh_from_db()
    assert post.is_locked
    assert post.locked_at
    assert post.locked_by == user
    assert post.locked_by_name == user.username
    assert post.locked_by_slug == user.slug
    assert post.lock_reason is None


def test_lock_post_locks_post_by_deleted_user(post):
    assert lock_post(post, "DeletedUser")
    assert post.is_locked
    assert post.locked_at
    assert post.locked_by is None
    assert post.locked_by_name == "DeletedUser"
    assert post.locked_by_slug == "deleteduser"
    assert post.lock_reason is None

    post.refresh_from_db()
    assert post.is_locked
    assert post.locked_at
    assert post.locked_by is None
    assert post.locked_by_name == "DeletedUser"
    assert post.locked_by_slug == "deleteduser"
    assert post.lock_reason is None


def test_lock_post_locks_post_with_reason(post, user):
    assert lock_post(post, user, "Lorem ipsum")
    assert post.is_locked
    assert post.locked_at
    assert post.locked_by == user
    assert post.locked_by_name == user.username
    assert post.locked_by_slug == user.slug
    assert post.lock_reason == "Lorem ipsum"

    post.refresh_from_db()
    assert post.is_locked
    assert post.locked_at
    assert post.locked_by == user
    assert post.locked_by_name == user.username
    assert post.locked_by_slug == user.slug
    assert post.lock_reason == "Lorem ipsum"


def test_lock_post_doesnt_lock_locked_post(django_assert_num_queries, post, user):
    post.is_locked = True
    post.save()

    with django_assert_num_queries(0):
        assert not lock_post(post, user, "Reason")
        assert post.is_locked

    post.refresh_from_db()
    assert post.is_locked
    assert post.locked_at is None
    assert post.locked_by is None
    assert post.locked_by_name is None
    assert post.locked_by_slug is None
    assert post.lock_reason is None


def test_lock_post_doesnt_save_post_if_commit_is_false(
    django_assert_num_queries, post, user
):
    with django_assert_num_queries(0):
        assert lock_post(post, user, "Reason", commit=False)
        assert post.is_locked

    assert post.locked_at
    assert post.locked_by == user
    assert post.locked_by_name == user.username
    assert post.locked_by_slug == user.slug
    assert post.lock_reason == "Reason"

    post.refresh_from_db()
    assert not post.is_locked
    assert post.locked_at is None
    assert post.locked_by is None
    assert post.locked_by_name is None
    assert post.locked_by_slug is None
    assert post.lock_reason is None


def test_unlock_post_unlocks_post(post, user):
    lock_post(post, user, "Reason")

    assert unlock_post(post)
    assert not post.is_locked
    assert post.locked_at is None
    assert post.locked_by is None
    assert post.locked_by_name is None
    assert post.locked_by_slug is None
    assert post.lock_reason is None

    post.refresh_from_db()
    assert not post.is_locked
    assert post.locked_at is None
    assert post.locked_by is None
    assert post.locked_by_name is None
    assert post.locked_by_slug is None
    assert post.lock_reason is None


def test_unlock_post_doesnt_unlock_unlocked_post(django_assert_num_queries, post):
    with django_assert_num_queries(0):
        assert not unlock_post(post)
        assert not post.is_locked

    post.refresh_from_db()
    assert not post.is_locked


def test_unlock_post_doesnt_save_post_if_commit_is_false(
    django_assert_num_queries, post, user
):
    lock_post(post, user, "Reason")

    with django_assert_num_queries(0):
        assert unlock_post(post, commit=False)
        assert not post.is_locked
    assert post.locked_at is None
    assert post.locked_by is None
    assert post.locked_by_name is None
    assert post.locked_by_slug is None
    assert post.lock_reason is None

    post.refresh_from_db()
    assert post.is_locked
    assert post.locked_at
    assert post.locked_by == user
    assert post.locked_by_name == user.username
    assert post.locked_by_slug == user.slug
    assert post.lock_reason == "Reason"
