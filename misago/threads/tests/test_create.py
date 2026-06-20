import pytest

from ..create import create_thread
from ..enums import ThreadPinned
from ..models import Thread


def test_create_thread_creates_thread(default_category):
    thread = create_thread(default_category, "Hello world!")

    assert thread.id
    assert thread.category == default_category
    assert thread.title == "Hello world!"
    assert thread.slug == "hello-world"
    assert not thread.pinned
    assert not thread.is_locked
    assert not thread.is_hidden

    thread.refresh_from_db()
    assert thread.category == default_category
    assert thread.title == "Hello world!"
    assert thread.slug == "hello-world"
    assert not thread.pinned
    assert not thread.is_locked
    assert not thread.is_hidden


def test_create_thread_creates_pinned_thread(default_category):
    thread = create_thread(
        default_category, "Hello world!", pinned=ThreadPinned.CATEGORY
    )

    assert thread.id
    assert thread.category == default_category
    assert thread.title == "Hello world!"
    assert thread.slug == "hello-world"
    assert thread.pinned == ThreadPinned.CATEGORY
    assert not thread.is_locked
    assert not thread.is_hidden

    thread.refresh_from_db()
    assert thread.category == default_category
    assert thread.title == "Hello world!"
    assert thread.slug == "hello-world"
    assert thread.pinned == ThreadPinned.CATEGORY
    assert not thread.is_locked
    assert not thread.is_hidden


def test_create_thread_creates_locked_thread(default_category):
    thread = create_thread(default_category, "Hello world!", is_locked=True)

    assert thread.id
    assert thread.category == default_category
    assert thread.title == "Hello world!"
    assert thread.slug == "hello-world"
    assert not thread.pinned
    assert thread.is_locked
    assert not thread.is_hidden

    thread.refresh_from_db()
    assert thread.category == default_category
    assert thread.title == "Hello world!"
    assert thread.slug == "hello-world"
    assert not thread.pinned
    assert thread.is_locked
    assert not thread.is_hidden


def test_create_thread_creates_hidden_thread(default_category):
    thread = create_thread(default_category, "Hello world!", is_hidden=True)

    assert thread.id
    assert thread.category == default_category
    assert thread.title == "Hello world!"
    assert thread.slug == "hello-world"
    assert not thread.pinned
    assert not thread.is_locked
    assert thread.is_hidden

    thread.refresh_from_db()
    assert thread.category == default_category
    assert thread.title == "Hello world!"
    assert thread.slug == "hello-world"
    assert not thread.pinned
    assert not thread.is_locked
    assert thread.is_hidden


def test_create_thread_creates_thread_with_all_options(default_category):
    thread = create_thread(
        default_category,
        "Hello world!",
        pinned=ThreadPinned.EVERYWHERE,
        is_locked=True,
        is_hidden=True,
    )

    assert thread.id
    assert thread.category == default_category
    assert thread.title == "Hello world!"
    assert thread.slug == "hello-world"
    assert thread.pinned == ThreadPinned.EVERYWHERE
    assert thread.is_locked
    assert thread.is_hidden

    thread.refresh_from_db()
    assert thread.category == default_category
    assert thread.title == "Hello world!"
    assert thread.slug == "hello-world"
    assert thread.pinned == ThreadPinned.EVERYWHERE
    assert thread.is_locked
    assert thread.is_hidden


def test_create_thread_doesnt_save_thread_if_commit_is_false(
    django_assert_num_queries, default_category
):
    with django_assert_num_queries(0):
        thread = create_thread(
            default_category,
            "Hello world!",
            pinned=ThreadPinned.EVERYWHERE,
            is_locked=True,
            is_hidden=True,
            commit=False,
        )

    assert not thread.id
    assert thread.category == default_category
    assert thread.title == "Hello world!"
    assert thread.slug == "hello-world"
    assert thread.pinned == ThreadPinned.EVERYWHERE
    assert thread.is_locked
    assert thread.is_hidden

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()
