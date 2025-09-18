from django.urls import reverse

from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_has_success_message


def test_open_thread_poll_view_opens_poll(moderator_client, thread, closed_poll):
    assert thread.has_poll

    response = moderator_client.post(
        reverse(
            "misago:thread-poll-open",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    assert_has_success_message(response, "Poll opened")

    closed_poll.refresh_from_db()
    assert not closed_poll.is_closed


def test_open_thread_poll_view_returns_redirect_to_next_thread_url(
    moderator_client, thread, closed_poll
):
    thread_url = reverse(
        "misago:thread",
        kwargs={"thread_id": thread.id, "slug": thread.slug, "page": 12},
    )

    response = moderator_client.post(
        reverse(
            "misago:thread-poll-open",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
        {"next": thread_url},
    )
    assert response.status_code == 302
    assert response["location"] == thread_url


def test_open_thread_poll_view_returns_redirect_to_default_thread_url_if_next_url_is_invalid(
    moderator_client, thread, closed_poll
):
    response = moderator_client.post(
        reverse(
            "misago:thread-poll-open",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
        {"next": "invalid"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )


def test_open_thread_poll_view_returns_partial_in_htmx(
    moderator_client, thread, closed_poll
):
    thread_url = reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    response = moderator_client.post(
        reverse(
            "misago:thread-poll-open",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
        {"next": f"{thread_url}extra/"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Opened poll")
    assert_contains(response, closed_poll.question)


def test_open_thread_poll_view_returns_404_if_thread_doesnt_exist(moderator_client):
    response = moderator_client.post(
        reverse(
            "misago:thread-poll-open",
            kwargs={"thread_id": 1, "slug": "invalid"},
        )
    )
    assert response.status_code == 404


def test_open_thread_poll_view_returns_404_if_thread_has_no_poll(
    moderator_client, thread
):
    assert not thread.has_poll

    response = moderator_client.post(
        reverse(
            "misago:thread-poll-open",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )
    assert response.status_code == 404


def test_open_thread_poll_view_checks_category_permission(
    user_client, thread, closed_poll
):
    CategoryGroupPermission.objects.filter(category=thread.category).delete()

    assert thread.has_poll

    response = user_client.post(
        reverse(
            "misago:thread-poll-open",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )
    assert response.status_code == 404

    thread.refresh_from_db()
    assert thread.has_poll

    closed_poll.refresh_from_db()
    assert closed_poll.is_closed


def test_open_thread_poll_view_checks_thread_permission(
    user_client, thread, closed_poll
):
    thread.is_hidden = True
    thread.save()

    assert thread.has_poll

    response = user_client.post(
        reverse(
            "misago:thread-poll-open",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )
    assert response.status_code == 404

    thread.refresh_from_db()
    assert thread.has_poll

    closed_poll.refresh_from_db()
    assert closed_poll.is_closed


def test_open_thread_poll_view_checks_open_poll_permission(
    user_client, user_thread, closed_user_poll
):
    assert user_thread.has_poll

    response = user_client.post(
        reverse(
            "misago:thread-poll-open",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        )
    )
    assert response.status_code == 403

    user_thread.refresh_from_db()
    assert user_thread.has_poll

    closed_user_poll.refresh_from_db()
    assert closed_user_poll.is_closed
