import pytest
from django.urls import reverse

from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission, Moderator
from ...test import assert_contains
from ..create import create_test_thread_update
from ..models import ThreadEvent


def test_thread_update_delete_view_returns_404_error_for_not_found_thread(user_client):
    response = user_client.post(
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": 100,
                "slug": "not-found",
                "thread_event_id": 100,
            },
        )
    )

    assert response.status_code == 404


def test_thread_update_delete_view_returns_404_error_for_not_found_update(
    user_client, thread
):
    response = user_client.post(
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": 100,
            },
        )
    )

    assert response.status_code == 404


def test_thread_update_delete_view_returns_403_error_for_anonymous_user(
    client, thread, thread_event
):
    response = client.post(
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        )
    )

    assert_contains(
        response, "Only a moderator can delete thread updates.", status_code=403
    )


def test_thread_update_delete_view_returns_403_error_for_user(
    user_client, thread, thread_event
):
    response = user_client.post(
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        )
    )

    assert_contains(
        response, "Only a moderator can delete thread updates.", status_code=403
    )


def test_thread_update_delete_view_checks_category_permission(
    user_client, thread, thread_event
):
    CategoryGroupPermission.objects.filter(
        permission=CategoryPermission.BROWSE
    ).delete()

    response = user_client.post(
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        )
    )

    assert response.status_code == 404


def test_thread_update_delete_view_checks_thread_permission(
    user_client, thread, thread_event
):
    thread.is_hidden = True
    thread.save()

    response = user_client.post(
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        )
    )

    assert response.status_code == 404


def test_thread_update_delete_view_checks_thread_update_permission(
    user_client, thread, hidden_thread_event
):
    response = user_client.post(
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": hidden_thread_event.id,
            },
        )
    )

    assert response.status_code == 404


def test_thread_update_delete_view_shows_confirm_delete_form_for_category_moderator(
    user_client, user, default_category, thread, thread_event
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )

    response = user_client.post(
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        ),
    )

    assert_contains(response, "Are you sure you want to delete this thread update?")


def test_thread_update_delete_view_deletes_update_for_category_moderator(
    user_client, user, default_category, thread, thread_event
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )

    response = user_client.post(
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        ),
        {"confirm": "true"},
    )

    assert response.status_code == 302

    with pytest.raises(ThreadEvent.DoesNotExist):
        thread_event.refresh_from_db()


def test_thread_update_delete_view_shows_confirm_delete_form_for_global_moderator(
    moderator_client, thread, thread_event
):
    response = moderator_client.post(
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        ),
    )

    assert_contains(response, "Are you sure you want to delete this thread update?")


def test_thread_update_delete_view_deletes_update_for_global_moderator(
    moderator_client, thread, thread_event
):
    response = moderator_client.post(
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        ),
        {"confirm": "true"},
    )

    assert response.status_code == 302

    with pytest.raises(ThreadEvent.DoesNotExist):
        thread_event.refresh_from_db()


def test_thread_update_delete_view_unsets_thread_has_updates_flag_for_last_update_deleted(
    moderator_client, thread, thread_event
):
    thread.has_events = True
    thread.save()

    response = moderator_client.post(
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        ),
        {"confirm": "true"},
    )

    assert response.status_code == 302

    thread.refresh_from_db()
    assert not thread.has_events

    with pytest.raises(ThreadEvent.DoesNotExist):
        thread_event.refresh_from_db()


def test_thread_update_delete_view_keeps_thread_has_updates_flag_if_other_updates_exist(
    moderator_client, thread, thread_event
):
    thread.has_events = True
    thread.save()

    create_test_thread_update(thread, "DeletedUser")

    response = moderator_client.post(
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        ),
        {"confirm": "true"},
    )

    assert response.status_code == 302

    thread.refresh_from_db()
    assert thread.has_events

    with pytest.raises(ThreadEvent.DoesNotExist):
        thread_event.refresh_from_db()


def test_thread_update_delete_view_returns_redirect_to_thread(
    moderator_client, thread, thread_event
):
    response = moderator_client.post(
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        ),
        {"confirm": "true"},
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )


def test_thread_update_delete_view_returns_redirect_to_next_url(
    moderator_client, thread, thread_event
):
    next_url = reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug, "page": 2}
    )
    next_url += "?redirect=1#update-123"

    response = moderator_client.post(
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        ),
        {
            "confirm": "true",
            "next": next_url,
        },
    )

    assert response.status_code == 302
    assert response["location"] == next_url


def test_thread_update_delete_view_returns_redirect_to_thread_for_invalid_next_url(
    moderator_client, thread, thread_event
):
    response = moderator_client.post(
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        ),
        {
            "confirm": "true",
            "next": "/invalid/url/",
        },
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )


def test_thread_update_delete_view_returns_404_error_for_not_found_thread_in_htmx(
    user_client,
):
    response = user_client.post(
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": 100,
                "slug": "not-found",
                "thread_event_id": 100,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 404


def test_thread_update_delete_view_returns_404_error_for_not_found_update_in_htmx(
    user_client, thread
):
    response = user_client.post(
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": 100,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 404


def test_thread_update_delete_view_returns_403_error_for_anonymous_user_in_htmx(
    client, thread, thread_event
):
    response = client.post(
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(
        response, "Only a moderator can delete thread updates.", status_code=403
    )


def test_thread_update_delete_view_returns_403_error_for_user_in_htmx(
    user_client, thread, thread_event
):
    response = user_client.post(
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(
        response, "Only a moderator can delete thread updates.", status_code=403
    )


def test_thread_update_delete_view_checks_category_permission_in_htmx(
    user_client, thread, thread_event
):
    CategoryGroupPermission.objects.filter(
        permission=CategoryPermission.BROWSE
    ).delete()

    response = user_client.post(
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 404


def test_thread_update_delete_view_checks_thread_permission_in_htmx(
    user_client, thread, thread_event
):
    thread.is_hidden = True
    thread.save()

    response = user_client.post(
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 404


def test_thread_update_delete_view_checks_thread_update_permission_in_htmx(
    user_client, thread, hidden_thread_event
):
    response = user_client.post(
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": hidden_thread_event.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 404


def test_thread_update_delete_view_deletes_update_for_category_moderator_in_htmx(
    user_client, user, default_category, thread, thread_event
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )

    response = user_client.post(
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 200

    with pytest.raises(ThreadEvent.DoesNotExist):
        thread_event.refresh_from_db()


def test_thread_update_delete_view_deletes_update_for_global_moderator_in_htmx(
    moderator_client, thread, thread_event
):
    response = moderator_client.post(
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 200

    with pytest.raises(ThreadEvent.DoesNotExist):
        thread_event.refresh_from_db()
