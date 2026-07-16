from ..hide import hide_thread_event


def test_hide_thread_event_hides_thread_event(thread_event):
    assert hide_thread_event(thread_event)

    thread_event.refresh_from_db()
    assert thread_event.is_hidden
    assert thread_event.hidden_by is None
    assert thread_event.hidden_by_name is None
    assert thread_event.hidden_by_slug is None
    assert thread_event.hidden_at


def test_hide_thread_event_hides_thread_event_and_sets_hidden_by_relation(
    thread_event, rf, user
):
    request = rf.get("/example/")
    request.user = user

    assert hide_thread_event(thread_event, request)

    thread_event.refresh_from_db()
    assert thread_event.is_hidden
    assert thread_event.hidden_by == user
    assert thread_event.hidden_by_name == user.username
    assert thread_event.hidden_by_slug == user.slug
    assert thread_event.hidden_at


def test_hide_thread_event_returns_false_if_thread_event_is_hidden(
    django_assert_num_queries, thread_event
):
    thread_event.is_hidden = True
    thread_event.save()

    with django_assert_num_queries(0):
        assert not hide_thread_event(thread_event)

    thread_event.refresh_from_db()
    assert thread_event.is_hidden
