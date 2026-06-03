from ..enums import ThreadPinned
from ..pin import pin_thread, unpin_thread


def test_pin_thread_pins_everywhere_unpinned_thread(thread):
    assert pin_thread(thread, everywhere=True)
    assert thread.pinned == ThreadPinned.EVERYWHERE

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.EVERYWHERE


def test_pin_thread_pins_everywhere_thread_pinned_in_category(thread):
    thread.pinned = ThreadPinned.CATEGORY
    thread.save()

    assert pin_thread(thread, everywhere=True)
    assert thread.pinned == ThreadPinned.EVERYWHERE

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.EVERYWHERE


def test_pin_thread_doesnt_pin_everywhere_thread_pinned_everywhere(
    django_assert_num_queries, thread
):
    thread.pinned = ThreadPinned.EVERYWHERE
    thread.save()

    with django_assert_num_queries(0):
        assert not pin_thread(thread, everywhere=True)
        assert thread.pinned == ThreadPinned.EVERYWHERE

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.EVERYWHERE


def test_pin_thread_everywhere_doesnt_save_thread_if_commit_is_false(
    django_assert_num_queries, thread
):
    with django_assert_num_queries(0):
        assert pin_thread(thread, everywhere=True, commit=False)
        assert thread.pinned == ThreadPinned.EVERYWHERE

    thread.refresh_from_db()
    assert thread.pinned != ThreadPinned.EVERYWHERE


def test_pin_thread_pins_in_category_unpinned_thread(thread):
    assert pin_thread(thread, everywhere=False)
    assert thread.pinned == ThreadPinned.CATEGORY

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.CATEGORY


def test_pin_thread_pins_in_category_thread_pinned_everywhere(thread):
    thread.pinned = ThreadPinned.EVERYWHERE
    thread.save()

    assert pin_thread(thread, everywhere=False)
    assert thread.pinned == ThreadPinned.CATEGORY

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.CATEGORY


def test_pin_thread_doesnt_pin_in_category_thread_pinned_in_category(
    django_assert_num_queries, thread
):
    thread.pinned = ThreadPinned.CATEGORY
    thread.save()

    with django_assert_num_queries(0):
        assert not pin_thread(thread, everywhere=False)
        assert thread.pinned == ThreadPinned.CATEGORY

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.CATEGORY


def test_pin_thread_in_category_doesnt_save_thread_if_commit_is_false(
    django_assert_num_queries, thread
):
    with django_assert_num_queries(0):
        assert pin_thread(thread, everywhere=False, commit=False)
        assert thread.pinned == ThreadPinned.CATEGORY

    thread.refresh_from_db()
    assert thread.pinned != ThreadPinned.CATEGORY


def test_unpin_thread_unpins_thread_pinned_in_everywhere(thread):
    thread.pinned = ThreadPinned.EVERYWHERE
    thread.save()

    assert unpin_thread(thread)
    assert thread.pinned == ThreadPinned.NONE

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.NONE


def test_unpin_thread_unpins_thread_pinned_in_category(thread):
    thread.pinned = ThreadPinned.CATEGORY
    thread.save()

    assert unpin_thread(thread)
    assert thread.pinned == ThreadPinned.NONE

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.NONE


def test_unpin_thread_doesnt_unpin_unpinned_thread(django_assert_num_queries, thread):
    with django_assert_num_queries(0):
        assert not unpin_thread(thread)
        assert thread.pinned == ThreadPinned.NONE

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.NONE


def test_unpin_thread_doesnt_save_thread_if_commit_is_false(
    django_assert_num_queries, thread
):
    thread.pinned = ThreadPinned.CATEGORY
    thread.save()

    with django_assert_num_queries(0):
        assert unpin_thread(thread, commit=False)
        assert thread.pinned == ThreadPinned.NONE

    thread.refresh_from_db()
    assert thread.pinned != ThreadPinned.NONE
