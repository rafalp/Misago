import pytest
from django.urls import reverse

from ...test import assert_contains
from ...threadupdates.enums import ThreadUpdateActionName
from ...threadupdates.models import ThreadUpdate


@pytest.fixture
def mock_synchronize_categories(mocker):
    return mocker.patch("misago.moderation.thread.synchronize_categories")


def test_private_thread_detail_view_executes_lock_thread_moderation_action(
    moderator_client, user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "lock"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )

    user_private_thread.refresh_from_db()
    assert user_private_thread.is_locked
    assert user_private_thread.has_updates

    ThreadUpdate.objects.get(
        thread=user_private_thread,
        action=ThreadUpdateActionName.LOCKED,
    )


def test_private_thread_detail_view_executes_unlock_thread_moderation_action(
    moderator_client, user_private_thread
):
    user_private_thread.is_locked = True
    user_private_thread.save()

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "unlock"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )

    user_private_thread.refresh_from_db()
    assert not user_private_thread.is_locked
    assert user_private_thread.has_updates

    ThreadUpdate.objects.get(
        thread=user_private_thread,
        action=ThreadUpdateActionName.UNLOCKED,
    )


def test_private_thread_detail_view_executes_hide_thread_moderation_action(
    moderator_client, moderator, user_private_thread, mock_synchronize_categories
):
    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "hide"},
    )
    assert_contains(response, "Reason for hiding")
    assert_contains(response, "Hide thread")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "thread_moderation": "hide",
            "moderation-hidden_reason": "Lorem ipsum",
            "confirm": True,
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"thread_id": user_private_thread.id, "slug": user_private_thread.slug},
    )

    user_private_thread.refresh_from_db()
    assert user_private_thread.is_hidden
    assert user_private_thread.hidden_at
    assert user_private_thread.hidden_by == moderator
    assert user_private_thread.hidden_by_name == moderator.username
    assert user_private_thread.hidden_by_slug == moderator.slug
    assert user_private_thread.hidden_reason == "Lorem ipsum"
    assert user_private_thread.has_updates

    ThreadUpdate.objects.get(
        thread=user_private_thread,
        action=ThreadUpdateActionName.HIDDEN,
    )

    mock_synchronize_categories.delay.assert_called_once_with(
        [user_private_thread.category_id]
    )


def test_private_thread_detail_view_executes_unhide_thread_moderation_action(
    moderator_client, user_private_thread, mock_synchronize_categories
):
    user_private_thread.is_hidden = True
    user_private_thread.save()

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "unhide"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"thread_id": user_private_thread.id, "slug": user_private_thread.slug},
    )

    user_private_thread.refresh_from_db()
    assert not user_private_thread.is_hidden
    assert user_private_thread.hidden_at is None
    assert user_private_thread.hidden_by is None
    assert user_private_thread.hidden_by_name is None
    assert user_private_thread.hidden_by_slug is None
    assert user_private_thread.hidden_reason is None
    assert user_private_thread.has_updates

    ThreadUpdate.objects.get(
        thread=user_private_thread,
        action=ThreadUpdateActionName.UNHIDDEN,
    )

    mock_synchronize_categories.delay.assert_called_once_with(
        [user_private_thread.category_id]
    )
