from django.urls import reverse

from ...threadupdates.enums import ThreadUpdateActionName
from ...threadupdates.models import ThreadUpdate


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
