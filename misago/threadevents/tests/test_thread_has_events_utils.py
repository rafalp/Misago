from ..create import create_test_thread_update
from ..threadflag import ensure_thread_has_events, sync_thread_has_events


def test_set_thread_has_updates_sets_thread_has_updates_flag(thread):
    assert ensure_thread_has_events(thread)
    assert thread.has_events

    thread.refresh_from_db()
    assert thread.has_events


def test_set_thread_has_updates_doesnt_set_thread_has_updates_flag_if_its_already_set(
    django_assert_num_queries, thread
):
    thread.has_events = True
    thread.save()

    with django_assert_num_queries(0):
        assert not ensure_thread_has_events(thread)
        assert thread.has_events

    thread.refresh_from_db()
    assert thread.has_events


def test_set_thread_has_updates_doesnt_save_thread_has_updates_flag_if_commit_is_false(
    django_assert_num_queries, thread
):
    with django_assert_num_queries(0):
        assert ensure_thread_has_events(thread, commit=False)
        assert thread.has_events

    thread.refresh_from_db()
    assert not thread.has_events


def test_sync_thread_has_updates_unsets_thread_has_updates_flag_for_thread_whithout_updates(
    django_assert_num_queries, thread
):
    thread.has_events = True
    thread.save()

    with django_assert_num_queries(2):
        assert sync_thread_has_events(thread)
        assert not thread.has_events

    thread.refresh_from_db()
    assert not thread.has_events


def test_sync_thread_has_updates_sets_thread_has_updates_flag_for_thread_with_updates(
    django_assert_num_queries, thread
):
    create_test_thread_update(thread, "DeletedUser")

    with django_assert_num_queries(2):
        assert sync_thread_has_events(thread)
        assert thread.has_events

    thread.refresh_from_db()
    assert thread.has_events


def test_sync_thread_has_updates_doesnt_change_thread_has_updates_flag_for_thread_without_updates(
    django_assert_num_queries, thread
):
    thread.has_events = False
    thread.save()

    with django_assert_num_queries(1):
        assert not sync_thread_has_events(thread)
        assert not thread.has_events

    thread.refresh_from_db()
    assert not thread.has_events


def test_sync_thread_has_updates_doesnt_change_thread_has_updates_flag_for_thread_with_updates(
    django_assert_num_queries, thread
):
    create_test_thread_update(thread, "DeletedUser")

    thread.has_events = True
    thread.save()

    with django_assert_num_queries(1):
        assert not sync_thread_has_events(thread)
        assert thread.has_events

    thread.refresh_from_db()
    assert thread.has_events


def test_sync_thread_has_updates_doesnt_save_thread_without_updates_if_commit_is_false(
    django_assert_num_queries, thread
):
    thread.has_events = True
    thread.save()

    with django_assert_num_queries(1):
        assert sync_thread_has_events(thread, commit=False)
        assert not thread.has_events

    thread.refresh_from_db()
    assert thread.has_events


def test_sync_thread_has_updates_doesnt_save_thread_with_updates_if_commit_is_false(
    django_assert_num_queries, thread
):
    create_test_thread_update(thread, "DeletedUser")

    with django_assert_num_queries(1):
        assert sync_thread_has_events(thread, commit=False)
        assert thread.has_events

    thread.refresh_from_db()
    assert not thread.has_events
