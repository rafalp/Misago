from ..threadupdates import (
    create_approved_thread_update,
    create_changed_title_thread_update,
    create_invited_thread_update,
    create_moved_thread_update,
    thread_updates_renderer,
)


def test_thread_updates_renderer_renders_simple_action(thread, user):
    thread_update = create_approved_thread_update(thread, user)
    data = thread_updates_renderer.render_thread_update(thread_update, {})
    assert data == {"description": "Approved thread", "icon": "verified_user"}


def test_thread_updates_renderer_renders_action_with_text_context(thread, user):
    thread_update = create_changed_title_thread_update(thread, "Old title", user)
    data = thread_updates_renderer.render_thread_update(thread_update, {})
    assert data == {
        "description": "Changed thread title from <em>Old title</em>",
        "icon": "edit",
    }


def test_thread_updates_renderer_renders_action_with_category_context(
    thread, user, default_category
):
    thread_update = create_moved_thread_update(thread, default_category, user)
    data = thread_updates_renderer.render_thread_update(
        thread_update, {"categories": {default_category.id: default_category}}
    )
    assert data == {
        "description": (
            f'Moved thread from <a href="{default_category.get_absolute_url()}">First category</a>'
        ),
        "icon": "arrow_forward",
    }


def test_thread_updates_renderer_renders_action_with_deleted_category_context(
    thread, user, default_category
):
    thread_update = create_moved_thread_update(thread, default_category, user)
    thread_update.clear_context_object()
    thread_update.save()

    data = thread_updates_renderer.render_thread_update(
        thread_update, {"categories": {}}
    )
    assert data == {
        "description": "Moved thread from <em>First category</em>",
        "icon": "arrow_forward",
    }


def test_thread_updates_renderer_renders_action_with_not_found_category_context(
    thread, user, default_category
):
    thread_update = create_moved_thread_update(thread, default_category, user)
    data = thread_updates_renderer.render_thread_update(
        thread_update, {"categories": {}}
    )
    assert data == {
        "description": "Moved thread from <em>First category</em>",
        "icon": "arrow_forward",
    }


def test_thread_updates_renderer_renders_action_with_user_context(
    thread, user, other_user
):
    thread_update = create_invited_thread_update(thread, other_user, user)
    data = thread_updates_renderer.render_thread_update(
        thread_update, {"users": {other_user.id: other_user}}
    )
    assert data == {
        "description": (
            f'Invited <a href="{other_user.get_absolute_url()}">Other_User</a>'
        ),
        "icon": "person_add",
    }


def test_thread_updates_renderer_renders_action_with_deleted_user_context(
    thread, user, other_user
):
    thread_update = create_invited_thread_update(thread, other_user, user)
    thread_update.clear_context_object()
    thread_update.save()

    data = thread_updates_renderer.render_thread_update(thread_update, {"users": {}})
    assert data == {"description": "Invited <em>Other_User</em>", "icon": "person_add"}


def test_thread_updates_renderer_renders_action_with_not_found_user_context(
    thread, user, other_user
):
    thread_update = create_invited_thread_update(thread, other_user, user)
    data = thread_updates_renderer.render_thread_update(thread_update, {"users": {}})
    assert data == {"description": "Invited <em>Other_User</em>", "icon": "person_add"}


def test_thread_updates_renderer_returns_none_for_unsupported_action(thread, user):
    thread_update = create_approved_thread_update(thread, user)
    thread_update.action = "invalid"
    thread_update.save()

    data = thread_updates_renderer.render_thread_update(thread_update, {})
    assert data is None
