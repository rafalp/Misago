from django.urls import reverse

from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_has_error_message, assert_not_contains
from ..votes import get_user_poll_votes


def test_poll_vote_view_shows_error_if_guest_has_no_category_permission(
    client, guests_group, thread, poll
):
    CategoryGroupPermission.objects.filter(group=guests_group).delete()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
    )
    assert response.status_code == 404


def test_poll_vote_view_shows_error_if_user_has_no_category_permission(
    user_client, members_group, thread, poll
):
    CategoryGroupPermission.objects.filter(group=members_group).delete()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
    )
    assert response.status_code == 404


def test_poll_vote_view_shows_error_if_guest_has_no_thread_permission(
    client, thread, poll
):
    thread.is_unapproved = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
    )
    assert response.status_code == 404


def test_poll_vote_view_shows_error_if_user_has_no_thread_permission(
    user_client, thread, poll
):
    thread.is_unapproved = True
    thread.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
    )
    assert response.status_code == 404


def test_poll_vote_view_doesnt_show_for_guest_if_thread_has_no_poll(client, thread):
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
    )
    assert_not_contains(response, "Submit vote")


def test_poll_vote_view_doesnt_show_for_user_if_thread_has_no_poll(user_client, thread):
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
    )
    assert_not_contains(response, "Submit vote")


def test_poll_vote_view_shows_error_404_for_guest_if_thread_has_no_poll_in_htmx(
    client, thread
):
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_poll_vote_view_shows_error_404_for_user_if_thread_has_no_poll_in_htmx(
    user_client, thread
):
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_poll_vote_view_doesnt_show_for_guest_if_they_have_no_permission(
    client, thread, poll
):
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
    )
    assert_not_contains(response, "Submit vote")


def test_poll_vote_view_doesnt_show_for_user_if_they_have_no_permission(
    user_client, members_group, thread, poll
):
    members_group.can_vote_in_polls = False
    members_group.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
    )
    assert_not_contains(response, "Submit vote")


def test_poll_vote_view_shows_error_403_for_guest_in_htmx(client, thread, poll):
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "You must be signed in to vote in polls.", 403)


def test_poll_vote_view_post_shows_error_if_guest_has_no_category_permission(
    client, guests_group, thread, poll
):
    CategoryGroupPermission.objects.filter(group=guests_group).delete()

    response = client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
        {"poll_choice": "choice1"},
    )
    assert response.status_code == 404


def test_poll_vote_view_post_shows_error_if_user_has_no_category_permission(
    user_client, members_group, thread, poll
):
    CategoryGroupPermission.objects.filter(group=members_group).delete()

    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
        {"poll_choice": "choice1"},
    )
    assert response.status_code == 404


def test_poll_vote_view_post_shows_error_if_guest_has_no_thread_permission(
    client, thread, poll
):
    thread.is_unapproved = True
    thread.save()

    response = client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
        {"poll_choice": "choice1"},
    )
    assert response.status_code == 404


def test_poll_vote_view_post_shows_error_if_user_has_no_thread_permission(
    user_client, thread, poll
):
    thread.is_unapproved = True
    thread.save()

    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
        {"poll_choice": "choice1"},
    )
    assert response.status_code == 404


def test_poll_vote_view_post_vote_shows_error_404_for_guest_if_thread_has_no_poll(
    client, thread
):
    response = client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
        {"poll_choice": "choice1"},
    )
    assert response.status_code == 404


def test_poll_vote_view_post_vote_shows_error_403_for_guest(client, thread, poll):
    response = client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
        {"poll_choice": "choice1"},
    )
    assert_contains(response, "You must be signed in to vote in polls.", 403)


def test_poll_vote_view_post_vote_shows_error_404_for_user_if_thread_has_no_poll(
    user_client, thread
):
    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
        {"poll_choice": "choice1"},
    )
    assert response.status_code == 404


def test_poll_vote_view_post_vote_shows_error_403_for_user_if_they_have_no_permission(
    user_client, members_group, thread, poll
):
    members_group.can_vote_in_polls = False
    members_group.save()

    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
        {"poll_choice": "choice1"},
    )
    assert_contains(response, "You can&#x27;t vote in polls.", 403)


def test_poll_vote_view_post_vote_shows_validation_error_message_for_user_if_they_made_invalid_vote(
    user_client, thread, poll
):
    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
    )
    assert response.status_code == 302
    assert_has_error_message(response, "Select a choice.")


def test_poll_vote_view_post_vote_shows_validation_error_message_for_user_if_they_made_invalid_vote_in_htmx(
    user_client, thread, poll
):
    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Select a choice.", 200)


def test_poll_vote_view_post_vote_saves_user_vote_and_redirects_them_to_thread(
    user_client, user, thread, poll
):
    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
        {"poll_choice": ["choice1"]},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    poll.refresh_from_db()
    assert poll.votes == 1

    assert get_user_poll_votes(user, poll) == {"choice1"}


def test_poll_vote_view_post_vote_saves_user_vote_and_redirects_them_to_next_url(
    user_client, user, thread, poll
):
    next_url = reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug, "page": 2}
    )

    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
        {"poll_choice": ["choice1"], "next": next_url},
    )
    assert response.status_code == 302
    assert response["location"] == next_url

    poll.refresh_from_db()
    assert poll.votes == 1

    assert get_user_poll_votes(user, poll) == {"choice1"}


def test_poll_vote_view_post_vote_saves_user_vote_and_redirects_them_to_thread_if_next_url_is_invalid(
    user_client, user, thread, poll
):
    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
        {"poll_choice": ["choice1"], "next": "invalid"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    poll.refresh_from_db()
    assert poll.votes == 1

    assert get_user_poll_votes(user, poll) == {"choice1"}


def test_poll_vote_view_post_vote_saves_user_vote_and_displays_results_in_htmx(
    user_client, user, thread, poll
):
    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
        {"poll_choice": ["choice1"]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "1 vote")

    poll.refresh_from_db()
    assert poll.votes == 1

    assert get_user_poll_votes(user, poll) == {"choice1"}


def test_poll_vote_view_post_vote_shows_error_403_for_user_if_they_already_voted_and_vote_change_is_disabled(
    user_client, user, thread, poll, poll_vote_factory
):
    poll_vote_factory(poll, user, "choice1")

    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
    )
    assert_contains(response, "This poll doesn&#x27;t allow vote changes.", 403)


def test_poll_vote_view_post_vote_shows_error_403_for_user_if_they_already_voted_and_vote_change_is_disabled_in_htmx(
    user_client, user, thread, poll, poll_vote_factory
):
    poll_vote_factory(poll, user, "choice1")

    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "allow vote changes.", 403)


def test_poll_vote_view_post_vote_shows_validation_error_message_for_user_if_they_made_invalid_vote_change(
    user_client, user, thread, poll, poll_vote_factory
):
    poll.can_change_vote = True
    poll.save()

    poll_vote_factory(poll, user, "choice1")

    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
    )
    assert response.status_code == 302
    assert_has_error_message(response, "Select a choice.")


def test_poll_vote_view_post_vote_shows_validation_error_message_for_user_if_they_made_invalid_vote_change_in_htmx(
    user_client, user, thread, poll, poll_vote_factory
):
    poll.can_change_vote = True
    poll.save()

    poll_vote_factory(poll, user, "choice1")

    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Select a choice.", 200)


def test_poll_vote_view_post_vote_changes_user_vote(
    user_client, user, thread, poll, poll_vote_factory
):
    poll.can_change_vote = True
    poll.save()

    poll_vote_factory(poll, user, "choice1")

    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
        {"poll_choice": ["choice3"]},
    )
    assert response.status_code == 302

    poll.refresh_from_db()
    assert poll.votes == 1

    assert get_user_poll_votes(user, poll) == {"choice3"}


def test_poll_vote_view_post_vote_changes_user_vote_in_htmx(
    user_client, user, thread, poll, poll_vote_factory
):
    poll.can_change_vote = True
    poll.save()

    poll_vote_factory(poll, user, "choice1")

    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=vote",
        {"poll_choice": ["choice3"]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "1 vote")

    poll.refresh_from_db()
    assert poll.votes == 1

    assert get_user_poll_votes(user, poll) == {"choice3"}
