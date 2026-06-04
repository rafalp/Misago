import pytest
from django.urls import reverse

from ...test import assert_contains
from ...threadupdates.enums import ThreadUpdateActionName
from ...threadupdates.models import ThreadUpdate
from ..enums import ThreadPinned


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
            "confirm": True,
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
