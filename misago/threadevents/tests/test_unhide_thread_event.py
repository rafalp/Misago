from ..hide import unhide_thread_event


def test_unhide_thread_event_unhides_thread_event(hidden_thread_event):
    assert hidden_thread_event.hidden_by
    assert hidden_thread_event.hidden_by_name
    assert hidden_thread_event.hidden_at

    assert unhide_thread_event(hidden_thread_event)

    hidden_thread_event.refresh_from_db()
    assert not hidden_thread_event.is_hidden
    assert hidden_thread_event.hidden_by is None
    assert hidden_thread_event.hidden_by_name is None
    assert hidden_thread_event.hidden_at is None


def test_unhide_thread_event_returns_false_if_thread_event_is_not_hidden(
    django_assert_num_queries, thread_event
):
    with django_assert_num_queries(0):
        assert not unhide_thread_event(thread_event)

    thread_event.refresh_from_db()
    assert not thread_event.is_hidden
