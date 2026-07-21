import pytest
from django.urls import reverse

from ...permissions.models import Moderator
from ...test import assert_contains
from ...threadevents.models import ThreadEvent


def test_private_thread_event_delete_view_returns_404_error_for_not_found_thread(
    user_client,
):
    response = user_client.post(
        reverse(
            "misago:private-thread-event-delete",
            kwargs={
                "thread_id": 100,
                "slug": "not-found",
                "thread_event_id": 100,
            },
        )
    )

    assert response.status_code == 404


def test_private_thread_event_delete_view_returns_404_error_for_not_found_event(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-event-delete",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_event_id": 100,
            },
        )
    )

    assert response.status_code == 404


def test_private_thread_event_delete_view_returns_403_error_for_anonymous_user(
    client, user_private_thread, user_private_thread_event
):
    response = client.post(
        reverse(
            "misago:private-thread-event-delete",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_event_id": user_private_thread_event.id,
            },
        )
    )

    assert_contains(
        response, "Only a moderator can delete thread events.", status_code=403
    )


def test_private_thread_event_delete_view_returns_403_error_for_user(
    user_client, user_private_thread, user_private_thread_event
):
    response = user_client.post(
        reverse(
            "misago:private-thread-event-delete",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_event_id": user_private_thread_event.id,
            },
        )
    )

    assert_contains(
        response, "Only a moderator can delete thread events.", status_code=403
    )


def test_private_thread_event_delete_view_checks_private_threads_permission(
    user_client, members_group, user_private_thread, user_private_thread_event
):
    members_group.can_use_private_threads = False
    members_group.save()

    response = user_client.post(
        reverse(
            "misago:private-thread-event-delete",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_event_id": user_private_thread_event.id,
            },
        )
    )

    assert_contains(response, "You can&#x27;t use private threads.", status_code=403)


def test_private_thread_event_delete_view_checks_thread_permission(
    user_client, private_thread, private_thread_event
):
    response = user_client.post(
        reverse(
            "misago:private-thread-event-delete",
            kwargs={
                "thread_id": private_thread.id,
                "slug": private_thread.slug,
                "thread_event_id": private_thread_event.id,
            },
        )
    )

    assert response.status_code == 404


def test_private_thread_event_delete_view_checks_thread_event_permission(
    user_client, user_private_thread, hidden_user_private_thread_event
):
    response = user_client.post(
        reverse(
            "misago:private-thread-event-delete",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_event_id": hidden_user_private_thread_event.id,
            },
        )
    )

    assert response.status_code == 404


def test_private_thread_event_delete_view_shows_confirm_delete_form_for_private_threads_moderator(
    user_client, user, user_private_thread, user_private_thread_event
):
    Moderator.objects.create(
        private_threads=True,
        user=user,
        is_global=False,
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-event-delete",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_event_id": user_private_thread_event.id,
            },
        ),
    )

    assert_contains(response, "Are you sure you want to delete this thread event?")


def test_private_thread_event_delete_view_deletes_event_for_private_threads_moderator(
    user_client, user, user_private_thread, user_private_thread_event
):
    Moderator.objects.create(
        private_threads=True,
        user=user,
        is_global=False,
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-event-delete",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_event_id": user_private_thread_event.id,
            },
        ),
        {"confirm": "true"},
    )

    assert response.status_code == 302

    with pytest.raises(ThreadEvent.DoesNotExist):
        user_private_thread_event.refresh_from_db()


def test_private_thread_event_delete_view_shows_confirm_delete_form_for_global_moderator(
    moderator_client, user_private_thread, user_private_thread_event
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread-event-delete",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_event_id": user_private_thread_event.id,
            },
        ),
    )

    assert_contains(response, "Are you sure you want to delete this thread event?")


def test_private_thread_event_delete_view_deletes_event_for_global_moderator(
    moderator_client, user_private_thread, user_private_thread_event
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread-event-delete",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_event_id": user_private_thread_event.id,
            },
        ),
        {"confirm": "true"},
    )

    assert response.status_code == 302

    with pytest.raises(ThreadEvent.DoesNotExist):
        user_private_thread_event.refresh_from_db()


def test_private_thread_event_delete_view_returns_redirect_to_thread(
    moderator_client, user_private_thread, user_private_thread_event
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread-event-delete",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_event_id": user_private_thread_event.id,
            },
        ),
        {"confirm": "true"},
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"thread_id": user_private_thread.id, "slug": user_private_thread.slug},
    )


def test_private_thread_event_delete_view_returns_redirect_to_next_url(
    moderator_client, user_private_thread, user_private_thread_event
):
    next_url = reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
            "page": 2,
        },
    )
    next_url += "?redirect=1#update-123"

    response = moderator_client.post(
        reverse(
            "misago:private-thread-event-delete",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_event_id": user_private_thread_event.id,
            },
        ),
        {
            "confirm": "true",
            "next": next_url,
        },
    )

    assert response.status_code == 302
    assert response["location"] == next_url


def test_private_thread_event_delete_view_returns_redirect_to_thread_for_invalid_next_url(
    moderator_client, user_private_thread, user_private_thread_event
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread-event-delete",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_event_id": user_private_thread_event.id,
            },
        ),
        {
            "confirm": "true",
            "next": "/invalid/url/",
        },
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"thread_id": user_private_thread.id, "slug": user_private_thread.slug},
    )


def test_private_thread_event_delete_view_returns_404_error_for_not_found_thread_in_htmx(
    user_client,
):
    response = user_client.post(
        reverse(
            "misago:private-thread-event-delete",
            kwargs={
                "thread_id": 100,
                "slug": "not-found",
                "thread_event_id": 100,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 404


def test_private_thread_event_delete_view_returns_404_error_for_not_found_event_in_htmx(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-event-delete",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_event_id": 100,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 404


def test_private_thread_event_delete_view_returns_403_error_for_anonymous_user_in_htmx(
    client, user_private_thread, user_private_thread_event
):
    response = client.post(
        reverse(
            "misago:private-thread-event-delete",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_event_id": user_private_thread_event.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(
        response, "Only a moderator can delete thread events.", status_code=403
    )


def test_private_thread_event_delete_view_returns_403_error_for_user_in_htmx(
    user_client, user_private_thread, user_private_thread_event
):
    response = user_client.post(
        reverse(
            "misago:private-thread-event-delete",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_event_id": user_private_thread_event.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(
        response, "Only a moderator can delete thread events.", status_code=403
    )


def test_private_thread_event_delete_view_checks_private_threads_permission_in_htmx(
    user_client, members_group, user_private_thread, user_private_thread_event
):
    members_group.can_use_private_threads = False
    members_group.save()

    response = user_client.post(
        reverse(
            "misago:private-thread-event-delete",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_event_id": user_private_thread_event.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(response, "You can't use private threads.", status_code=403)


def test_private_thread_event_delete_view_checks_thread_permission_in_htmx(
    user_client, private_thread, private_thread_event
):
    response = user_client.post(
        reverse(
            "misago:private-thread-event-delete",
            kwargs={
                "thread_id": private_thread.id,
                "slug": private_thread.slug,
                "thread_event_id": private_thread_event.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 404


def test_private_thread_event_delete_view_checks_thread_event_permission_in_htmx(
    user_client, user_private_thread, hidden_user_private_thread_event
):
    response = user_client.post(
        reverse(
            "misago:private-thread-event-delete",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_event_id": hidden_user_private_thread_event.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 404


def test_private_thread_event_delete_view_deletes_event_for_private_threads_moderator_in_htmx(
    user_client, user, user_private_thread, user_private_thread_event
):
    Moderator.objects.create(
        private_threads=True,
        user=user,
        is_global=False,
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-event-delete",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_event_id": user_private_thread_event.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 200

    with pytest.raises(ThreadEvent.DoesNotExist):
        user_private_thread_event.refresh_from_db()


def test_private_thread_event_delete_view_deletes_event_for_global_moderator_in_htmx(
    moderator_client, user_private_thread, user_private_thread_event
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread-event-delete",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_event_id": user_private_thread_event.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 200

    with pytest.raises(ThreadEvent.DoesNotExist):
        user_private_thread_event.refresh_from_db()
