from ..hide import hide_thread, unhide_thread


def test_hide_thread_hides_thread(thread):
    assert hide_thread(thread)
    assert thread.is_hidden

    thread.refresh_from_db()
    assert thread.is_hidden


def test_hide_thread_doesnt_hide_hidden_thread(django_assert_num_queries, thread):
    thread.is_hidden = True
    thread.save()

    with django_assert_num_queries(0):
        assert not hide_thread(thread)
        assert thread.is_hidden

    thread.refresh_from_db()
    assert thread.is_hidden


def test_hide_thread_doesnt_save_thread_if_commit_is_false(
    django_assert_num_queries, thread
):
    with django_assert_num_queries(0):
        assert hide_thread(thread, commit=False)
        assert thread.is_hidden

    thread.refresh_from_db()
    assert not thread.is_hidden


def test_unhide_thread_unhides_thread(thread):
    thread.is_hidden = True
    thread.save()

    assert unhide_thread(thread)
    assert not thread.is_hidden

    thread.refresh_from_db()
    assert not thread.is_hidden


def test_unhide_thread_doesnt_unhide_unhidden_thread(django_assert_num_queries, thread):
    with django_assert_num_queries(0):
        assert not unhide_thread(thread)
        assert not thread.is_hidden

    thread.refresh_from_db()
    assert not thread.is_hidden


def test_unhide_thread_doesnt_save_thread_if_commit_is_false(
    django_assert_num_queries, thread
):
    thread.is_hidden = True
    thread.save()

    with django_assert_num_queries(0):
        assert unhide_thread(thread, commit=False)
        assert not thread.is_hidden

    thread.refresh_from_db()
    assert thread.is_hidden
