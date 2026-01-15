from unittest.mock import ANY

from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_not_contains
from ..enums import PublicPollsAvailability
from ..models import Poll


def test_start_thread_poll_view_shows_error_if_guest_has_no_category_permission(
    client, guests_group, thread
):
    CategoryGroupPermission.objects.filter(group=guests_group).delete()

    response = client.get(
        reverse(
            "misago:thread-poll-start",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
    )
    assert response.status_code == 404


def test_start_thread_poll_view_shows_error_if_user_has_no_category_permission(
    user_client, members_group, thread
):
    CategoryGroupPermission.objects.filter(group=members_group).delete()

    response = user_client.get(
        reverse(
            "misago:thread-poll-start",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
    )
    assert response.status_code == 404


def test_start_thread_poll_view_shows_error_if_guest_has_no_thread_permission(
    client, thread
):
    thread.is_unapproved = True
    thread.save()

    response = client.get(
        reverse(
            "misago:thread-poll-start",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
    )
    assert response.status_code == 404


def test_start_thread_poll_view_shows_error_if_user_has_no_thread_permission(
    user_client, thread
):
    thread.is_unapproved = True
    thread.save()

    response = user_client.get(
        reverse(
            "misago:thread-poll-start",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
    )
    assert response.status_code == 404


def test_start_thread_poll_view_shows_error_to_anonymous_users(client, thread):
    response = client.get(
        reverse(
            "misago:thread-poll-start",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
    )
    assert_contains(response, "You must be signed in to start polls.", 403)


def test_start_thread_poll_view_shows_error_for_user_without_permission(
    user_client, thread
):
    response = user_client.get(
        reverse(
            "misago:thread-poll-start",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
    )
    assert_contains(
        response, "You can&#x27;t start polls in other users&#x27; threads.", 403
    )


def test_start_thread_poll_view_shows_error_for_user_with_permission_if_thread_has_poll(
    user_client, user_thread, user_poll
):
    response = user_client.get(
        reverse(
            "misago:thread-poll-start",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
    )
    assert_contains(response, "This thread already has a poll.", 403)


def test_start_thread_poll_view_shows_form(user_client, user_thread):
    response = user_client.get(
        reverse(
            "misago:thread-poll-start",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
    )
    assert_contains(response, "Start poll")


@override_dynamic_settings(enable_public_polls=PublicPollsAvailability.ENABLED)
def test_start_thread_poll_view_displays_public_poll_option(user_client, user_thread):
    response = user_client.get(
        reverse(
            "misago:thread-poll-start",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
    )
    assert_contains(response, "Start poll")
    assert_contains(response, "is_public")


@override_dynamic_settings(enable_public_polls=PublicPollsAvailability.DISABLED)
def test_start_thread_poll_view_hides_public_poll_option(user_client, user_thread):
    response = user_client.get(
        reverse(
            "misago:thread-poll-start",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
    )
    assert_contains(response, "Start poll")
    assert_not_contains(response, "is_public")


def test_start_thread_poll_view_validates_poll_question(user_client, user_thread):
    response = user_client.post(
        reverse(
            "misago:thread-poll-start",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "question": "W",
            "choices_new": [
                "Great",
                "Okay",
                "About average",
                "Sad panda",
            ],
            "choices_new_noscript": "",
            "duration": "30",
            "max_choices": "2",
            "can_change_vote": "1",
            "is_public": "1",
        },
    )
    assert_contains(response, "Poll question should be at least 8 characters long")


def test_start_thread_poll_view_validates_poll_choices_are_required(
    user_client, user_thread
):
    response = user_client.post(
        reverse(
            "misago:thread-poll-start",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "question": "What's your mood?",
            "choices_new": [],
            "choices_new_noscript": "",
            "duration": "30",
            "max_choices": "2",
            "can_change_vote": "1",
            "is_public": "1",
        },
    )
    assert_contains(response, "This field is required.")


def test_start_thread_poll_view_validates_poll_choices(user_client, user_thread):
    response = user_client.post(
        reverse(
            "misago:thread-poll-start",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "question": "What's your mood?",
            "choices_new": [
                "Great",
                "OK",
                "About average",
                "Sad panda",
            ],
            "choices_new_noscript": "",
            "duration": "30",
            "max_choices": "2",
            "can_change_vote": "1",
            "is_public": "1",
        },
    )
    assert_contains(
        response, "&quot;OK&quot;: choice should be at least 3 characters long"
    )


def test_start_thread_poll_view_starts_thread_poll_using_choices_from_list(
    user_client, user, user_thread
):
    response = user_client.post(
        reverse(
            "misago:thread-poll-start",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "question": "What's your mood?",
            "choices_new": [
                "Great",
                "Okay",
                "About average",
                "Sad panda",
            ],
            "choices_new_noscript": "",
            "duration": "30",
            "max_choices": "2",
            "can_change_vote": "1",
            "is_public": "1",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": user_thread.pk, "slug": user_thread.slug}
    )

    user_thread.refresh_from_db()
    assert user_thread.has_poll

    poll = Poll.objects.get(thread=user_thread)
    assert poll.category == user_thread.category
    assert poll.thread == user_thread
    assert poll.starter == user
    assert poll.starter_name == user.username
    assert poll.starter_slug == user.slug
    assert poll.started_at
    assert poll.closed_at is None
    assert poll.question == "What's your mood?"
    assert poll.choices == [
        {
            "id": ANY,
            "name": "Great",
            "votes": 0,
        },
        {
            "id": ANY,
            "name": "Okay",
            "votes": 0,
        },
        {
            "id": ANY,
            "name": "About average",
            "votes": 0,
        },
        {
            "id": ANY,
            "name": "Sad panda",
            "votes": 0,
        },
    ]
    assert poll.duration == 30
    assert poll.max_choices == 2
    assert poll.can_change_vote
    assert poll.is_public
    assert not poll.is_closed
    assert poll.votes == 0
    assert poll.closed_by is None
    assert poll.closed_by_name is None
    assert poll.closed_by_slug is None

    choices_ids = [len(choice["id"]) for choice in poll.choices]
    assert choices_ids == [12, 12, 12, 12]


def test_start_thread_poll_view_starts_thread_poll_using_choices_from_textarea(
    user_client, user, user_thread
):
    response = user_client.post(
        reverse(
            "misago:thread-poll-start",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "question": "What's your mood?",
            "choices_new": [],
            "choices_new_noscript": "Great\nOkay\nAbout average\nSad panda",
            "duration": "30",
            "max_choices": "2",
            "can_change_vote": "1",
            "is_public": "1",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": user_thread.pk, "slug": user_thread.slug}
    )

    user_thread.refresh_from_db()
    assert user_thread.has_poll

    poll = Poll.objects.get(thread=user_thread)
    assert poll.category == user_thread.category
    assert poll.thread == user_thread
    assert poll.starter == user
    assert poll.starter_name == user.username
    assert poll.starter_slug == user.slug
    assert poll.started_at
    assert poll.closed_at is None
    assert poll.question == "What's your mood?"
    assert poll.choices == [
        {
            "id": ANY,
            "name": "Great",
            "votes": 0,
        },
        {
            "id": ANY,
            "name": "Okay",
            "votes": 0,
        },
        {
            "id": ANY,
            "name": "About average",
            "votes": 0,
        },
        {
            "id": ANY,
            "name": "Sad panda",
            "votes": 0,
        },
    ]
    assert poll.duration == 30
    assert poll.max_choices == 2
    assert poll.can_change_vote
    assert poll.is_public
    assert not poll.is_closed
    assert poll.votes == 0
    assert poll.closed_by is None
    assert poll.closed_by_name is None
    assert poll.closed_by_slug is None

    choices_ids = [len(choice["id"]) for choice in poll.choices]
    assert choices_ids == [12, 12, 12, 12]


def test_start_thread_poll_view_overrides_max_choices_with_poll_choices_number(
    user_client, user, user_thread
):
    response = user_client.post(
        reverse(
            "misago:thread-poll-start",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "question": "What's your mood?",
            "choices_new": [
                "Great",
                "Okay",
                "About average",
                "Sad panda",
            ],
            "choices_new_noscript": "",
            "duration": "30",
            "max_choices": "20",
            "can_change_vote": "1",
            "is_public": "1",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": user_thread.pk, "slug": user_thread.slug}
    )

    user_thread.refresh_from_db()
    assert user_thread.has_poll

    poll = Poll.objects.get(thread=user_thread)
    assert poll.category == user_thread.category
    assert poll.thread == user_thread
    assert poll.starter == user
    assert poll.starter_name == user.username
    assert poll.starter_slug == user.slug
    assert poll.started_at
    assert poll.closed_at is None
    assert poll.question == "What's your mood?"
    assert poll.choices == [
        {
            "id": ANY,
            "name": "Great",
            "votes": 0,
        },
        {
            "id": ANY,
            "name": "Okay",
            "votes": 0,
        },
        {
            "id": ANY,
            "name": "About average",
            "votes": 0,
        },
        {
            "id": ANY,
            "name": "Sad panda",
            "votes": 0,
        },
    ]
    assert poll.duration == 30
    assert poll.max_choices == 4
    assert poll.can_change_vote
    assert poll.is_public
    assert not poll.is_closed
    assert poll.votes == 0
    assert poll.closed_by is None
    assert poll.closed_by_name is None
    assert poll.closed_by_slug is None

    choices_ids = [len(choice["id"]) for choice in poll.choices]
    assert choices_ids == [12, 12, 12, 12]
