from django.urls import reverse

from ...threadupdates.enums import ThreadUpdateActionName
from ...threadupdates.models import ThreadUpdate
from ..enums import ThreadPinned


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
