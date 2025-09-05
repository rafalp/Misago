from ...threads.threadurl import get_thread_url
from ..create import (
    create_added_member_thread_update,
    create_approved_thread_update,
    create_changed_title_thread_update,
    create_moved_thread_update,
    create_split_thread_update,
)
from ..renderer import thread_updates_renderer


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


def test_thread_updates_renderer_renders_action_with_thread_context(
    thread, user, default_category, other_thread
):
    thread_update = create_split_thread_update(thread, other_thread, user)
    data = thread_updates_renderer.render_thread_update(
        thread_update,
        {
            "categories": {default_category.id: default_category},
            "threads": {other_thread.id: other_thread},
        },
    )
    thread_url = get_thread_url(other_thread, default_category)
    assert data == {
        "description": f'Split this thread from <a href="{thread_url}">{other_thread.title}</a>',
        "icon": "call_split",
    }


def test_thread_updates_renderer_renders_action_with_not_found_thread_category(
    thread, user, other_thread
):
    thread_update = create_split_thread_update(thread, other_thread, user)
    data = thread_updates_renderer.render_thread_update(
        thread_update, {"categories": {}, "threads": {other_thread.id: other_thread}}
    )
    assert data == {
        "description": f"Split this thread from <em>{other_thread.title}</em>",
        "icon": "call_split",
    }


def test_thread_updates_renderer_renders_action_with_deleted_thread_context(
    thread, user, other_thread
):
    thread_update = create_split_thread_update(thread, other_thread, user)
    thread_update.clear_context_object()
    thread_update.save()

    data = thread_updates_renderer.render_thread_update(thread_update, {"threads": {}})
    assert data == {
        "description": f"Split this thread from <em>{other_thread.title}</em>",
        "icon": "call_split",
    }


def test_thread_updates_renderer_renders_action_with_not_found_thread_context(
    thread, user, other_thread
):
    thread_update = create_split_thread_update(thread, other_thread, user)
    data = thread_updates_renderer.render_thread_update(thread_update, {"threads": {}})
    assert data == {
        "description": f"Split this thread from <em>{other_thread.title}</em>",
        "icon": "call_split",
    }


def test_thread_updates_renderer_renders_action_with_user_context(
    thread, user, other_user
):
    thread_update = create_added_member_thread_update(thread, other_user, user)
    data = thread_updates_renderer.render_thread_update(
        thread_update, {"users": {other_user.id: other_user}}
    )
    assert data == {
        "description": (
            f'Added <a href="{other_user.get_absolute_url()}">Other_User</a>'
        ),
        "icon": "person_add",
    }


def test_thread_updates_renderer_renders_action_with_deleted_user_context(
    thread, user, other_user
):
    thread_update = create_added_member_thread_update(thread, other_user, user)
    thread_update.clear_context_object()
    thread_update.save()

    data = thread_updates_renderer.render_thread_update(thread_update, {"users": {}})
    assert data == {"description": "Added <em>Other_User</em>", "icon": "person_add"}


def test_thread_updates_renderer_renders_action_with_not_found_user_context(
    thread, user, other_user
):
    thread_update = create_added_member_thread_update(thread, other_user, user)
    data = thread_updates_renderer.render_thread_update(thread_update, {"users": {}})
    assert data == {"description": "Added <em>Other_User</em>", "icon": "person_add"}


def test_thread_updates_renderer_returns_none_for_unsupported_action(thread, user):
    thread_update = create_approved_thread_update(thread, user)
    thread_update.action = "invalid"
    thread_update.save()

    data = thread_updates_renderer.render_thread_update(thread_update, {})
    assert data is None
