import pytest
from django.urls import reverse

from ...permissions.models import CategoryGroupPermission
from ...test import assert_has_success_message
from ..models import Poll


def test_delete_thread_poll_view_deletes_poll(moderator_client, thread, poll):
    assert thread.has_poll

    response = moderator_client.post(
        reverse(
            "misago:thread-poll-delete",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    assert_has_success_message(response, "Poll deleted")

    thread.refresh_from_db()
    assert not thread.has_poll

    with pytest.raises(Poll.DoesNotExist):
        poll.refresh_from_db()


def test_delete_thread_poll_view_returns_redirect_to_next_thread_url(
    moderator_client, thread, poll
):
    thread_url = reverse(
        "misago:thread",
        kwargs={"thread_id": thread.id, "slug": thread.slug, "page": 12},
    )

    response = moderator_client.post(
        reverse(
            "misago:thread-poll-delete",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
        {"next": thread_url},
    )
    assert response.status_code == 302
    assert response["location"] == thread_url


def test_delete_thread_poll_view_returns_redirect_to_default_thread_url_if_next_url_is_invalid(
    moderator_client, thread, poll
):
    response = moderator_client.post(
        reverse(
            "misago:thread-poll-delete",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
        {"next": "invalid"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )


def test_delete_thread_poll_view_returns_404_if_thread_doesnt_exist(moderator_client):
    response = moderator_client.post(
        reverse(
            "misago:thread-poll-delete",
            kwargs={"thread_id": 1, "slug": "invalid"},
        )
    )
    assert response.status_code == 404


def test_delete_thread_poll_view_returns_404_if_thread_has_no_poll(
    moderator_client, thread
):
    assert not thread.has_poll

    response = moderator_client.post(
        reverse(
            "misago:thread-poll-delete",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )
    assert response.status_code == 404


def test_delete_thread_poll_view_checks_category_permission(user_client, thread, poll):
    CategoryGroupPermission.objects.filter(category=thread.category).delete()

    assert thread.has_poll

    response = user_client.post(
        reverse(
            "misago:thread-poll-delete",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )
    assert response.status_code == 404

    thread.refresh_from_db()
    assert thread.has_poll

    poll.refresh_from_db()


def test_delete_thread_poll_view_checks_thread_permission(user_client, thread, poll):
    thread.is_hidden = True
    thread.save()

    assert thread.has_poll

    response = user_client.post(
        reverse(
            "misago:thread-poll-delete",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )
    assert response.status_code == 404

    thread.refresh_from_db()
    assert thread.has_poll

    poll.refresh_from_db()


def test_delete_thread_poll_view_checks_delete_poll_permission(
    user_client, thread, poll
):
    assert thread.has_poll

    response = user_client.post(
        reverse(
            "misago:thread-poll-delete",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )
    assert response.status_code == 403

    thread.refresh_from_db()
    assert thread.has_poll

    poll.refresh_from_db()
