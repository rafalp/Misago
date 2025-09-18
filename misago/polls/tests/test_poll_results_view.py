from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_not_contains
from ..enums import PublicPollsAvailability


def test_poll_results_view_shows_error_if_guest_has_no_category_permission(
    client, guests_group, thread, poll
):
    CategoryGroupPermission.objects.filter(group=guests_group).delete()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
    )
    assert response.status_code == 404


def test_poll_results_view_shows_error_if_user_has_no_category_permission(
    user_client, members_group, thread, poll
):
    CategoryGroupPermission.objects.filter(group=members_group).delete()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
    )
    assert response.status_code == 404


def test_poll_results_view_shows_error_if_guest_has_no_thread_permission(
    client, thread, poll
):
    thread.is_unapproved = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
    )
    assert response.status_code == 404


def test_poll_results_view_shows_error_if_user_has_no_thread_permission(
    user_client, thread, poll
):
    thread.is_unapproved = True
    thread.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
    )
    assert response.status_code == 404


def test_poll_results_view_doesnt_show_for_guest_if_thread_has_no_poll(client, thread):
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
    )
    assert response.status_code == 200


def test_poll_results_view_shows_error_404_for_guest_if_thread_has_no_poll_in_htmx(
    client, thread
):
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_poll_results_view_doesnt_show_for_user_if_thread_has_no_poll(
    user_client, thread
):
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
    )
    assert response.status_code == 200


def test_poll_results_view_shows_error_404_for_user_if_thread_has_no_poll_in_htmx(
    user_client, thread
):
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_poll_results_view_shows_guest_results_for_poll_without_votes(
    client, thread, poll
):
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
    )
    assert_contains(response, poll.question)


def test_poll_results_view_shows_user_results_for_poll_without_votes(
    user_client, thread, poll
):
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
    )
    assert_contains(response, poll.question)


def test_poll_results_view_shows_guest_results_for_poll_without_votes_in_htmx(
    client, thread, poll
):
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
        headers={"hx-request": "true"},
    )
    assert_contains(response, poll.question)


def test_poll_results_view_shows_user_results_for_poll_without_votes_in_htmx(
    user_client, thread, poll
):
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
        headers={"hx-request": "true"},
    )
    assert_contains(response, poll.question)


def test_poll_results_view_shows_guest_results_for_poll_with_votes(
    client, other_user, thread, poll, poll_vote_factory
):
    poll_vote_factory(poll, other_user, "choice2")

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
    )
    assert_contains(response, poll.question)


def test_poll_results_view_shows_user_results_for_poll_with_votes(
    user_client, other_user, thread, poll, poll_vote_factory
):
    poll_vote_factory(poll, other_user, "choice2")

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
    )
    assert_contains(response, poll.question)


def test_poll_results_view_shows_guest_results_for_poll_with_votes_in_htmx(
    client, other_user, thread, poll, poll_vote_factory
):
    poll_vote_factory(poll, other_user, "choice2")

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
        headers={"hx-request": "true"},
    )
    assert_contains(response, poll.question)


def test_poll_results_view_shows_user_results_for_poll_with_votes_in_htmx(
    user_client, other_user, thread, poll, poll_vote_factory
):
    poll_vote_factory(poll, other_user, "choice2")

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
        headers={"hx-request": "true"},
    )
    assert_contains(response, poll.question)


def test_poll_results_doesnt_show_vote_button_to_guest(client, thread, poll):
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
    )
    assert_contains(response, poll.question)
    assert_not_contains(response, "?poll=vote")


def test_poll_results_doesnt_show_vote_button_to_guest_in_htmx(client, thread, poll):
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
        headers={"hx-request": "true"},
    )
    assert_contains(response, poll.question)
    assert_not_contains(response, "?poll=vote")


def test_poll_results_shows_vote_button_to_user_who_didnt_vote(
    user_client, thread, poll
):
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
    )
    assert_contains(response, poll.question)
    assert_contains(response, "?poll=vote")


def test_poll_results_shows_vote_button_to_user_who_didnt_vote_in_htmx(
    user_client, thread, poll
):
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
        headers={"hx-request": "true"},
    )
    assert_contains(response, poll.question)
    assert_contains(response, "?poll=vote")


def test_poll_results_doesnt_show_vote_button_to_user_who_has_no_permission(
    user_client, members_group, thread, poll
):
    members_group.can_vote_in_polls = False
    members_group.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
    )
    assert_contains(response, poll.question)
    assert_not_contains(response, "?poll=vote")


def test_poll_results_doesnt_show_vote_button_to_user_who_has_no_permission_in_htmx(
    user_client, members_group, thread, poll
):
    members_group.can_vote_in_polls = False
    members_group.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
        headers={"hx-request": "true"},
    )
    assert_contains(response, poll.question)
    assert_not_contains(response, "?poll=vote")


def test_poll_results_doesnt_show_vote_button_to_user_who_voted(
    user_client, user, thread, poll, poll_vote_factory
):
    poll_vote_factory(poll, user, "choice1")

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
    )
    assert_contains(response, poll.question)
    assert_not_contains(response, "?poll=vote")


def test_poll_results_doesnt_show_vote_button_to_user_who_voted_in_htmx(
    user_client, user, thread, poll, poll_vote_factory
):
    poll_vote_factory(poll, user, "choice1")

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
        headers={"hx-request": "true"},
    )
    assert_contains(response, poll.question)
    assert_not_contains(response, "?poll=vote")


def test_poll_results_shows_vote_button_to_user_who_voted_if_poll_allows_vote_change(
    user_client, user, thread, poll, poll_vote_factory
):
    poll.can_change_vote = True
    poll.save()

    poll_vote_factory(poll, user, "choice1")

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
    )
    assert_contains(response, poll.question)
    assert_contains(response, "?poll=vote")


def test_poll_results_shows_vote_button_to_user_who_voted_if_poll_allows_vote_change_in_htmx(
    user_client, user, thread, poll, poll_vote_factory
):
    poll.can_change_vote = True
    poll.save()

    poll_vote_factory(poll, user, "choice1")

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
        headers={"hx-request": "true"},
    )
    assert_contains(response, poll.question)
    assert_contains(response, "?poll=vote")


def test_poll_results_doesnt_show_view_voters_button_if_poll_is_not_public(
    user_client, thread, poll
):
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
    )
    assert_contains(response, poll.question)
    assert_not_contains(response, "?poll=voters")


def test_poll_results_doesnt_show_view_voters_button_if_poll_is_not_public_in_htmx(
    user_client, thread, poll
):
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
        headers={"hx-request": "true"},
    )
    assert_contains(response, poll.question)
    assert_not_contains(response, "?poll=voters")


@override_dynamic_settings(enable_public_polls=PublicPollsAvailability.DISABLED)
def test_poll_results_doesnt_show_view_voters_button_if_public_polls_are_disabled(
    user_client, thread, poll
):
    poll.is_public = True
    poll.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
    )
    assert_contains(response, poll.question)
    assert_not_contains(response, "?poll=voters")


@override_dynamic_settings(enable_public_polls=PublicPollsAvailability.DISABLED)
def test_poll_results_doesnt_show_view_voters_button_if_public_polls_are_disabled_in_htmx(
    user_client, thread, poll
):
    poll.is_public = True
    poll.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
        headers={"hx-request": "true"},
    )
    assert_contains(response, poll.question)
    assert_not_contains(response, "?poll=voters")


def test_poll_results_shows_view_voters_button_if_poll_is_public(
    user_client, thread, poll
):
    poll.is_public = True
    poll.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
    )
    assert_contains(response, poll.question)
    assert_contains(response, "?poll=voters")


def test_poll_results_shows_view_voters_button_if_poll_is_public_htmx(
    user_client, thread, poll
):
    poll.is_public = True
    poll.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
        + "?poll=results",
        headers={"hx-request": "true"},
    )
    assert_contains(response, poll.question)
    assert_contains(response, "?poll=voters")
