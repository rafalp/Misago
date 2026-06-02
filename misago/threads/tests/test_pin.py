from ..enums import ThreadPinned
from ..pin import (
    pin_thread_globally,
    pin_thread_in_category,
    unpin_thread,
)


def test_pin_thread_globally_pins_unpinned_thread(thread):
    assert pin_thread_globally(thread)
    assert thread.weight == ThreadPinned.EVERYWHERE

    thread.refresh_from_db()
    assert thread.weight == ThreadPinned.EVERYWHERE


def test_pin_thread_globally_pins_pinned_in_category_thread(thread):
    thread.weight = ThreadPinned.CATEGORY
    thread.save()

    assert pin_thread_globally(thread)
    assert thread.weight == ThreadPinned.EVERYWHERE

    thread.refresh_from_db()
    assert thread.weight == ThreadPinned.EVERYWHERE


def test_pin_thread_globally_doesnt_pin_globally_pinned_thread(
    django_assert_num_queries, thread
):
    thread.weight = ThreadPinned.EVERYWHERE
    thread.save()

    with django_assert_num_queries(0):
        assert not pin_thread_globally(thread)
        assert thread.weight == ThreadPinned.EVERYWHERE

    thread.refresh_from_db()
    assert thread.weight == ThreadPinned.EVERYWHERE


def test_pin_thread_globally_doesnt_save_thread_if_commit_is_false(
    django_assert_num_queries, thread
):
    with django_assert_num_queries(0):
        assert pin_thread_globally(thread, commit=False)
        assert thread.weight == ThreadPinned.EVERYWHERE

    thread.refresh_from_db()
    assert thread.weight != ThreadPinned.EVERYWHERE


def test_pin_thread_in_category_pins_unpinned_thread(thread):
    assert pin_thread_in_category(thread)
    assert thread.weight == ThreadPinned.CATEGORY

    thread.refresh_from_db()
    assert thread.weight == ThreadPinned.CATEGORY


def test_pin_thread_in_category_pins_pinned_globally_thread(thread):
    thread.weight = ThreadPinned.EVERYWHERE
    thread.save()

    assert pin_thread_in_category(thread)
    assert thread.weight == ThreadPinned.CATEGORY

    thread.refresh_from_db()
    assert thread.weight == ThreadPinned.CATEGORY


def test_pin_thread_in_category_doesnt_pin_in_category_pinned_thread(
    django_assert_num_queries, thread
):
    thread.weight = ThreadPinned.CATEGORY
    thread.save()

    with django_assert_num_queries(0):
        assert not pin_thread_in_category(thread)
        assert thread.weight == ThreadPinned.CATEGORY

    thread.refresh_from_db()
    assert thread.weight == ThreadPinned.CATEGORY


def test_pin_thread_in_category_doesnt_save_thread_if_commit_is_false(
    django_assert_num_queries, thread
):
    with django_assert_num_queries(0):
        assert pin_thread_in_category(thread, commit=False)
        assert thread.weight == ThreadPinned.CATEGORY

    thread.refresh_from_db()
    assert thread.weight != ThreadPinned.CATEGORY


def test_unpin_thread_unpins_globally_pinned_thread(thread):
    thread.weight = ThreadPinned.EVERYWHERE
    thread.save()

    assert unpin_thread(thread)
    assert thread.weight == ThreadPinned.NONE

    thread.refresh_from_db()
    assert thread.weight == ThreadPinned.NONE


def test_unpin_thread_unpins_pinned_in_category_thread(thread):
    thread.weight = ThreadPinned.CATEGORY
    thread.save()

    assert unpin_thread(thread)
    assert thread.weight == ThreadPinned.NONE

    thread.refresh_from_db()
    assert thread.weight == ThreadPinned.NONE


def test_unpin_thread_doesnt_unpin_unpinned_thread(django_assert_num_queries, thread):
    with django_assert_num_queries(0):
        assert not unpin_thread(thread)
        assert thread.weight == ThreadPinned.NONE

    thread.refresh_from_db()
    assert thread.weight == ThreadPinned.NONE


def test_unpin_thread_doesnt_save_thread_if_commit_is_false(
    django_assert_num_queries, thread
):
    thread.weight = ThreadPinned.CATEGORY
    thread.save()

    with django_assert_num_queries(0):
        assert unpin_thread(thread, commit=False)
        assert thread.weight == ThreadPinned.NONE

    thread.refresh_from_db()
    assert thread.weight != ThreadPinned.NONE
