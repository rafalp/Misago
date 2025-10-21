from django.urls import reverse

from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission, Moderator
from ...test import assert_contains


def test_thread_update_hide_view_returns_404_error_for_not_found_thread(user_client):
    response = user_client.post(
        reverse(
            "misago:thread-update-hide",
            kwargs={
                "thread_id": 100,
                "slug": "not-found",
                "thread_update_id": 100,
            },
        )
    )

    assert response.status_code == 404


def test_thread_update_hide_view_returns_404_error_for_not_found_update(
    user_client, thread
):
    response = user_client.post(
        reverse(
            "misago:thread-update-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_update_id": 100,
            },
        )
    )

    assert response.status_code == 404


def test_thread_update_hide_view_returns_403_error_for_anonymous_user(
    client, thread, thread_update
):
    response = client.post(
        reverse(
            "misago:thread-update-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_update_id": thread_update.id,
            },
        )
    )

    assert_contains(
        response, "Only a moderator can hide thread updates.", status_code=403
    )


def test_thread_update_hide_view_returns_403_error_for_user(
    user_client, thread, thread_update
):
    response = user_client.post(
        reverse(
            "misago:thread-update-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_update_id": thread_update.id,
            },
        )
    )

    assert_contains(
        response, "Only a moderator can hide thread updates.", status_code=403
    )


def test_thread_update_hide_view_checks_category_permission(
    user_client, thread, thread_update
):
    CategoryGroupPermission.objects.filter(
        permission=CategoryPermission.BROWSE
    ).delete()

    response = user_client.post(
        reverse(
            "misago:thread-update-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_update_id": thread_update.id,
            },
        )
    )

    assert response.status_code == 404


def test_thread_update_hide_view_checks_thread_permission(
    user_client, thread, thread_update
):
    thread.is_hidden = True
    thread.save()

    response = user_client.post(
        reverse(
            "misago:thread-update-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_update_id": thread_update.id,
            },
        )
    )

    assert response.status_code == 404


def test_thread_update_hide_view_checks_thread_update_permission(
    user_client, thread, hidden_thread_update
):
    response = user_client.post(
        reverse(
            "misago:thread-update-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_update_id": hidden_thread_update.id,
            },
        )
    )

    assert response.status_code == 404


def test_thread_update_hide_view_hides_update_for_category_moderator(
    user_client, user, default_category, thread, thread_update
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )

    response = user_client.post(
        reverse(
            "misago:thread-update-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_update_id": thread_update.id,
            },
        )
    )

    assert response.status_code == 302

    thread_update.refresh_from_db()
    assert thread_update.is_hidden


def test_thread_update_hide_view_hides_update_for_global_moderator(
    moderator_client, thread, thread_update
):
    response = moderator_client.post(
        reverse(
            "misago:thread-update-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_update_id": thread_update.id,
            },
        )
    )

    assert response.status_code == 302

    thread_update.refresh_from_db()
    assert thread_update.is_hidden


def test_thread_update_hide_view_doesnt_update_already_hidden_update(
    moderator_client, thread, hidden_thread_update
):
    response = moderator_client.post(
        reverse(
            "misago:thread-update-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_update_id": hidden_thread_update.id,
            },
        )
    )

    assert response.status_code == 302

    hidden_thread_update.refresh_from_db()
    assert hidden_thread_update.is_hidden


def test_thread_update_hide_view_returns_redirect_to_thread(
    moderator_client, thread, thread_update
):
    response = moderator_client.post(
        reverse(
            "misago:thread-update-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_update_id": thread_update.id,
            },
        )
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )


def test_thread_update_hide_view_returns_redirect_to_next_url(
    moderator_client, thread, thread_update
):
    next_url = reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug, "page": 2}
    )
    next_url += "?redirect=1#update-123"

    response = moderator_client.post(
        reverse(
            "misago:thread-update-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_update_id": thread_update.id,
            },
        ),
        {"next": next_url},
    )

    assert response.status_code == 302
    assert response["location"] == next_url


def test_thread_update_hide_view_returns_redirect_to_thread_for_invalid_next_url(
    moderator_client, thread, thread_update
):
    response = moderator_client.post(
        reverse(
            "misago:thread-update-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_update_id": thread_update.id,
            },
        ),
        {"next": "/invalid/url/"},
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )


def test_thread_update_hide_view_returns_404_error_for_not_found_thread_in_htmx(
    user_client,
):
    response = user_client.post(
        reverse(
            "misago:thread-update-hide",
            kwargs={
                "thread_id": 100,
                "slug": "not-found",
                "thread_update_id": 100,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 404


def test_thread_update_hide_view_returns_404_error_for_not_found_update_in_htmx(
    user_client, thread
):
    response = user_client.post(
        reverse(
            "misago:thread-update-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_update_id": 100,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 404


def test_thread_update_hide_view_returns_403_error_for_anonymous_user_in_htmx(
    client, thread, thread_update
):
    response = client.post(
        reverse(
            "misago:thread-update-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_update_id": thread_update.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(
        response, "Only a moderator can hide thread updates.", status_code=403
    )


def test_thread_update_hide_view_returns_403_error_for_user_in_htmx(
    user_client, thread, thread_update
):
    response = user_client.post(
        reverse(
            "misago:thread-update-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_update_id": thread_update.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(
        response, "Only a moderator can hide thread updates.", status_code=403
    )


def test_thread_update_hide_view_checks_category_permission_in_htmx(
    user_client, thread, thread_update
):
    CategoryGroupPermission.objects.filter(
        permission=CategoryPermission.BROWSE
    ).delete()

    response = user_client.post(
        reverse(
            "misago:thread-update-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_update_id": thread_update.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 404


def test_thread_update_hide_view_checks_thread_permission_in_htmx(
    user_client, thread, thread_update
):
    thread.is_hidden = True
    thread.save()

    response = user_client.post(
        reverse(
            "misago:thread-update-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_update_id": thread_update.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 404


def test_thread_update_hide_view_checks_thread_update_permission_in_htmx(
    user_client, thread, hidden_thread_update
):
    response = user_client.post(
        reverse(
            "misago:thread-update-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_update_id": hidden_thread_update.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 404


def test_thread_update_hide_view_hides_update_for_category_moderator_in_htmx(
    user_client, user, default_category, thread, thread_update
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )

    response = user_client.post(
        reverse(
            "misago:thread-update-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_update_id": thread_update.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 200

    thread_update.refresh_from_db()
    assert thread_update.is_hidden


def test_thread_update_hide_view_hides_update_for_global_moderator_in_htmx(
    moderator_client, thread, thread_update
):
    response = moderator_client.post(
        reverse(
            "misago:thread-update-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_update_id": thread_update.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 200

    thread_update.refresh_from_db()
    assert thread_update.is_hidden


def test_thread_update_hide_view_doesnt_update_already_hidden_update_in_htmx(
    moderator_client, thread, hidden_thread_update
):
    response = moderator_client.post(
        reverse(
            "misago:thread-update-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_update_id": hidden_thread_update.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 200

    hidden_thread_update.refresh_from_db()
    assert hidden_thread_update.is_hidden
