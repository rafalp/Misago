from django.urls import reverse

from ...permissions.models import Moderator
from ...test import assert_contains


def test_unhide_private_thread_update_view_returns_404_error_for_not_found_thread(
    user_client,
):
    response = user_client.post(
        reverse(
            "misago:unhide-private-thread-update",
            kwargs={
                "id": 100,
                "slug": "not-found",
                "thread_update": 100,
            },
        )
    )

    assert response.status_code == 404


def test_unhide_private_thread_update_view_returns_404_error_for_not_found_update(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:unhide-private-thread-update",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_update": 100,
            },
        )
    )

    assert response.status_code == 404


def test_unhide_private_thread_update_view_returns_403_error_for_anonymous_user(
    client, user_private_thread, hidden_user_private_thread_update
):
    response = client.post(
        reverse(
            "misago:unhide-private-thread-update",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_update": hidden_user_private_thread_update.id,
            },
        )
    )

    assert_contains(
        response, "Only a moderator can unhide thread updates.", status_code=403
    )


def test_unhide_private_thread_update_view_returns_404_error_for_user(
    user_client, user_private_thread, hidden_user_private_thread_update
):
    response = user_client.post(
        reverse(
            "misago:unhide-private-thread-update",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_update": hidden_user_private_thread_update.id,
            },
        )
    )

    assert response.status_code == 404


def test_unhide_private_thread_update_view_checks_private_threads_permission(
    user_client, members_group, user_private_thread, hidden_user_private_thread_update
):
    members_group.can_use_private_threads = False
    members_group.save()

    response = user_client.post(
        reverse(
            "misago:unhide-private-thread-update",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_update": hidden_user_private_thread_update.id,
            },
        )
    )

    assert_contains(response, "You can&#x27;t use private threads.", status_code=403)


def test_unhide_private_thread_update_view_checks_thread_permission(
    user_client, private_thread, hidden_private_thread_update
):
    private_thread.is_hidden = True
    private_thread.save()

    response = user_client.post(
        reverse(
            "misago:unhide-private-thread-update",
            kwargs={
                "id": private_thread.id,
                "slug": private_thread.slug,
                "thread_update": hidden_private_thread_update.id,
            },
        )
    )

    assert response.status_code == 404


def test_unhide_private_thread_update_view_unhides_update_for_private_threads_moderator(
    user_client, user, user_private_thread, hidden_user_private_thread_update
):
    Moderator.objects.create(
        private_threads=True,
        user=user,
        is_global=False,
    )

    response = user_client.post(
        reverse(
            "misago:unhide-private-thread-update",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_update": hidden_user_private_thread_update.id,
            },
        )
    )

    assert response.status_code == 302

    hidden_user_private_thread_update.refresh_from_db()
    assert not hidden_user_private_thread_update.is_hidden


def test_unhide_private_thread_update_view_unhides_update_for_global_moderator(
    moderator_client, user_private_thread, hidden_user_private_thread_update
):
    response = moderator_client.post(
        reverse(
            "misago:unhide-private-thread-update",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_update": hidden_user_private_thread_update.id,
            },
        )
    )

    assert response.status_code == 302

    hidden_user_private_thread_update.refresh_from_db()
    assert not hidden_user_private_thread_update.is_hidden


def test_unhide_private_thread_update_view_doesnt_update_already_unhidden_update(
    moderator_client, user_private_thread, user_private_thread_update
):
    response = moderator_client.post(
        reverse(
            "misago:unhide-private-thread-update",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_update": user_private_thread_update.id,
            },
        )
    )

    assert response.status_code == 302

    user_private_thread_update.refresh_from_db()
    assert not user_private_thread_update.is_hidden


def test_unhide_private_thread_update_view_returns_redirect_to_thread(
    moderator_client, user_private_thread, hidden_user_private_thread_update
):
    response = moderator_client.post(
        reverse(
            "misago:unhide-private-thread-update",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_update": hidden_user_private_thread_update.id,
            },
        )
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
    )


def test_unhide_private_thread_update_view_returns_redirect_to_next_url(
    moderator_client, user_private_thread, hidden_user_private_thread_update
):
    next_url = reverse(
        "misago:private-thread",
        kwargs={
            "id": user_private_thread.id,
            "slug": user_private_thread.slug,
            "page": 2,
        },
    )
    next_url += "?redirect=1#update-123"

    response = moderator_client.post(
        reverse(
            "misago:unhide-private-thread-update",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_update": hidden_user_private_thread_update.id,
            },
        ),
        {"next": next_url},
    )

    assert response.status_code == 302
    assert response["location"] == next_url


def test_unhide_private_thread_update_view_returns_redirect_to_thread_for_invalid_next_url(
    moderator_client, user_private_thread, hidden_user_private_thread_update
):
    response = moderator_client.post(
        reverse(
            "misago:unhide-private-thread-update",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_update": hidden_user_private_thread_update.id,
            },
        ),
        {"next": "/invalid/url/"},
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
    )


def test_unhide_private_thread_update_view_returns_404_error_for_not_found_update_in_htmx(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:unhide-private-thread-update",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_update": 100,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 404


def test_unhide_private_thread_update_view_returns_404_error_for_not_found_thread_in_htmx(
    user_client,
):
    response = user_client.post(
        reverse(
            "misago:unhide-private-thread-update",
            kwargs={
                "id": 100,
                "slug": "not-found",
                "thread_update": 100,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 404


def test_unhide_private_thread_update_view_returns_403_error_for_anonymous_user_in_htmx(
    client, user_private_thread, hidden_user_private_thread_update
):
    response = client.post(
        reverse(
            "misago:unhide-private-thread-update",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_update": hidden_user_private_thread_update.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(
        response, "Only a moderator can unhide thread updates.", status_code=403
    )


def test_unhide_private_thread_update_view_returns_404_error_for_user_in_htmx(
    user_client, user_private_thread, hidden_user_private_thread_update
):
    response = user_client.post(
        reverse(
            "misago:unhide-private-thread-update",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_update": hidden_user_private_thread_update.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 404


def test_unhide_private_thread_update_view_checks_private_threads_permission_in_htmx(
    user_client, members_group, user_private_thread, hidden_user_private_thread_update
):
    members_group.can_use_private_threads = False
    members_group.save()

    response = user_client.post(
        reverse(
            "misago:unhide-private-thread-update",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_update": hidden_user_private_thread_update.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(response, "You can't use private threads.", status_code=403)


def test_unhide_private_thread_update_view_checks_thread_permission_in_htmx(
    user_client, private_thread, hidden_user_private_thread_update
):
    private_thread.is_hidden = True
    private_thread.save()

    response = user_client.post(
        reverse(
            "misago:unhide-private-thread-update",
            kwargs={
                "id": private_thread.id,
                "slug": private_thread.slug,
                "thread_update": hidden_user_private_thread_update.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 404


def test_unhide_private_thread_update_view_checks_thread_update_permission_in_htmx(
    user_client, user_private_thread, hidden_private_thread_update
):
    response = user_client.post(
        reverse(
            "misago:unhide-private-thread-update",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_update": hidden_private_thread_update.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 404


def test_unhide_private_thread_update_view_unhides_update_for_private_threads_moderator_in_htmx(
    user_client, user, user_private_thread, hidden_user_private_thread_update
):
    Moderator.objects.create(
        private_threads=True,
        user=user,
        is_global=False,
    )

    response = user_client.post(
        reverse(
            "misago:unhide-private-thread-update",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_update": hidden_user_private_thread_update.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 200

    hidden_user_private_thread_update.refresh_from_db()
    assert not hidden_user_private_thread_update.is_hidden


def test_unhide_private_thread_update_view_unhides_update_for_global_moderator_in_htmx(
    moderator_client, user_private_thread, hidden_user_private_thread_update
):
    response = moderator_client.post(
        reverse(
            "misago:unhide-private-thread-update",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_update": hidden_user_private_thread_update.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 200

    hidden_user_private_thread_update.refresh_from_db()
    assert not hidden_user_private_thread_update.is_hidden


def test_unhide_private_thread_update_view_doesnt_update_already_unhidden_update_in_htmx(
    moderator_client, user_private_thread, user_private_thread_update
):

    response = moderator_client.post(
        reverse(
            "misago:unhide-private-thread-update",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "thread_update": user_private_thread_update.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 200

    user_private_thread_update.refresh_from_db()
    assert not user_private_thread_update.is_hidden
