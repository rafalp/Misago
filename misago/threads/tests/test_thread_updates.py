import pytest

from ..models import ThreadUpdate
from ..threadupdates import (
    create_thread_update,
    delete_thread_update,
    hide_thread_update,
    unhide_thread_update,
)


def test_create_thread_update_creates_thread_update(default_category, thread, user):
    thread_update = create_thread_update(thread, "closed", user)

    assert thread_update.category == default_category
    assert thread_update.thread == thread

    thread_update.refresh_from_db()


def test_create_thread_update_creates_thread_update_with_actor(thread, user):
    thread_update = create_thread_update(thread, "closed", user)
    assert thread_update.actor == user
    assert thread_update.actor_name == user.username

    thread_update.refresh_from_db()


def test_create_thread_update_creates_thread_update_with_actor_name(thread):
    thread_update = create_thread_update(thread, "closed", "Misago")
    assert thread_update.actor is None
    assert thread_update.actor_name == "Misago"

    thread_update.refresh_from_db()


def test_create_thread_update_creates_thread_update_without_actor(thread):
    thread_update = create_thread_update(thread, "closed")
    assert thread_update.actor is None
    assert thread_update.actor_name is None

    thread_update.refresh_from_db()


def test_create_thread_update_creates_thread_update_with_context(thread):
    thread_update = create_thread_update(thread, "closed", context="Old title")
    assert thread_update.context == "Old title"
    assert thread_update.context_type is None
    assert thread_update.context_id is None

    thread_update.refresh_from_db()


def test_create_thread_update_creates_thread_update_with_full_context(
    thread, sibling_category
):
    thread_update = create_thread_update(
        thread, "closed", context_object=sibling_category, context=sibling_category.name
    )
    assert thread_update.context_type == "misago_categories.category"
    assert thread_update.context_id == sibling_category.id
    assert thread_update.context == sibling_category.name

    thread_update.refresh_from_db()

    assert (
        thread_update.context_model.objects.get(id=thread_update.context_id)
        == sibling_category
    )


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


def test_delete_thread_deletes_thread_update(thread_update):
    delete_thread_update(thread_update)

    with pytest.raises(ThreadUpdate.DoesNotExist):
        thread_update.refresh_from_db()

    assert not ThreadUpdate.objects.exists()
