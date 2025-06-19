from ..create import create_thread_update


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
