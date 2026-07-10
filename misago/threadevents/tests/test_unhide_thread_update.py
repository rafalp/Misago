from ..hide import unhide_thread_update


def test_unhide_thread_update_unhides_thread_update(hidden_thread_update):
    assert hidden_thread_update.hidden_by
    assert hidden_thread_update.hidden_by_name
    assert hidden_thread_update.hidden_at

    assert unhide_thread_update(hidden_thread_update)

    hidden_thread_update.refresh_from_db()
    assert not hidden_thread_update.is_hidden
    assert hidden_thread_update.hidden_by is None
    assert hidden_thread_update.hidden_by_name is None
    assert hidden_thread_update.hidden_at is None


def test_unhide_thread_update_returns_false_if_thread_update_is_not_hidden(
    django_assert_num_queries, thread_update
):
    with django_assert_num_queries(0):
        assert not unhide_thread_update(thread_update)

    thread_update.refresh_from_db()
    assert not thread_update.is_hidden
