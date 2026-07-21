from ...threads.threadurl import get_thread_url
from ..create import (
    create_added_member_thread_event,
    create_approved_thread_event,
    create_changed_title_thread_event,
    create_moved_thread_event,
    create_split_posts_from_thread_event,
)
from ..renderer import thread_events_renderer


def test_thread_events_renderer_renders_simple_action(thread, user):
    thread_event = create_approved_thread_event(thread, user)
    data = thread_events_renderer.render_thread_event(thread_event, {})
    assert data == {"description": "Approved", "icon": "tabler/checkbox.svg"}


def test_thread_events_renderer_renders_action_with_text_context(thread, user):
    thread_event = create_changed_title_thread_event(thread, "Old title", user)
    data = thread_events_renderer.render_thread_event(thread_event, {})
    assert data == {
        "description": "Changed title from <em>Old title</em>",
        "icon": "tabler/pencil.svg",
    }


def test_thread_events_renderer_renders_action_with_category_context(
    thread, user, default_category
):
    thread_event = create_moved_thread_event(thread, default_category, user)
    data = thread_events_renderer.render_thread_event(
        thread_event, {"categories": {default_category.id: default_category}}
    )
    assert data == {
        "description": (
            f'Moved from <a href="{default_category.get_absolute_url()}">First category</a>'
        ),
        "icon": "tabler/arrow-right.svg",
    }


def test_thread_events_renderer_renders_action_with_deleted_category_context(
    thread, user, default_category
):
    thread_event = create_moved_thread_event(thread, default_category, user)
    thread_event.clear_context_object()
    thread_event.save()

    data = thread_events_renderer.render_thread_event(thread_event, {"categories": {}})
    assert data == {
        "description": "Moved from <em>First category</em>",
        "icon": "tabler/arrow-right.svg",
    }


def test_thread_events_renderer_renders_action_with_not_found_category_context(
    thread, user, default_category
):
    thread_event = create_moved_thread_event(thread, default_category, user)
    data = thread_events_renderer.render_thread_event(thread_event, {"categories": {}})
    assert data == {
        "description": "Moved from <em>First category</em>",
        "icon": "tabler/arrow-right.svg",
    }


def test_thread_events_renderer_renders_action_with_thread_context(
    thread, user, default_category, other_thread
):
    thread_event = create_split_posts_from_thread_event(
        thread, other_thread, actor=user
    )
    data = thread_events_renderer.render_thread_event(
        thread_event,
        {
            "categories": {default_category.id: default_category},
            "threads": {other_thread.id: other_thread},
        },
    )
    thread_url = get_thread_url(other_thread, default_category)
    assert data == {
        "description": f'Split from <a href="{thread_url}">{other_thread.title}</a>',
        "icon": "tabler/arrows-split-2.svg",
    }


def test_thread_events_renderer_renders_action_with_not_found_thread_category(
    thread, user, other_thread
):
    thread_event = create_split_posts_from_thread_event(
        thread, other_thread, actor=user
    )
    data = thread_events_renderer.render_thread_event(
        thread_event, {"categories": {}, "threads": {other_thread.id: other_thread}}
    )
    assert data == {
        "description": f"Split from <em>{other_thread.title}</em>",
        "icon": "tabler/arrows-split-2.svg",
    }


def test_thread_events_renderer_renders_action_with_deleted_thread_context(
    thread, user, other_thread
):
    thread_event = create_split_posts_from_thread_event(
        thread, other_thread, actor=user
    )
    thread_event.clear_context_object()
    thread_event.save()

    data = thread_events_renderer.render_thread_event(thread_event, {"threads": {}})
    assert data == {
        "description": f"Split from <em>{other_thread.title}</em>",
        "icon": "tabler/arrows-split-2.svg",
    }


def test_thread_events_renderer_renders_action_with_not_found_thread_context(
    thread, user, other_thread
):
    thread_event = create_split_posts_from_thread_event(
        thread, other_thread, actor=user
    )
    data = thread_events_renderer.render_thread_event(thread_event, {"threads": {}})
    assert data == {
        "description": f"Split from <em>{other_thread.title}</em>",
        "icon": "tabler/arrows-split-2.svg",
    }


def test_thread_events_renderer_renders_action_with_user_context(
    thread, user, other_user
):
    thread_event = create_added_member_thread_event(thread, other_user, user)
    data = thread_events_renderer.render_thread_event(
        thread_event, {"users": {other_user.id: other_user}}
    )
    assert data == {
        "description": (
            f'Added <a href="{other_user.get_absolute_url()}">Other_User</a>'
        ),
        "icon": "tabler/user.svg",
    }


def test_thread_events_renderer_renders_action_with_deleted_user_context(
    thread, user, other_user
):
    thread_event = create_added_member_thread_event(thread, other_user, user)
    thread_event.clear_context_object()
    thread_event.save()

    data = thread_events_renderer.render_thread_event(thread_event, {"users": {}})
    assert data == {
        "description": "Added <em>Other_User</em>",
        "icon": "tabler/user.svg",
    }


def test_thread_events_renderer_renders_action_with_not_found_user_context(
    thread, user, other_user
):
    thread_event = create_added_member_thread_event(thread, other_user, user)
    data = thread_events_renderer.render_thread_event(thread_event, {"users": {}})
    assert data == {
        "description": "Added <em>Other_User</em>",
        "icon": "tabler/user.svg",
    }


def test_thread_events_renderer_returns_none_for_unsupported_action(thread, user):
    thread_event = create_approved_thread_event(thread, user)
    thread_event.action = "invalid"
    thread_event.save()

    data = thread_events_renderer.render_thread_event(thread_event, {})
    assert data is None
