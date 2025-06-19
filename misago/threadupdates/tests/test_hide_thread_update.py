from ..hide import hide_thread_update, unhide_thread_update


def test_hide_thread_update_hides_thread_update(thread_update):
    assert hide_thread_update(thread_update)

    thread_update.refresh_from_db()
    assert thread_update.is_hidden
    assert thread_update.hidden_by is None
    assert thread_update.hidden_by_name is None
    assert thread_update.hidden_at


def test_hide_thread_update_hides_thread_update_and_sets_hidden_by_relation(
    thread_update, rf, user
):
    request = rf.get("/example/")
    request.user = user

    assert hide_thread_update(thread_update, request)

    thread_update.refresh_from_db()
    assert thread_update.is_hidden
    assert thread_update.hidden_by == user
    assert thread_update.hidden_by_name == user.username
    assert thread_update.hidden_at


def test_hide_thread_update_returns_false_if_thread_update_is_hidden(
    django_assert_num_queries, thread_update
):
    thread_update.is_hidden = True
    thread_update.save()

    with django_assert_num_queries(0):
        assert not hide_thread_update(thread_update)

    thread_update.refresh_from_db()
    assert thread_update.is_hidden
