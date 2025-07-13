from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_not_contains
from ..enums import PublicPollsAvailability


def test_poll_start_view_shows_error_if_guest_has_no_category_permission(
    client, guests_group, thread
):
    CategoryGroupPermission.objects.filter(group=guests_group).delete()

    response = client.get(
        reverse(
            "misago:start-thread-poll", kwargs={"id": thread.id, "slug": thread.slug}
        ),
    )
    assert response.status_code == 404


def test_poll_start_view_shows_error_if_guest_has_no_category_permission_in_htmx(
    client, guests_group, thread
):
    CategoryGroupPermission.objects.filter(group=guests_group).delete()

    response = client.get(
        reverse(
            "misago:start-thread-poll", kwargs={"id": thread.id, "slug": thread.slug}
        ),
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_poll_start_view_shows_error_if_user_has_no_category_permission(
    user_client, members_group, thread
):
    CategoryGroupPermission.objects.filter(group=members_group).delete()

    response = user_client.get(
        reverse(
            "misago:start-thread-poll", kwargs={"id": thread.id, "slug": thread.slug}
        ),
    )
    assert response.status_code == 404


def test_poll_start_view_shows_error_if_user_has_no_category_permission_in_htmx(
    user_client, members_group, thread
):
    CategoryGroupPermission.objects.filter(group=members_group).delete()

    response = user_client.get(
        reverse(
            "misago:start-thread-poll", kwargs={"id": thread.id, "slug": thread.slug}
        ),
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_poll_start_view_shows_error_if_guest_has_no_thread_permission(
    client, guests_group, thread
):
    thread.is_unapproved = True
    thread.save()

    response = client.get(
        reverse(
            "misago:start-thread-poll", kwargs={"id": thread.id, "slug": thread.slug}
        ),
    )
    assert response.status_code == 404


def test_poll_start_view_shows_error_if_guest_has_no_thread_permission_in_htmx(
    client, guests_group, thread
):
    thread.is_unapproved = True
    thread.save()

    response = client.get(
        reverse(
            "misago:start-thread-poll", kwargs={"id": thread.id, "slug": thread.slug}
        ),
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_poll_start_view_shows_error_if_user_has_no_thread_permission(
    user_client, members_group, thread
):
    thread.is_unapproved = True
    thread.save()

    response = user_client.get(
        reverse(
            "misago:start-thread-poll", kwargs={"id": thread.id, "slug": thread.slug}
        ),
    )
    assert response.status_code == 404


def test_poll_start_view_shows_error_if_user_has_no_thread_permission_in_htmx(
    user_client, members_group, thread
):
    thread.is_unapproved = True
    thread.save()

    response = user_client.get(
        reverse(
            "misago:start-thread-poll", kwargs={"id": thread.id, "slug": thread.slug}
        ),
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_poll_start_view_shows_error_for_guests(client, thread):
    response = client.get(
        reverse(
            "misago:start-thread-poll", kwargs={"id": thread.id, "slug": thread.slug}
        ),
    )
    assert_contains(response, "You must be signed in to start polls.", 403)


def test_poll_start_view_shows_error_for_guests_in_htmx(client, thread):
    response = client.get(
        reverse(
            "misago:start-thread-poll", kwargs={"id": thread.id, "slug": thread.slug}
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "You must be signed in to start polls.", 403)


def test_poll_start_view_shows_error_for_user_without_permission(user_client, thread):
    response = user_client.get(
        reverse(
            "misago:start-thread-poll", kwargs={"id": thread.id, "slug": thread.slug}
        ),
    )
    assert_contains(
        response, "You can&#x27;t start polls in other users&#x27; threads.", 403
    )


def test_poll_start_view_shows_error_for_user_without_permission_in_htmx(
    user_client, thread
):
    response = user_client.get(
        reverse(
            "misago:start-thread-poll", kwargs={"id": thread.id, "slug": thread.slug}
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "You can't start polls in other users' threads.", 403)


def test_poll_start_view_shows_error_for_user_with_permission_if_thread_has_poll(
    user_client, user_thread, user_poll
):
    response = user_client.get(
        reverse(
            "misago:start-thread-poll",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
    )
    assert_contains(response, "This thread already has a poll.", 403)


def test_poll_start_view_shows_error_for_user_with_permission_if_thread_has_poll_in_htmx(
    user_client, user_thread, user_poll
):
    response = user_client.get(
        reverse(
            "misago:start-thread-poll",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "This thread already has a poll.", 403)
