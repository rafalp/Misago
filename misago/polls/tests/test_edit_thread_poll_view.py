from unittest.mock import ANY

import pytest
from django.urls import reverse

from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_not_contains
from ..models import PollVote


def test_edit_thread_poll_view_shows_error_if_guest_has_no_category_permission(
    client, guests_group, user_thread, user_poll
):
    CategoryGroupPermission.objects.filter(group=guests_group).delete()

    response = client.get(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
    )
    assert response.status_code == 404


def test_edit_thread_poll_view_shows_error_if_guest_has_no_category_permission_in_htmx(
    client, guests_group, user_thread, user_poll
):
    CategoryGroupPermission.objects.filter(group=guests_group).delete()

    response = client.get(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
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
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
    )
    assert response.status_code == 404


def test_edit_thread_poll_view_shows_error_if_user_has_no_category_permission_in_htmx(
    user_client, members_group, user_thread, user_poll
):
    CategoryGroupPermission.objects.filter(group=members_group).delete()

    response = user_client.get(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
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
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
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
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
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
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
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
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_edit_thread_poll_view_shows_error_to_anonymous_users(
    client, user_thread, user_poll
):
    response = client.get(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
    )
    assert_contains(
        response, "You can&#x27;t edit polls in other users&#x27; threads.", 403
    )


def test_edit_thread_poll_view_shows_error_to_anonymous_users_in_htmx(
    client, user_thread, user_poll
):
    response = client.get(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
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
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
    )
    assert_contains(response, "This thread is locked", 403)


def test_edit_thread_poll_view_shows_error_if_user_has_no_edit_poll_permission_in_htmx(
    user_client, user_thread, user_poll
):
    user_thread.is_closed = True
    user_thread.save()

    response = user_client.get(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "This thread is locked", 403)


def test_edit_thread_poll_view_shows_guest_error_404_if_thread_has_no_poll(
    client, user_thread
):
    response = client.get(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
    )
    assert response.status_code == 404


def test_edit_thread_poll_view_shows_guest_error_404_if_thread_has_no_poll_in_htmx(
    client, user_thread
):
    response = client.get(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_edit_thread_poll_view_shows_user_error_404_if_thread_has_no_poll(
    user_client, user_thread
):
    response = user_client.get(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
    )
    assert response.status_code == 404


def test_edit_thread_poll_view_shows_user_error_404_if_thread_has_no_poll_in_htmx(
    user_client, user_thread
):
    response = user_client.get(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_edit_thread_poll_view_shows_edit_poll_form(
    user_client, user_thread, user_poll
):
    response = user_client.get(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
    )
    assert_contains(response, "Edit poll")


def test_edit_thread_poll_view_shows_edit_poll_form_in_htmx(
    user_client, user_thread, user_poll
):
    response = user_client.get(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Edit poll")


def test_edit_thread_poll_view_validates_poll_question(
    user_client, user_thread, user_poll
):
    data = {
        "question": "Q",
        "duration": str(user_poll.duration),
        "choices_new": [],
        "choices_new_noscript": "",
        "choices_delete": [],
        "max_choices": "1",
    }

    for choice in user_poll.choices:
        data[f'choices_edit[{choice["id"]}]'] = choice["name"]

    response = user_client.post(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        data,
    )
    assert_contains(response, "Poll question should be at least 8 characters long")


def test_edit_thread_poll_view_validates_edited_poll_choices_are_required(
    user_client, user_thread, user_poll
):
    data = {
        "question": "Edited question",
        "duration": str(user_poll.duration),
        "choices_new": [],
        "choices_new_noscript": "",
        "choices_delete": [],
        "max_choices": "1",
    }

    for choice in user_poll.choices:
        data[f'choices_edit[{choice["id"]}]'] = ""

    response = user_client.post(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        data,
    )
    assert_contains(response, "Edited poll choice can&#x27;t be empty.")


def test_edit_thread_poll_view_edits_poll_question(user_client, user_thread, user_poll):
    data = {
        "question": "Edited question",
        "duration": str(user_poll.duration),
        "choices_new": [],
        "choices_new_noscript": "",
        "choices_delete": [],
        "max_choices": "1",
    }

    for choice in user_poll.choices:
        data[f'choices_edit[{choice["id"]}]'] = choice["name"]

    response = user_client.post(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        data,
    )
    assert response.status_code == 302

    user_poll.refresh_from_db()
    assert user_poll.question == "Edited question"


def test_edit_thread_poll_view_renames_existing_choices(
    user_client, user_thread, user_poll
):
    data = {
        "question": "Edited question",
        "duration": str(user_poll.duration),
        "choices_new": [],
        "choices_new_noscript": "",
        "choices_delete": [],
        "max_choices": "1",
    }

    for votes, choice in enumerate(user_poll.choices):
        data[f'choices_edit[{choice["id"]}]'] = "Edited " + choice["name"]
        choice["votes"] = votes

    user_poll.save()

    response = user_client.post(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        data,
    )
    assert response.status_code == 302

    user_poll.refresh_from_db()
    assert user_poll.choices == [
        {
            "id": "choice1",
            "name": "Edited Yes",
            "votes": 0,
        },
        {
            "id": "choice2",
            "name": "Edited Nope",
            "votes": 1,
        },
        {
            "id": "choice3",
            "name": "Edited Maybe",
            "votes": 2,
        },
    ]


def test_edit_thread_poll_view_deletes_choice(user_client, user_thread, user_poll):
    data = {
        "question": "Edited question",
        "duration": str(user_poll.duration),
        "choices_new": [],
        "choices_new_noscript": "",
        "choices_delete": ["choice2"],
        "max_choices": "1",
    }

    for votes, choice in enumerate(user_poll.choices):
        data[f'choices_edit[{choice["id"]}]'] = "Edited " + choice["name"]
        choice["votes"] = votes

    user_poll.save()

    response = user_client.post(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        data,
    )
    assert response.status_code == 302

    user_poll.refresh_from_db()
    assert user_poll.choices == [
        {
            "id": "choice1",
            "name": "Edited Yes",
            "votes": 0,
        },
        {
            "id": "choice3",
            "name": "Edited Maybe",
            "votes": 2,
        },
    ]


def test_edit_thread_poll_view_deletes_choice_votes(
    user, other_user, user_client, user_thread, user_poll, poll_vote_factory
):
    data = {
        "question": "Edited question",
        "duration": str(user_poll.duration),
        "choices_new": [],
        "choices_new_noscript": "",
        "choices_delete": ["choice2"],
        "max_choices": "1",
    }

    kept_vote = poll_vote_factory(user_poll, user, "choice1")
    deleted_vote = poll_vote_factory(user_poll, user, "choice2")

    for votes, choice in enumerate(user_poll.choices):
        data[f'choices_edit[{choice["id"]}]'] = "Edited " + choice["name"]
        choice["votes"] = votes

    user_poll.votes = 3
    user_poll.save()

    response = user_client.post(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        data,
    )
    assert response.status_code == 302

    user_poll.refresh_from_db()
    assert user_poll.votes == 1
    assert user_poll.choices == [
        {
            "id": "choice1",
            "name": "Edited Yes",
            "votes": 0,
        },
        {
            "id": "choice3",
            "name": "Edited Maybe",
            "votes": 2,
        },
    ]

    kept_vote.refresh_from_db()

    with pytest.raises(PollVote.DoesNotExist):
        deleted_vote.refresh_from_db()


def test_edit_thread_poll_view_adds_new_choices(user_client, user_thread, user_poll):
    data = {
        "question": "Edited question",
        "duration": str(user_poll.duration),
        "choices_new": ["New", "Another"],
        "choices_new_noscript": "",
        "choices_delete": [],
        "max_choices": "1",
    }

    for votes, choice in enumerate(user_poll.choices):
        data[f'choices_edit[{choice["id"]}]'] = choice["name"]
        choice["votes"] = votes

    user_poll.save()

    response = user_client.post(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        data,
    )
    assert response.status_code == 302

    user_poll.refresh_from_db()
    assert user_poll.choices == [
        {
            "id": "choice1",
            "name": "Yes",
            "votes": 0,
        },
        {
            "id": "choice2",
            "name": "Nope",
            "votes": 1,
        },
        {
            "id": "choice3",
            "name": "Maybe",
            "votes": 2,
        },
        {
            "id": ANY,
            "name": "New",
            "votes": 0,
        },
        {
            "id": ANY,
            "name": "Another",
            "votes": 0,
        },
    ]


def test_edit_thread_poll_view_adds_new_choices_using_noscript_ui(
    user_client, user_thread, user_poll
):
    data = {
        "question": "Edited question",
        "duration": str(user_poll.duration),
        "choices_new": [],
        "choices_new_noscript": "New\nAnother",
        "choices_delete": [],
        "max_choices": "1",
    }

    for votes, choice in enumerate(user_poll.choices):
        data[f'choices_edit[{choice["id"]}]'] = choice["name"]
        choice["votes"] = votes

    user_poll.save()

    response = user_client.post(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        data,
    )
    assert response.status_code == 302

    user_poll.refresh_from_db()
    assert user_poll.choices == [
        {
            "id": "choice1",
            "name": "Yes",
            "votes": 0,
        },
        {
            "id": "choice2",
            "name": "Nope",
            "votes": 1,
        },
        {
            "id": "choice3",
            "name": "Maybe",
            "votes": 2,
        },
        {
            "id": ANY,
            "name": "New",
            "votes": 0,
        },
        {
            "id": ANY,
            "name": "Another",
            "votes": 0,
        },
    ]


def test_edit_thread_poll_view_defaults_to_new_choices_if_both_new_and_new_noscript_are_set(
    user_client, user_thread, user_poll
):
    data = {
        "question": "Edited question",
        "duration": str(user_poll.duration),
        "choices_new": ["New", "Another"],
        "choices_new_noscript": "Lorem\nIpsum",
        "choices_delete": [],
        "max_choices": "1",
    }

    for votes, choice in enumerate(user_poll.choices):
        data[f'choices_edit[{choice["id"]}]'] = choice["name"]
        choice["votes"] = votes

    user_poll.save()

    response = user_client.post(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        data,
    )
    assert response.status_code == 302

    user_poll.refresh_from_db()
    assert user_poll.choices == [
        {
            "id": "choice1",
            "name": "Yes",
            "votes": 0,
        },
        {
            "id": "choice2",
            "name": "Nope",
            "votes": 1,
        },
        {
            "id": "choice3",
            "name": "Maybe",
            "votes": 2,
        },
        {
            "id": ANY,
            "name": "New",
            "votes": 0,
        },
        {
            "id": ANY,
            "name": "Another",
            "votes": 0,
        },
    ]


def test_edit_thread_poll_view_changes_deletes_and_adds_poll_choices(
    user_client, user_thread, user_poll
):
    data = {
        "question": "Edited question",
        "duration": str(user_poll.duration),
        "choices_new": ["New"],
        "choices_new_noscript": "",
        "choices_delete": ["choice3"],
        "max_choices": "1",
    }

    for votes, choice in enumerate(user_poll.choices):
        if votes == 1:
            data[f'choices_edit[{choice["id"]}]'] = "Edited " + choice["name"]
        else:
            data[f'choices_edit[{choice["id"]}]'] = choice["name"]

        choice["votes"] = votes

    user_poll.save()

    response = user_client.post(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        data,
    )
    assert response.status_code == 302

    user_poll.refresh_from_db()
    assert user_poll.choices == [
        {
            "id": "choice1",
            "name": "Yes",
            "votes": 0,
        },
        {
            "id": "choice2",
            "name": "Edited Nope",
            "votes": 1,
        },
        {
            "id": ANY,
            "name": "New",
            "votes": 0,
        },
    ]


def test_edit_thread_poll_view_edits_poll_max_choices(
    user_client, user_thread, user_poll
):
    data = {
        "question": "Edited question",
        "duration": str(user_poll.duration),
        "choices_new": [],
        "choices_new_noscript": "",
        "choices_delete": [],
        "max_choices": "3",
    }

    for choice in user_poll.choices:
        data[f'choices_edit[{choice["id"]}]'] = choice["name"]

    response = user_client.post(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        data,
    )
    assert response.status_code == 302

    user_poll.refresh_from_db()
    assert user_poll.max_choices == 3


def test_edit_thread_poll_view_overrides_max_choices_with_poll_choices_number(
    user_client, user_thread, user_poll
):
    data = {
        "question": "Edited question",
        "duration": str(user_poll.duration),
        "choices_new": [],
        "choices_new_noscript": "",
        "choices_delete": [],
        "max_choices": "20",
    }

    for choice in user_poll.choices:
        data[f'choices_edit[{choice["id"]}]'] = choice["name"]

    response = user_client.post(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        data,
    )
    assert response.status_code == 302

    user_poll.refresh_from_db()
    assert user_poll.max_choices == 3


def test_edit_thread_poll_view_enables_vote_change(user_client, user_thread, user_poll):
    data = {
        "question": "Edited question",
        "duration": str(user_poll.duration),
        "choices_new": [],
        "choices_new_noscript": "",
        "choices_delete": [],
        "max_choices": "3",
        "can_change_vote": "1",
    }

    for choice in user_poll.choices:
        data[f'choices_edit[{choice["id"]}]'] = choice["name"]

    response = user_client.post(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        data,
    )
    assert response.status_code == 302

    user_poll.refresh_from_db()
    assert user_poll.can_change_vote


def test_edit_thread_poll_view_disables_vote_change(
    user_client, user_thread, user_poll
):
    user_poll.can_change_vote = True
    user_poll.save()

    data = {
        "question": "Edited question",
        "duration": str(user_poll.duration),
        "choices_new": [],
        "choices_new_noscript": "",
        "choices_delete": [],
        "max_choices": "3",
    }

    for choice in user_poll.choices:
        data[f'choices_edit[{choice["id"]}]'] = choice["name"]

    response = user_client.post(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        data,
    )
    assert response.status_code == 302

    user_poll.refresh_from_db()
    assert not user_poll.can_change_vote


def test_edit_thread_poll_view_returns_redirect_to_thread_on_save(
    user_client, user_thread, user_poll
):
    data = {
        "question": "Edited question",
        "duration": str(user_poll.duration),
        "choices_new": [],
        "choices_new_noscript": "",
        "choices_delete": [],
        "max_choices": "3",
    }

    for choice in user_poll.choices:
        data[f'choices_edit[{choice["id"]}]'] = choice["name"]

    response = user_client.post(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        data,
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread",
        kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
    )

    user_poll.refresh_from_db()
    assert user_poll.question == "Edited question"


def test_edit_thread_poll_view_returns_redirect_to_next_url_if_its_valid(
    user_client, user_thread, user_poll
):
    data = {
        "question": "Edited question",
        "duration": str(user_poll.duration),
        "choices_new": [],
        "choices_new_noscript": "",
        "choices_delete": [],
        "max_choices": "3",
        "next": reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug, "page": 42},
        ),
    }

    for choice in user_poll.choices:
        data[f'choices_edit[{choice["id"]}]'] = choice["name"]

    response = user_client.post(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        data,
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread",
        kwargs={"thread_id": user_thread.id, "slug": user_thread.slug, "page": 42},
    )


def test_edit_thread_poll_view_returns_redirect_to_thread_if_next_url_is_invalid(
    user_client, user_thread, user_poll
):
    data = {
        "question": "Edited question",
        "duration": str(user_poll.duration),
        "choices_new": [],
        "choices_new_noscript": "",
        "choices_delete": [],
        "max_choices": "3",
        "next": "invalid",
    }

    for choice in user_poll.choices:
        data[f'choices_edit[{choice["id"]}]'] = choice["name"]

    response = user_client.post(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        data,
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread",
        kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
    )


def test_edit_thread_poll_view_returns_vote_form_after_save_in_htmx_if_user_can_vote(
    user_client, user_thread, user_poll
):
    data = {
        "question": "Edited question",
        "duration": str(user_poll.duration),
        "choices_new": [],
        "choices_new_noscript": "",
        "choices_delete": [],
        "max_choices": "3",
    }

    for choice in user_poll.choices:
        data[f'choices_edit[{choice["id"]}]'] = choice["name"]

    response = user_client.post(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        data,
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Edited question")
    assert_contains(response, "Submit vote")


def test_edit_thread_poll_view_returns_results_after_save_in_htmx_if_user_already_voted(
    user, user_client, user_thread, user_poll, poll_vote_factory
):
    data = {
        "question": "Edited question",
        "duration": str(user_poll.duration),
        "choices_new": [],
        "choices_new_noscript": "",
        "choices_delete": [],
        "max_choices": "3",
    }

    for choice in user_poll.choices:
        data[f'choices_edit[{choice["id"]}]'] = choice["name"]

    poll_vote_factory(user_poll, user, user_poll.choices[0]["id"])

    response = user_client.post(
        reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        data,
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Edited question")
    assert_not_contains(response, "Submit vote")
