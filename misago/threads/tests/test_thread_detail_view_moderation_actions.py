import pytest
from django.urls import reverse

from ...permissions.enums import CategoryPermission
from ...test import SAME_ITEMS, assert_contains
from ...testutils import grant_category_group_permissions
from ...threadupdates.enums import ThreadUpdateActionName
from ...threadupdates.models import ThreadUpdate
from ..enums import ThreadPinned
from ..models import Thread


@pytest.fixture
def mock_synchronize_categories(mocker):
    return mocker.patch("misago.moderation.thread.synchronize_categories")


def test_thread_detail_view_executes_pin_everywhere_thread_moderation_action(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "pin_everywhere"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.EVERYWHERE
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.PINNED_EVERYWHERE,
    )


def test_thread_detail_view_executes_pin_category_thread_moderation_action(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "pin_category"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.CATEGORY
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.PINNED_CATEGORY,
    )


def test_thread_detail_view_executes_unpin_pinned_everywhere_thread_moderation_action(
    moderator_client, thread
):
    thread.pinned = ThreadPinned.EVERYWHERE
    thread.save()

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "unpin"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.NONE
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.UNPINNED,
    )


def test_thread_detail_view_executes_unpin_pinned_category_thread_moderation_action(
    moderator_client, thread
):
    thread.pinned = ThreadPinned.CATEGORY
    thread.save()

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "unpin"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.NONE
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.UNPINNED,
    )


def test_thread_detail_view_executes_lock_thread_moderation_action(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "lock"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.is_locked
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.LOCKED,
    )


def test_thread_detail_view_executes_unlock_thread_moderation_action(
    moderator_client, thread
):
    thread.is_locked = True
    thread.save()

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "unlock"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert not thread.is_locked
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.UNLOCKED,
    )


def test_thread_detail_view_executes_hide_thread_moderation_action(
    moderator_client, moderator, thread, mock_synchronize_categories
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "hide"},
    )
    assert_contains(response, "Reason for hiding")
    assert_contains(response, "Hide thread")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "hide",
            "moderation-hidden_reason": "Lorem ipsum",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.is_hidden
    assert thread.hidden_at
    assert thread.hidden_by == moderator
    assert thread.hidden_by_name == moderator.username
    assert thread.hidden_by_slug == moderator.slug
    assert thread.hidden_reason == "Lorem ipsum"
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.HIDDEN,
    )

    mock_synchronize_categories.delay.assert_called_once_with([thread.category_id])


def test_thread_detail_view_executes_unhide_thread_moderation_action(
    moderator_client, thread, mock_synchronize_categories
):
    thread.is_hidden = True
    thread.save()

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "unhide"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert not thread.is_hidden
    assert thread.hidden_at is None
    assert thread.hidden_by is None
    assert thread.hidden_by_name is None
    assert thread.hidden_by_slug is None
    assert thread.hidden_reason is None
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.UNHIDDEN,
    )

    mock_synchronize_categories.delay.assert_called_once_with([thread.category_id])


def test_thread_detail_view_executes_approve_thread_moderation_action(
    moderator_client, thread, mock_synchronize_categories
):
    thread.is_unapproved = True
    thread.save()

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "approve"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert not thread.is_unapproved
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.APPROVED,
    )

    mock_synchronize_categories.delay.assert_called_once_with([thread.category_id])


def test_thread_detail_view_executes_require_reply_approval_thread_moderation_action(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "require_reply_approval"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.require_reply_approval
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.REQUIRED_REPLY_APPROVAL,
    )


def test_thread_detail_view_executes_remove_reply_approval_thread_moderation_action(
    moderator_client, thread
):
    thread.require_reply_approval = True
    thread.save()

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "remove_reply_approval"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert not thread.require_reply_approval
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.REMOVED_REPLY_APPROVAL,
    )


def test_thread_detail_view_executes_move_thread_moderation_action(
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
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "move", "thread": thread.id},
    )
    assert_contains(response, "Move thread")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "move",
            "thread": thread.id,
            "moderation-category": sibling_category.id,
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.category == sibling_category
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.MOVED,
    )

    mock_synchronize_categories.delay.assert_called_once_with(
        SAME_ITEMS([default_category.id, sibling_category.id])
    )


def test_thread_detail_view_move_moderation_action_requires_category(
    thread_factory, moderator_client, default_category, mock_synchronize_categories
):
    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "move", "thread": thread.id},
    )
    assert_contains(response, "Move thread")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "move",
            "thread": thread.id,
            "confirm": "true",
        },
    )
    assert_contains(response, "This field is required.")

    thread.refresh_from_db()
    assert thread.category == default_category
    assert not thread.has_updates

    assert not ThreadUpdate.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_move_moderation_action_validates_category_value(
    thread_factory, moderator_client, default_category, mock_synchronize_categories
):
    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "move", "thread": thread.id},
    )
    assert_contains(response, "Move thread")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "move",
            "thread": thread.id,
            "moderation-category": "invalid",
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    thread.refresh_from_db()
    assert thread.category == default_category
    assert not thread.has_updates

    assert not ThreadUpdate.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_move_moderation_action_validates_category_permission(
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
    )

    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "move", "thread": thread.id},
    )
    assert_contains(response, "Move thread")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "move",
            "thread": thread.id,
            "moderation-category": sibling_category.id,
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    thread.refresh_from_db()
    assert thread.category == default_category
    assert not thread.has_updates

    assert not ThreadUpdate.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_move_moderation_action_validates_category_type(
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

    sibling_category.is_vanilla = True
    sibling_category.save()

    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "move", "thread": thread.id},
    )
    assert_contains(response, "Move thread")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "move",
            "thread": thread.id,
            "moderation-category": sibling_category.id,
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    thread.refresh_from_db()
    assert thread.category == default_category
    assert not thread.has_updates

    assert not ThreadUpdate.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_move_moderation_action_validates_category_is_new(
    thread_factory, moderator_client, default_category, mock_synchronize_categories
):
    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "move", "thread": thread.id},
    )
    assert_contains(response, "Move thread")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "move",
            "thread": thread.id,
            "moderation-category": default_category.id,
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    thread.refresh_from_db()
    assert thread.category == default_category
    assert not thread.has_updates

    assert not ThreadUpdate.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_executes_delete_thread_moderation_action(
    moderator_client, default_category, thread, mock_synchronize_categories
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "delete", "thread": thread.id},
    )
    assert_contains(response, "Delete thread")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "delete",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:category-thread-list",
        kwargs={"category_id": default_category.id, "slug": default_category.slug},
    )

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()

    mock_synchronize_categories.delay.assert_called_once_with([default_category.id])
