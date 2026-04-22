from ..threadflag import set_thread_has_updates


def test_set_thread_has_updates_sets_thread_has_updates_flag(thread):
    assert set_thread_has_updates(thread)
    assert thread.has_updates

    thread.refresh_from_db()
    assert thread.has_updates


def test_set_thread_has_updates_doesnt_set_thread_has_updates_flag_if_its_already_set(
    django_assert_num_queries, thread
):
    thread.has_updates = True
    thread.save()

    with django_assert_num_queries(0):
        assert not set_thread_has_updates(thread)
        assert thread.has_updates

    thread.refresh_from_db()
    assert thread.has_updates


def test_set_thread_has_updates_doesnt_save_thread_has_updates_flag_if_commit_is_false(
    django_assert_num_queries, thread
):
    with django_assert_num_queries(0):
        assert set_thread_has_updates(thread, commit=False)
        assert thread.has_updates

    thread.refresh_from_db()
    assert not thread.has_updates
