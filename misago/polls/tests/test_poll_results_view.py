from django.urls import reverse

from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_not_contains


def test_poll_results_view_shows_error_if_guest_has_no_category_permission(
    client, guests_group, thread, poll
):
    CategoryGroupPermission.objects.filter(group=guests_group).delete()

    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=results",
    )
    assert response.status_code == 404


def test_poll_results_view_shows_error_if_user_has_no_category_permission(
    user_client, members_group, thread, poll
):
    CategoryGroupPermission.objects.filter(group=members_group).delete()

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=results",
    )
    assert response.status_code == 404


def test_poll_voters_view_shows_error_if_guest_has_no_category_permission(
    client, guests_group, thread, poll
):
    CategoryGroupPermission.objects.filter(group=guests_group).delete()

    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
    )
    assert response.status_code == 404


def test_poll_voters_view_shows_error_if_user_has_no_category_permission(
    user_client, members_group, thread, poll
):
    CategoryGroupPermission.objects.filter(group=members_group).delete()

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
    )
    assert response.status_code == 404


def test_poll_results_view_shows_error_if_guest_has_no_thread_permission(
    client, thread, poll
):
    thread.is_unapproved = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=results",
    )
    assert response.status_code == 404


def test_poll_results_view_shows_error_if_user_has_no_thread_permission(
    user_client, thread, poll
):
    thread.is_unapproved = True
    thread.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=results",
    )
    assert response.status_code == 404


def test_poll_voters_view_shows_error_if_guest_has_no_thread_permission(
    client, thread, poll
):
    thread.is_unapproved = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
    )
    assert response.status_code == 404


def test_poll_voters_view_shows_error_if_user_has_no_thread_permission(
    user_client, thread, poll
):
    thread.is_unapproved = True
    thread.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
    )
    assert response.status_code == 404


def test_poll_results_view_doesnt_show_for_guest_if_thread_has_no_poll(client, thread):
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=results",
    )
    assert response.status_code == 200


def test_poll_results_view_shows_error_404_for_guest_if_thread_has_no_poll_in_htmx(
    client, thread
):
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=results",
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_poll_results_view_doesnt_show_for_user_if_thread_has_no_poll(
    user_client, thread
):
    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=results",
    )
    assert response.status_code == 200


def test_poll_results_view_shows_error_404_for_user_if_thread_has_no_poll_in_htmx(
    user_client, thread
):
    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=results",
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_poll_voters_view_doesnt_show_for_guest_if_thread_has_no_poll(client, thread):
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
    )
    assert response.status_code == 200


def test_poll_voters_view_shows_error_404_for_guest_if_thread_has_no_poll_in_htmx(
    client, thread
):
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_poll_voters_view_doesnt_show_for_user_if_thread_has_no_poll(
    user_client, thread
):
    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
    )
    assert response.status_code == 200


def test_poll_voters_view_shows_error_404_for_user_if_thread_has_no_poll_in_htmx(
    user_client, thread
):
    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404
