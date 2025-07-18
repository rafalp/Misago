from django.urls import reverse

from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_not_contains
from ..models import Poll


def test_edit_thread_poll_view_shows_error_if_guest_has_no_category_permission(
    client, guests_group, user_thread, user_poll
):
    CategoryGroupPermission.objects.filter(group=guests_group).delete()

    response = client.get(
        reverse(
            "misago:edit-thread-poll",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
    )
    assert response.status_code == 404


def test_edit_thread_poll_view_shows_error_if_guest_has_no_category_permission_in_htmx(
    client, guests_group, user_thread, user_poll
):
    CategoryGroupPermission.objects.filter(group=guests_group).delete()

    response = client.get(
        reverse(
            "misago:edit-thread-poll",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_edit_thread_poll_view_shows_error_if_user_has_no_category_permission(
    user_client, members_group, user_thread, user_poll
):
    CategoryGroupPermission.objects.filter(group=members_group).delete()

    response = user_client.get(
        reverse(
            "misago:edit-thread-poll",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
    )
    assert response.status_code == 404


def test_edit_thread_poll_view_shows_error_if_user_has_no_category_permission_in_htmx(
    user_client, members_group, user_thread, user_poll
):
    CategoryGroupPermission.objects.filter(group=members_group).delete()

    response = user_client.get(
        reverse(
            "misago:edit-thread-poll",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_edit_thread_poll_view_shows_error_if_guest_has_no_thread_permission(
    client, user_thread, user_poll
):
    user_thread.is_hidden = True
    user_thread.save()

    response = client.get(
        reverse(
            "misago:edit-thread-poll",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
    )
    assert response.status_code == 404


def test_edit_thread_poll_view_shows_error_if_guest_has_no_thread_permission_in_htmx(
    client, user_thread, user_poll
):
    user_thread.is_hidden = True
    user_thread.save()

    response = client.get(
        reverse(
            "misago:edit-thread-poll",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_edit_thread_poll_view_shows_error_if_user_has_no_thread_permission(
    user_client, user_thread, user_poll
):
    user_thread.is_hidden = True
    user_thread.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread-poll",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
    )
    assert response.status_code == 404


def test_edit_thread_poll_view_shows_error_if_user_has_no_thread_permission_in_htmx(
    user_client, user_thread, user_poll
):
    user_thread.is_hidden = True
    user_thread.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread-poll",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_edit_thread_poll_view_shows_error_for_guests(client, user_thread, user_poll):
    response = client.get(
        reverse(
            "misago:edit-thread-poll",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
    )
    assert_contains(
        response, "You can&#x27;t edit polls in other users&#x27; threads.", 403
    )


def test_edit_thread_poll_view_shows_error_for_guests_in_htmx(
    client, user_thread, user_poll
):
    response = client.get(
        reverse(
            "misago:edit-thread-poll",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "You can't edit polls in other users' threads.", 403)


def test_edit_thread_poll_view_shows_error_if_user_has_no_edit_poll_permission(
    user_client, user_thread, user_poll
):
    user_thread.is_closed = True
    user_thread.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread-poll",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
    )
    assert_contains(response, "This thread is closed.", 403)


def test_edit_thread_poll_view_shows_error_if_user_has_no_edit_poll_permission_in_htmx(
    user_client, user_thread, user_poll
):
    user_thread.is_closed = True
    user_thread.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread-poll",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "This thread is closed.", 403)


def test_edit_thread_poll_view_shows_guest_error_404_if_thread_has_no_poll(
    client, user_thread
):
    response = client.get(
        reverse(
            "misago:edit-thread-poll",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
    )
    assert response.status_code == 404


def test_edit_thread_poll_view_shows_guest_error_404_if_thread_has_no_poll_in_htmx(
    client, user_thread
):
    response = client.get(
        reverse(
            "misago:edit-thread-poll",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_edit_thread_poll_view_shows_user_error_404_if_thread_has_no_poll(
    user_client, user_thread
):
    response = user_client.get(
        reverse(
            "misago:edit-thread-poll",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
    )
    assert response.status_code == 404


def test_edit_thread_poll_view_shows_user_error_404_if_thread_has_no_poll_in_htmx(
    user_client, user_thread
):
    response = user_client.get(
        reverse(
            "misago:edit-thread-poll",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404
