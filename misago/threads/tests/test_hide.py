from ..hide import hide_post, hide_thread, unhide_post, unhide_thread


def test_hide_thread_hides_thread(thread, user):
    assert hide_thread(thread, user)
    assert thread.is_hidden
    assert thread.hidden_at
    assert thread.hidden_by == user
    assert thread.hidden_by_name == user.username
    assert thread.hidden_by_slug == user.slug
    assert thread.hidden_reason is None

    thread.refresh_from_db()
    assert thread.is_hidden
    assert thread.hidden_at
    assert thread.hidden_by == user
    assert thread.hidden_by_name == user.username
    assert thread.hidden_by_slug == user.slug
    assert thread.hidden_reason is None


def test_hide_thread_hides_thread_by_deleted_user(thread):
    assert hide_thread(thread, "DeletedUser")
    assert thread.is_hidden
    assert thread.hidden_at
    assert thread.hidden_by is None
    assert thread.hidden_by_name == "DeletedUser"
    assert thread.hidden_by_slug == "deleteduser"
    assert thread.hidden_reason is None

    thread.refresh_from_db()
    assert thread.is_hidden
    assert thread.hidden_at
    assert thread.hidden_by is None
    assert thread.hidden_by_name == "DeletedUser"
    assert thread.hidden_by_slug == "deleteduser"
    assert thread.hidden_reason is None


def test_hide_thread_hides_thread_with_reason(thread, user):
    assert hide_thread(thread, user, "Lorem ipsum")
    assert thread.is_hidden
    assert thread.hidden_at
    assert thread.hidden_by == user
    assert thread.hidden_by_name == user.username
    assert thread.hidden_by_slug == user.slug
    assert thread.hidden_reason == "Lorem ipsum"

    thread.refresh_from_db()
    assert thread.is_hidden
    assert thread.hidden_at
    assert thread.hidden_by == user
    assert thread.hidden_by_name == user.username
    assert thread.hidden_by_slug == user.slug
    assert thread.hidden_reason == "Lorem ipsum"


def test_hide_thread_doesnt_hide_hidden_thread(django_assert_num_queries, thread, user):
    thread.is_hidden = True
    thread.save()

    with django_assert_num_queries(0):
        assert not hide_thread(thread, user, "Reason")
        assert thread.is_hidden

    thread.refresh_from_db()
    assert thread.is_hidden
    assert thread.hidden_at is None
    assert thread.hidden_by is None
    assert thread.hidden_by_name is None
    assert thread.hidden_by_slug is None
    assert thread.hidden_reason is None


def test_hide_thread_doesnt_save_thread_if_commit_is_false(
    django_assert_num_queries, thread, user
):
    with django_assert_num_queries(0):
        assert hide_thread(thread, user, "Reason", commit=False)
        assert thread.is_hidden
    assert thread.hidden_at
    assert thread.hidden_by == user
    assert thread.hidden_by_name == user.username
    assert thread.hidden_by_slug == user.slug
    assert thread.hidden_reason == "Reason"

    thread.refresh_from_db()
    assert not thread.is_hidden
    assert thread.hidden_at is None
    assert thread.hidden_by is None
    assert thread.hidden_by_name is None
    assert thread.hidden_by_slug is None
    assert thread.hidden_reason is None


def test_unhide_thread_unhides_thread(thread, user):
    hide_thread(thread, user, "Reason")

    assert unhide_thread(thread)
    assert not thread.is_hidden
    assert thread.hidden_at is None
    assert thread.hidden_by is None
    assert thread.hidden_by_name is None
    assert thread.hidden_by_slug is None
    assert thread.hidden_reason is None

    thread.refresh_from_db()
    assert not thread.is_hidden
    assert thread.hidden_at is None
    assert thread.hidden_by is None
    assert thread.hidden_by_name is None
    assert thread.hidden_by_slug is None
    assert thread.hidden_reason is None


def test_unhide_thread_doesnt_unhide_unhidden_thread(django_assert_num_queries, thread):
    with django_assert_num_queries(0):
        assert not unhide_thread(thread)
        assert not thread.is_hidden

    thread.refresh_from_db()
    assert not thread.is_hidden


def test_unhide_thread_doesnt_save_thread_if_commit_is_false(
    django_assert_num_queries, thread, user
):
    hide_thread(thread, user, "Reason")

    with django_assert_num_queries(0):
        assert unhide_thread(thread, commit=False)
        assert not thread.is_hidden
    assert thread.hidden_at is None
    assert thread.hidden_by is None
    assert thread.hidden_by_name is None
    assert thread.hidden_by_slug is None
    assert thread.hidden_reason is None

    thread.refresh_from_db()
    assert thread.is_hidden
    assert thread.hidden_at
    assert thread.hidden_by == user
    assert thread.hidden_by_name == user.username
    assert thread.hidden_by_slug == user.slug
    assert thread.hidden_reason == "Reason"


def test_hide_post_hides_post(post, user):
    assert hide_post(post, user)
    assert post.is_hidden
    assert post.hidden_at
    assert post.hidden_by == user
    assert post.hidden_by_name == user.username
    assert post.hidden_by_slug == user.slug
    assert post.hidden_reason is None

    post.refresh_from_db()
    assert post.is_hidden
    assert post.hidden_at
    assert post.hidden_by == user
    assert post.hidden_by_name == user.username
    assert post.hidden_by_slug == user.slug
    assert post.hidden_reason is None


def test_hide_post_hides_post_by_deleted_user(post):
    assert hide_post(post, "DeletedUser")
    assert post.is_hidden
    assert post.hidden_at
    assert post.hidden_by is None
    assert post.hidden_by_name == "DeletedUser"
    assert post.hidden_by_slug == "deleteduser"
    assert post.hidden_reason is None

    post.refresh_from_db()
    assert post.is_hidden
    assert post.hidden_at
    assert post.hidden_by is None
    assert post.hidden_by_name == "DeletedUser"
    assert post.hidden_by_slug == "deleteduser"
    assert post.hidden_reason is None


def test_hide_post_hides_post_with_reason(post, user):
    assert hide_post(post, user, "Lorem ipsum")
    assert post.is_hidden
    assert post.hidden_at
    assert post.hidden_by == user
    assert post.hidden_by_name == user.username
    assert post.hidden_by_slug == user.slug
    assert post.hidden_reason == "Lorem ipsum"

    post.refresh_from_db()
    assert post.is_hidden
    assert post.hidden_at
    assert post.hidden_by == user
    assert post.hidden_by_name == user.username
    assert post.hidden_by_slug == user.slug
    assert post.hidden_reason == "Lorem ipsum"


def test_hide_post_doesnt_hide_hidden_post(django_assert_num_queries, post, user):
    post.is_hidden = True
    post.save()

    with django_assert_num_queries(0):
        assert not hide_post(post, user, "Reason")
        assert post.is_hidden

    post.refresh_from_db()
    assert post.is_hidden
    assert post.hidden_at is None
    assert post.hidden_by is None
    assert post.hidden_by_name is None
    assert post.hidden_by_slug is None
    assert post.hidden_reason is None


def test_hide_post_doesnt_save_post_if_commit_is_false(
    django_assert_num_queries, post, user
):
    with django_assert_num_queries(0):
        assert hide_post(post, user, "Reason", commit=False)
        assert post.is_hidden
    assert post.hidden_at
    assert post.hidden_by == user
    assert post.hidden_by_name == user.username
    assert post.hidden_by_slug == user.slug
    assert post.hidden_reason == "Reason"

    post.refresh_from_db()
    assert not post.is_hidden
    assert post.hidden_at is None
    assert post.hidden_by is None
    assert post.hidden_by_name is None
    assert post.hidden_by_slug is None
    assert post.hidden_reason is None


def test_unhide_post_unhides_post(post, user):
    hide_post(post, user, "Reason")

    assert unhide_post(post)
    assert not post.is_hidden
    assert post.hidden_at is None
    assert post.hidden_by is None
    assert post.hidden_by_name is None
    assert post.hidden_by_slug is None
    assert post.hidden_reason is None

    post.refresh_from_db()
    assert not post.is_hidden
    assert post.hidden_at is None
    assert post.hidden_by is None
    assert post.hidden_by_name is None
    assert post.hidden_by_slug is None
    assert post.hidden_reason is None


def test_unhide_post_doesnt_unhide_unhidden_post(django_assert_num_queries, post):
    with django_assert_num_queries(0):
        assert not unhide_post(post)
        assert not post.is_hidden

    post.refresh_from_db()
    assert not post.is_hidden


def test_unhide_post_doesnt_save_post_if_commit_is_false(
    django_assert_num_queries, post, user
):
    hide_post(post, user, "Reason")

    with django_assert_num_queries(0):
        assert unhide_post(post, commit=False)
        assert not post.is_hidden
    assert post.hidden_at is None
    assert post.hidden_by is None
    assert post.hidden_by_name is None
    assert post.hidden_by_slug is None
    assert post.hidden_reason is None

    post.refresh_from_db()
    assert post.is_hidden
    assert post.hidden_at
    assert post.hidden_by == user
    assert post.hidden_by_name == user.username
    assert post.hidden_by_slug == user.slug
    assert post.hidden_reason == "Reason"
