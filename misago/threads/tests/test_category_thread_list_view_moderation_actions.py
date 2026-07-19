import pytest

from ...permissions.enums import CategoryPermission
from ...permissions.models import Moderator
from ...polls.models import Poll
from ...solutions.select import select_thread_solution
from ...test import UNORDERED, assert_contains, assert_not_contains
from ...testutils import grant_category_group_permissions
from ...threadevents.enums import ThreadEventActionName
from ...threadevents.models import ThreadEvent
from ..enums import ThreadPinned
from ..models import Thread


@pytest.fixture
def mock_synchronize_categories(mocker):
    return mocker.patch("misago.moderation.threads.synchronize_categories")


@pytest.fixture
def mock_delete_duplicate_watched_threads(mocker):
    return mocker.patch("misago.moderation.threads.delete_duplicate_watched_threads")


def test_category_thread_list_view_pin_everywhere_moderation_action_pins_unpinned_threads(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "pin_everywhere", "threads": [thread.id]},
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.EVERYWHERE
    assert thread.has_events

    ThreadEvent.objects.get(
        thread=thread,
        action=ThreadEventActionName.PINNED_EVERYWHERE,
    )


def test_category_thread_list_view_pin_everywhere_moderation_action_pins_pinned_category_threads(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category, pinned=ThreadPinned.CATEGORY)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "pin_everywhere", "threads": [thread.id]},
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.EVERYWHERE
    assert thread.has_events

    ThreadEvent.objects.get(
        thread=thread,
        action=ThreadEventActionName.PINNED_EVERYWHERE,
    )


def test_category_thread_list_view_pin_everywhere_moderation_action_validates_threads(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category, pinned=ThreadPinned.EVERYWHERE)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "pin_everywhere", "threads": [thread.id]},
    )
    assert_contains(response, "Threads are already pinned.")

    assert not ThreadEvent.objects.exists()


def test_category_thread_list_view_pin_category_moderation_action_pins_unpinned_threads(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "pin_category", "threads": [thread.id]},
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.CATEGORY
    assert thread.has_events

    ThreadEvent.objects.get(
        thread=thread,
        action=ThreadEventActionName.PINNED_CATEGORY,
    )


def test_category_thread_list_view_pin_category_moderation_action_pins_pinned_everywhere_threads(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category, pinned=ThreadPinned.EVERYWHERE)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "pin_category", "threads": [thread.id]},
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.CATEGORY
    assert thread.has_events

    ThreadEvent.objects.get(
        thread=thread,
        action=ThreadEventActionName.PINNED_CATEGORY,
    )


def test_category_thread_list_view_pin_category_moderation_action_validates_threads(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category, pinned=ThreadPinned.CATEGORY)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "pin_category", "threads": [thread.id]},
    )
    assert_contains(response, "Threads are already pinned.")

    assert not ThreadEvent.objects.exists()


def test_category_thread_list_view_unpin_moderation_action_unpins_pinned_everywhere_threads(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category, pinned=ThreadPinned.EVERYWHERE)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "unpin", "threads": [thread.id]},
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.NONE
    assert thread.has_events

    ThreadEvent.objects.get(
        thread=thread,
        action=ThreadEventActionName.UNPINNED,
    )


def test_category_thread_list_view_unpin_moderation_action_unpins_pinned_category_threads(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category, pinned=ThreadPinned.CATEGORY)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "unpin", "threads": [thread.id]},
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.NONE
    assert thread.has_events

    ThreadEvent.objects.get(
        thread=thread,
        action=ThreadEventActionName.UNPINNED,
    )


def test_category_thread_list_view_unpin_moderation_action_validates_threads(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "unpin", "threads": [thread.id]},
    )
    assert_contains(response, "Threads are already unpinned.")

    assert not ThreadEvent.objects.exists()


def test_category_thread_list_view_lock_moderation_action_locks_threads(
    thread_factory, moderator_client, moderator, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "lock", "threads": [thread.id]},
    )
    assert_contains(response, "Lock threads")
    assert_contains(response, "Reason for lock")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "lock",
            "threads": [thread.id],
            "moderation-lock_reason": "Lorem ipsum",
            "confirm": True,
        },
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()

    thread.refresh_from_db()
    assert thread.is_locked
    assert thread.locked_at
    assert thread.locked_by == moderator
    assert thread.locked_by_name == moderator.username
    assert thread.locked_by_slug == moderator.slug
    assert thread.lock_reason == "Lorem ipsum"
    assert thread.has_events

    ThreadEvent.objects.get(
        thread=thread,
        action=ThreadEventActionName.LOCKED,
    )


def test_category_thread_list_view_lock_moderation_action_validates_threads(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category, is_locked=True)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "lock", "threads": [thread.id]},
    )
    assert_contains(response, "Threads are already locked.")

    assert not ThreadEvent.objects.exists()


def test_category_thread_list_view_unlock_moderation_action_unlocks_threads(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category, is_locked=True)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "unlock", "threads": [thread.id]},
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()

    thread.refresh_from_db()
    assert not thread.is_locked
    assert thread.has_events

    ThreadEvent.objects.get(
        thread=thread,
        action=ThreadEventActionName.UNLOCKED,
    )


def test_category_thread_list_view_unlock_moderation_action_validates_threads(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "unlock", "threads": [thread.id]},
    )
    assert_contains(response, "Threads are already unlocked.")

    assert not ThreadEvent.objects.exists()


def test_category_thread_list_view_hide_moderation_action_hides_threads(
    thread_factory,
    moderator_client,
    moderator,
    default_category,
    mock_synchronize_categories,
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "hide", "threads": [thread.id]},
    )
    assert_contains(response, "Hide threads")
    assert_contains(response, "Reason for hiding")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "hide",
            "threads": [thread.id],
            "moderation-hide_reason": "Lorem ipsum",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()

    thread.refresh_from_db()
    assert thread.is_hidden
    assert thread.hidden_at
    assert thread.hidden_by == moderator
    assert thread.hidden_by_name == moderator.username
    assert thread.hidden_by_slug == moderator.slug
    assert thread.hide_reason == "Lorem ipsum"
    assert thread.has_events

    ThreadEvent.objects.get(
        thread=thread,
        action=ThreadEventActionName.HIDDEN,
    )

    mock_synchronize_categories.delay.assert_called_once_with([default_category.id])


def test_category_thread_list_view_hide_moderation_action_validates_threads(
    thread_factory, moderator_client, default_category, mock_synchronize_categories
):
    thread = thread_factory(default_category, is_hidden=True)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "hide", "threads": [thread.id]},
    )
    assert_contains(response, "Threads are already hidden.")

    assert not ThreadEvent.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()


def test_category_thread_list_view_unhide_moderation_action_unhides_threads(
    thread_factory, moderator_client, default_category, mock_synchronize_categories
):
    thread = thread_factory(default_category, is_hidden=True)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "unhide", "threads": [thread.id]},
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()

    thread.refresh_from_db()
    assert not thread.is_hidden
    assert thread.hidden_at is None
    assert thread.hidden_by is None
    assert thread.hidden_by_name is None
    assert thread.hidden_by_slug is None
    assert thread.hide_reason is None
    assert thread.has_events

    ThreadEvent.objects.get(
        thread=thread,
        action=ThreadEventActionName.UNHIDDEN,
    )

    mock_synchronize_categories.delay.assert_called_once_with([default_category.id])


def test_category_thread_list_view_unhide_moderation_action_validates_threads(
    thread_factory, moderator_client, default_category, mock_synchronize_categories
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "unhide", "threads": [thread.id]},
    )
    assert_contains(response, "Threads are already unhidden.")

    assert not ThreadEvent.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()


def test_category_thread_list_view_require_reply_approval_moderation_action_requires_threads_reply_approval(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "require_reply_approval", "threads": [thread.id]},
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()

    thread.refresh_from_db()
    assert thread.require_reply_approval
    assert thread.has_events

    ThreadEvent.objects.get(
        thread=thread,
        action=ThreadEventActionName.REQUIRED_REPLY_APPROVAL,
    )


def test_category_thread_list_view_require_reply_approval_moderation_action_validates_threads(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category, require_reply_approval=True)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "require_reply_approval", "threads": [thread.id]},
    )
    assert_contains(response, "Threads already require reply approval.")

    assert not ThreadEvent.objects.exists()


def test_category_thread_list_view_remove_reply_approval_moderation_action_removes_threads_reply_approval(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category, require_reply_approval=True)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "remove_reply_approval", "threads": [thread.id]},
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()

    thread.refresh_from_db()
    assert not thread.require_reply_approval
    assert thread.has_events

    ThreadEvent.objects.get(
        thread=thread,
        action=ThreadEventActionName.REMOVED_REPLY_APPROVAL,
    )


def test_category_thread_list_view_remove_reply_approval_moderation_action_validates_threads(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "remove_reply_approval", "threads": [thread.id]},
    )
    assert_contains(response, "Threads already don&#x27;t require reply approval.")

    assert not ThreadEvent.objects.exists()


def test_category_thread_list_view_approve_moderation_action_approves_threads(
    thread_factory, moderator_client, default_category, mock_synchronize_categories
):
    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "approve", "threads": [thread.id]},
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()

    thread.refresh_from_db()
    assert not thread.is_unapproved
    assert thread.has_events

    ThreadEvent.objects.get(
        thread=thread,
        action=ThreadEventActionName.APPROVED,
    )

    mock_synchronize_categories.delay.assert_called_once_with([default_category.id])


def test_category_thread_list_view_approve_moderation_action_validates_threads(
    thread_factory, moderator_client, default_category, mock_synchronize_categories
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "approve", "threads": [thread.id]},
    )
    assert_contains(response, "Threads are already approved.")

    assert not ThreadEvent.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()


def test_category_thread_list_view_move_moderation_action_moves_threads(
    thread_factory,
    moderator_client,
    moderators_group,
    default_category,
    sibling_category,
    mock_synchronize_categories,
):
    grant_category_group_permissions(
        sibling_category,
        moderators_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
        CategoryPermission.START,
    )

    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "move", "threads": [thread.id]},
    )
    assert_contains(response, "Move threads")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "move",
            "threads": [thread.id],
            "moderation-category": sibling_category.id,
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()

    thread.refresh_from_db()
    assert thread.category == sibling_category
    assert thread.has_events

    ThreadEvent.objects.get(
        thread=thread,
        action=ThreadEventActionName.MOVED,
    )

    mock_synchronize_categories.delay.assert_called_once_with(
        UNORDERED([default_category.id, sibling_category.id])
    )


def test_category_thread_list_view_move_moderation_action_validates_other_category_choices_exist(
    thread_factory,
    moderator_client,
    default_category,
    mock_synchronize_categories,
):
    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "move", "threads": [thread.id]},
    )
    assert_contains(response, "There are no other categories you can move threads to.")

    thread.refresh_from_db()
    assert thread.category == default_category
    assert not thread.has_events

    assert not ThreadEvent.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()


def test_category_thread_list_view_move_moderation_action_requires_category(
    thread_factory,
    moderator_client,
    moderators_group,
    default_category,
    sibling_category,
    mock_synchronize_categories,
):
    grant_category_group_permissions(
        sibling_category,
        moderators_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
        CategoryPermission.START,
    )

    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "move", "threads": [thread.id]},
    )
    assert_contains(response, "Move threads")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "move",
            "threads": [thread.id],
            "confirm": "true",
        },
    )
    assert_contains(response, "This field is required.")

    thread.refresh_from_db()
    assert thread.category == default_category
    assert not thread.has_events

    assert not ThreadEvent.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()


def test_category_thread_list_view_move_moderation_action_validates_category_value(
    thread_factory,
    moderator_client,
    moderators_group,
    default_category,
    sibling_category,
    mock_synchronize_categories,
):
    grant_category_group_permissions(
        sibling_category,
        moderators_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
        CategoryPermission.START,
    )

    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "move", "threads": [thread.id]},
    )
    assert_contains(response, "Move threads")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "move",
            "threads": [thread.id],
            "moderation-category": "invalid",
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    thread.refresh_from_db()
    assert thread.category == default_category
    assert not thread.has_events

    assert not ThreadEvent.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()


def test_category_thread_list_view_move_moderation_action_validates_category_browse_permission(
    thread_factory,
    moderator_client,
    moderators_group,
    default_category,
    sibling_category,
    other_category,
    mock_synchronize_categories,
):
    grant_category_group_permissions(
        sibling_category,
        moderators_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )
    grant_category_group_permissions(
        other_category,
        moderators_group,
        CategoryPermission.SEE,
    )

    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "move", "threads": [thread.id]},
    )
    assert_contains(response, "Move threads")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "move",
            "threads": [thread.id],
            "moderation-category": other_category.id,
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    thread.refresh_from_db()
    assert thread.category == default_category
    assert not thread.has_events

    assert not ThreadEvent.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()


def test_category_thread_list_view_move_moderation_action_validates_category_moderator_permission(
    thread_factory,
    user_client,
    members_group,
    user,
    default_category,
    sibling_category,
    other_category,
    mock_synchronize_categories,
):
    grant_category_group_permissions(
        sibling_category,
        members_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )
    grant_category_group_permissions(
        other_category,
        members_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id, sibling_category.id],
    )

    thread = thread_factory(default_category, is_unapproved=True)

    response = user_client.post(
        default_category.get_absolute_url(),
        {"moderation": "move", "threads": [thread.id]},
    )
    assert_contains(response, "Move threads")

    response = user_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "move",
            "threads": [thread.id],
            "moderation-category": other_category.id,
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    thread.refresh_from_db()
    assert thread.category == default_category
    assert not thread.has_events

    assert not ThreadEvent.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()


def test_category_thread_list_view_move_moderation_action_validates_category_type(
    thread_factory,
    moderator_client,
    moderators_group,
    default_category,
    sibling_category,
    other_category,
    mock_synchronize_categories,
):
    grant_category_group_permissions(
        sibling_category,
        moderators_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
        CategoryPermission.START,
    )
    grant_category_group_permissions(
        other_category,
        moderators_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
        CategoryPermission.START,
    )

    other_category.is_vanilla = True
    other_category.save()

    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "move", "threads": [thread.id]},
    )
    assert_contains(response, "Move threads")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "move",
            "threads": [thread.id],
            "moderation-category": other_category.id,
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    thread.refresh_from_db()
    assert thread.category == default_category
    assert not thread.has_events

    assert not ThreadEvent.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()


def test_category_thread_list_view_move_moderation_action_validates_category_is_new(
    thread_factory,
    moderator_client,
    moderators_group,
    default_category,
    sibling_category,
    mock_synchronize_categories,
):
    grant_category_group_permissions(
        sibling_category,
        moderators_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
        CategoryPermission.START,
    )

    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "move", "threads": [thread.id]},
    )
    assert_contains(response, "Move threads")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "move",
            "threads": [thread.id],
            "moderation-category": default_category.id,
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    thread.refresh_from_db()
    assert thread.category == default_category
    assert not thread.has_events

    assert not ThreadEvent.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()


def test_category_thread_list_view_merge_moderation_action_merges_threads(
    moderator_client,
    default_category,
    thread,
    other_thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "merge", "threads": [thread.id, other_thread.id]},
    )
    assert_contains(response, "Merge threads")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "merge",
            "threads": [thread.id, other_thread.id],
            "moderation-category": default_category.id,
            "moderation-title": "Merged thread",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()

    with pytest.raises(Thread.DoesNotExist):
        other_thread.refresh_from_db()

    merged_thread = Thread.objects.get(slug="merged-thread")
    assert merged_thread.replies == 1

    assert (
        ThreadEvent.objects.filter(
            thread=merged_thread,
            action=ThreadEventActionName.MERGED,
        ).count()
        == 2
    )

    mock_synchronize_categories.delay.assert_called_once_with([default_category.id])
    mock_delete_duplicate_watched_threads.delay.assert_called_once_with(
        merged_thread.id
    )


def test_category_thread_list_view_merge_moderation_action_merges_threads_without_conflicts(
    thread_reply_factory,
    poll_factory,
    moderator_client,
    default_category,
    thread,
    other_thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    solution = thread_reply_factory(thread, poster="Answer")
    select_thread_solution(thread, solution, user="JohnDoe")

    poll = poll_factory(other_thread)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "merge", "threads": [thread.id, other_thread.id]},
    )
    assert_contains(response, "Merge threads")
    assert_not_contains(response, "Solution")
    assert_not_contains(response, "Poll")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "merge",
            "threads": [thread.id, other_thread.id],
            "moderation-category": default_category.id,
            "moderation-title": "Merged thread",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()

    with pytest.raises(Thread.DoesNotExist):
        other_thread.refresh_from_db()

    merged_thread = Thread.objects.get(slug="merged-thread")
    assert merged_thread.replies == 2
    assert merged_thread.solution == solution

    poll.refresh_from_db()
    assert poll.thread == merged_thread

    assert (
        ThreadEvent.objects.filter(
            thread=merged_thread,
            action=ThreadEventActionName.MERGED,
        ).count()
        == 2
    )

    mock_synchronize_categories.delay.assert_called_once_with([default_category.id])
    mock_delete_duplicate_watched_threads.delay.assert_called_once_with(
        merged_thread.id
    )


def test_category_thread_list_view_merge_moderation_action_merges_threads_with_conflicts(
    thread_reply_factory,
    poll_factory,
    moderator_client,
    default_category,
    thread,
    other_thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    thread_solution = thread_reply_factory(thread, poster="Answer")
    other_thread_solution = thread_reply_factory(other_thread, poster="Answer")

    select_thread_solution(thread, thread_solution, user="JohnDoe")
    select_thread_solution(other_thread, other_thread_solution, user="JohnDoe")

    thread_poll = poll_factory(thread)
    other_thread_poll = poll_factory(other_thread)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "merge", "threads": [thread.id, other_thread.id]},
    )
    assert_contains(response, "Merge threads")
    assert_contains(response, "Solution")
    assert_contains(response, "Poll")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "merge",
            "threads": [thread.id, other_thread.id],
            "moderation-category": default_category.id,
            "moderation-title": "Merged thread",
            "moderation-solution": thread.id,
            "moderation-poll": other_thread_poll.id,
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()

    with pytest.raises(Thread.DoesNotExist):
        other_thread.refresh_from_db()

    merged_thread = Thread.objects.get(slug="merged-thread")
    assert merged_thread.replies == 3
    assert merged_thread.solution == thread_solution

    other_thread_poll.refresh_from_db()
    assert other_thread_poll.thread == merged_thread

    with pytest.raises(Poll.DoesNotExist):
        thread_poll.refresh_from_db()

    assert (
        ThreadEvent.objects.filter(
            thread=merged_thread,
            action=ThreadEventActionName.MERGED,
        ).count()
        == 2
    )

    mock_synchronize_categories.delay.assert_called_once_with([default_category.id])
    mock_delete_duplicate_watched_threads.delay.assert_called_once_with(
        merged_thread.id
    )


def test_category_thread_list_view_merge_moderation_action_merges_threads_with_moderation_options(
    moderator_client,
    default_category,
    thread,
    other_thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "merge", "threads": [thread.id, other_thread.id]},
    )
    assert_contains(response, "Merge threads")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "merge",
            "threads": [thread.id, other_thread.id],
            "moderation-category": default_category.id,
            "moderation-title": "Merged thread",
            "moderation-pin": ThreadPinned.EVERYWHERE,
            "moderation-is_hidden": "1",
            "moderation-is_locked": "1",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()

    with pytest.raises(Thread.DoesNotExist):
        other_thread.refresh_from_db()

    merged_thread = Thread.objects.get(slug="merged-thread")
    assert merged_thread.replies == 1
    assert merged_thread.pinned == ThreadPinned.EVERYWHERE
    assert merged_thread.is_hidden
    assert merged_thread.is_locked

    assert (
        ThreadEvent.objects.filter(
            thread=merged_thread,
            action=ThreadEventActionName.MERGED,
        ).count()
        == 2
    )

    mock_synchronize_categories.delay.assert_called_once_with([default_category.id])
    mock_delete_duplicate_watched_threads.delay.assert_called_once_with(
        merged_thread.id
    )


def test_category_thread_list_view_merge_moderation_action_validates_multiple_threads_are_selected(
    moderator_client,
    default_category,
    thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "merge", "threads": [thread.id]},
    )
    assert_contains(response, "Merge threads")
    assert_contains(response, "Select at least two threads to merge.")

    thread.refresh_from_db()

    assert not ThreadEvent.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_category_thread_list_view_merge_moderation_action_validates_category_value(
    moderator_client,
    default_category,
    thread,
    other_thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "merge", "threads": [thread.id, other_thread.id]},
    )
    assert_contains(response, "Merge threads")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "merge",
            "threads": [thread.id, other_thread.id],
            "moderation-category": "invalid",
            "moderation-title": "Merged thread",
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    thread.refresh_from_db()
    other_thread.refresh_from_db()

    assert not ThreadEvent.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_category_thread_list_view_merge_moderation_action_validates_category_browse_permission(
    moderator_client,
    moderators_group,
    default_category,
    sibling_category,
    thread,
    other_thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    grant_category_group_permissions(
        sibling_category,
        moderators_group,
        CategoryPermission.SEE,
    )

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "merge", "threads": [thread.id, other_thread.id]},
    )
    assert_contains(response, "Merge threads")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "merge",
            "threads": [thread.id, other_thread.id],
            "moderation-category": sibling_category.id,
            "moderation-title": "Merged thread",
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    thread.refresh_from_db()
    other_thread.refresh_from_db()

    assert not ThreadEvent.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_category_thread_list_view_merge_moderation_action_validates_category_moderator_permission(
    user_client,
    members_group,
    user,
    default_category,
    sibling_category,
    thread,
    other_thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    grant_category_group_permissions(
        sibling_category,
        members_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    response = user_client.post(
        default_category.get_absolute_url(),
        {"moderation": "merge", "threads": [thread.id, other_thread.id]},
    )
    assert_contains(response, "Merge threads")

    response = user_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "merge",
            "threads": [thread.id, other_thread.id],
            "moderation-category": sibling_category.id,
            "moderation-title": "Merged thread",
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    thread.refresh_from_db()
    other_thread.refresh_from_db()

    assert not ThreadEvent.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_category_thread_list_view_merge_moderation_action_validates_category_type(
    moderator_client,
    moderators_group,
    default_category,
    sibling_category,
    thread,
    other_thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    grant_category_group_permissions(
        sibling_category,
        moderators_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    sibling_category.is_vanilla = True
    sibling_category.save()

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "merge", "threads": [thread.id, other_thread.id]},
    )
    assert_contains(response, "Merge threads")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "merge",
            "threads": [thread.id, other_thread.id],
            "moderation-category": sibling_category.id,
            "moderation-title": "Merged thread",
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    thread.refresh_from_db()
    other_thread.refresh_from_db()

    assert not ThreadEvent.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_category_thread_list_view_merge_moderation_action_requires_thread_title(
    moderator_client,
    default_category,
    thread,
    other_thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "merge", "threads": [thread.id, other_thread.id]},
    )
    assert_contains(response, "Merge threads")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "merge",
            "threads": [thread.id, other_thread.id],
            "moderation-category": default_category.id,
            "confirm": "true",
        },
    )
    assert_contains(response, "This field is required.")

    thread.refresh_from_db()
    other_thread.refresh_from_db()

    assert not ThreadEvent.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_category_thread_list_view_merge_moderation_action_validates_thread_title(
    moderator_client,
    default_category,
    thread,
    other_thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "merge", "threads": [thread.id, other_thread.id]},
    )
    assert_contains(response, "Merge threads")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "merge",
            "threads": [thread.id, other_thread.id],
            "moderation-category": default_category.id,
            "moderation-title": "Q",
            "confirm": "true",
        },
    )
    assert_contains(response, "Thread title should be at least 5 characters long")

    thread.refresh_from_db()
    other_thread.refresh_from_db()

    assert not ThreadEvent.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_category_thread_list_view_merge_moderation_action_requires_conflict_resolution(
    thread_reply_factory,
    moderator_client,
    default_category,
    thread,
    other_thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    thread_solution = thread_reply_factory(thread, poster="Answer")
    other_thread_solution = thread_reply_factory(other_thread, poster="Answer")

    select_thread_solution(thread, thread_solution, user="JohnDoe")
    select_thread_solution(other_thread, other_thread_solution, user="JohnDoe")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "merge", "threads": [thread.id, other_thread.id]},
    )
    assert_contains(response, "Merge threads")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "merge",
            "threads": [thread.id, other_thread.id],
            "moderation-category": default_category.id,
            "moderation-title": "Merged thread",
            "confirm": "true",
        },
    )
    assert_contains(response, "This field is required.")

    thread.refresh_from_db()
    other_thread.refresh_from_db()

    assert not ThreadEvent.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_category_thread_list_view_merge_moderation_action_validates_conflict_resolution(
    thread_reply_factory,
    moderator_client,
    default_category,
    thread,
    other_thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    thread_solution = thread_reply_factory(thread, poster="Answer")
    other_thread_solution = thread_reply_factory(other_thread, poster="Answer")

    select_thread_solution(thread, thread_solution, user="JohnDoe")
    select_thread_solution(other_thread, other_thread_solution, user="JohnDoe")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "merge", "threads": [thread.id, other_thread.id]},
    )
    assert_contains(response, "Merge threads")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "merge",
            "threads": [thread.id, other_thread.id],
            "moderation-category": default_category.id,
            "moderation-title": "Merged thread",
            "moderation-solution": max(thread.id, other_thread.id) + 1,
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    thread.refresh_from_db()
    other_thread.refresh_from_db()

    assert not ThreadEvent.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_category_thread_list_view_delete_moderation_action_deletes_threads(
    thread_factory, moderator_client, default_category, mock_synchronize_categories
):
    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "delete", "threads": [thread.id]},
    )
    assert_contains(response, "Delete threads")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "delete",
            "threads": [thread.id],
            "confirm": "true",
        },
    )

    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()

    mock_synchronize_categories.delay.assert_called_once_with([default_category.id])
