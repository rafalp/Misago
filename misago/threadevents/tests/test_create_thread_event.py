from ..create import create_thread_event


def test_create_thread_event_creates_thread_event(default_category, thread, user):
    thread_event = create_thread_event(thread, "closed", user)

    assert thread_event.category == default_category
    assert thread_event.thread == thread

    thread_event.refresh_from_db()


def test_create_thread_event_creates_thread_event_with_actor(thread, user):
    thread_event = create_thread_event(thread, "closed", user)
    assert thread_event.actor == user
    assert thread_event.actor_name == user.username
    assert thread_event.actor_slug == user.slug

    thread_event.refresh_from_db()


def test_create_thread_event_creates_thread_event_with_actor_name(thread):
    thread_event = create_thread_event(thread, "closed", "Misago")
    assert thread_event.actor is None
    assert thread_event.actor_name == "Misago"
    assert thread_event.actor_slug == "misago"

    thread_event.refresh_from_db()


def test_create_thread_event_creates_thread_event_without_actor(thread):
    thread_event = create_thread_event(thread, "closed")
    assert thread_event.actor is None
    assert thread_event.actor_name is None
    assert thread_event.actor_slug is None

    thread_event.refresh_from_db()


def test_create_thread_event_creates_thread_event_with_context(thread):
    thread_event = create_thread_event(thread, "closed", context="Old title")
    assert thread_event.context == "Old title"
    assert thread_event.context_type is None
    assert thread_event.context_id is None

    thread_event.refresh_from_db()


def test_create_thread_event_creates_thread_event_with_full_context(
    thread, sibling_category
):
    thread_event = create_thread_event(
        thread, "closed", context_object=sibling_category, context=sibling_category.name
    )
    assert thread_event.context_type == "misago_categories.category"
    assert thread_event.context_id == sibling_category.id
    assert thread_event.context == sibling_category.name

    thread_event.refresh_from_db()

    assert (
        thread_event.context_model.objects.get(id=thread_event.context_id)
        == sibling_category
    )
