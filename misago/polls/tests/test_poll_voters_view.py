from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_not_contains
from ..enums import PublicPollsAvailability


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


def test_poll_voters_view_shows_guest_voters_for_poll_without_votes(
    client, thread, poll
):
    poll.is_public = True
    poll.save()

    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
    )
    assert_contains(response, poll.question)


def test_poll_voters_view_shows_user_voters_for_poll_without_votes(
    user_client, thread, poll
):
    poll.is_public = True
    poll.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
    )
    assert_contains(response, poll.question)


def test_poll_voters_view_shows_guest_voters_for_poll_without_votes_in_htmx(
    client, thread, poll
):
    poll.is_public = True
    poll.save()

    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
        headers={"hx-request": "true"},
    )
    assert_contains(response, poll.question)


def test_poll_voters_view_shows_user_voters_for_poll_without_votes_in_htmx(
    user_client, thread, poll
):
    poll.is_public = True
    poll.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
        headers={"hx-request": "true"},
    )
    assert_contains(response, poll.question)


def test_poll_voters_view_shows_guest_voters_for_poll_with_votes(
    client, other_user, thread, poll, poll_vote_factory
):
    poll.is_public = True
    poll.save()

    poll_vote_factory(poll, other_user, "choice2")

    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
    )
    assert_contains(response, poll.question)


def test_poll_voters_view_shows_user_voters_for_poll_with_votes(
    user_client, other_user, thread, poll, poll_vote_factory
):
    poll.is_public = True
    poll.save()

    poll_vote_factory(poll, other_user, "choice2")

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
    )
    assert_contains(response, poll.question)


def test_poll_voters_view_shows_guest_voters_for_poll_with_votes_in_htmx(
    client, other_user, thread, poll, poll_vote_factory
):
    poll.is_public = True
    poll.save()

    poll_vote_factory(poll, other_user, "choice2")

    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
        headers={"hx-request": "true"},
    )
    assert_contains(response, poll.question)


def test_poll_voters_view_shows_user_voters_for_poll_with_votes_in_htmx(
    user_client, other_user, thread, poll, poll_vote_factory
):
    poll.is_public = True
    poll.save()

    poll_vote_factory(poll, other_user, "choice2")

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
        headers={"hx-request": "true"},
    )
    assert_contains(response, poll.question)


def test_poll_voters_doesnt_show_vote_button_to_guest(client, thread, poll):
    poll.is_public = True
    poll.save()

    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
    )
    assert_contains(response, poll.question)
    assert_not_contains(response, "?poll=vote")


def test_poll_voters_doesnt_show_vote_button_to_guest_in_htmx(client, thread, poll):
    poll.is_public = True
    poll.save()

    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
        headers={"hx-request": "true"},
    )
    assert_contains(response, poll.question)
    assert_not_contains(response, "?poll=vote")


def test_poll_voters_shows_vote_button_to_user_who_didnt_vote(
    user_client, thread, poll
):
    poll.is_public = True
    poll.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
    )
    assert_contains(response, poll.question)
    assert_contains(response, "?poll=vote")


def test_poll_voters_shows_vote_button_to_user_who_didnt_vote_in_htmx(
    user_client, thread, poll
):
    poll.is_public = True
    poll.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
        headers={"hx-request": "true"},
    )
    assert_contains(response, poll.question)
    assert_contains(response, "?poll=vote")


def test_poll_voters_doesnt_show_vote_button_to_user_who_has_no_permission(
    user_client, members_group, thread, poll
):
    poll.is_public = True
    poll.save()

    members_group.can_vote_in_polls = False
    members_group.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
    )
    assert_contains(response, poll.question)
    assert_not_contains(response, "?poll=vote")


def test_poll_voters_doesnt_show_vote_button_to_user_who_has_no_permission_in_htmx(
    user_client, members_group, thread, poll
):
    poll.is_public = True
    poll.save()

    members_group.can_vote_in_polls = False
    members_group.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
        headers={"hx-request": "true"},
    )
    assert_contains(response, poll.question)
    assert_not_contains(response, "?poll=vote")


def test_poll_voters_doesnt_show_vote_button_to_user_who_voted(
    user_client, user, thread, poll, poll_vote_factory
):
    poll.is_public = True
    poll.save()

    poll_vote_factory(poll, user, "choice1")

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
    )
    assert_contains(response, poll.question)
    assert_not_contains(response, "?poll=vote")


def test_poll_voters_doesnt_show_vote_button_to_user_who_voted_in_htmx(
    user_client, user, thread, poll, poll_vote_factory
):
    poll.is_public = True
    poll.save()

    poll_vote_factory(poll, user, "choice1")

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
        headers={"hx-request": "true"},
    )
    assert_contains(response, poll.question)
    assert_not_contains(response, "?poll=vote")


def test_poll_voters_shows_vote_button_to_user_who_voted_if_poll_allows_vote_change(
    user_client, user, thread, poll, poll_vote_factory
):
    poll.is_public = True
    poll.save()

    poll.can_change_vote = True
    poll.save()

    poll_vote_factory(poll, user, "choice1")

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
    )
    assert_contains(response, poll.question)
    assert_contains(response, "?poll=vote")


def test_poll_voters_shows_vote_button_to_user_who_voted_if_poll_allows_vote_change_in_htmx(
    user_client, user, thread, poll, poll_vote_factory
):
    poll.is_public = True
    poll.save()

    poll.can_change_vote = True
    poll.save()

    poll_vote_factory(poll, user, "choice1")

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
        headers={"hx-request": "true"},
    )
    assert_contains(response, poll.question)
    assert_contains(response, "?poll=vote")


def test_poll_voters_shows_hide_voters_button(user_client, thread, poll):
    poll.is_public = True
    poll.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
    )
    assert_contains(response, poll.question)
    assert_contains(response, "Hide voters")
    assert_contains(response, "?poll=results")


def test_poll_voters_shows_hide_voters_button_in_htmx(user_client, thread, poll):
    poll.is_public = True
    poll.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
        headers={"hx-request": "true"},
    )
    assert_contains(response, poll.question)
    assert_contains(response, "Hide voters")
    assert_contains(response, "?poll=results")


def test_poll_voters_shows_poll_voters(
    user_client, other_user, thread, poll, poll_vote_factory
):
    poll_vote_factory(poll, other_user, "choice1")

    poll.is_public = True
    poll.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
    )
    assert_contains(response, poll.question)
    assert_contains(response, other_user.username)


def test_poll_voters_shows_poll_voters(
    user_client, other_user, thread, poll, poll_vote_factory
):
    poll_vote_factory(poll, other_user, "choice1")

    poll.is_public = True
    poll.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
        headers={"hx-request": "true"},
    )
    assert_contains(response, poll.question)
    assert_contains(response, other_user.username)


@override_dynamic_settings(enable_public_polls=PublicPollsAvailability.DISABLED)
def test_poll_voters_falls_back_to_results_if_public_polls_are_disabled(
    user_client, other_user, thread, poll, poll_vote_factory
):
    poll_vote_factory(poll, other_user, "choice1")

    poll.is_public = True
    poll.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
    )
    assert_contains(response, poll.question)
    assert_not_contains(response, "?poll=voters")
    assert_not_contains(response, other_user.username)


@override_dynamic_settings(enable_public_polls=PublicPollsAvailability.DISABLED)
def test_poll_voters_falls_back_to_results_if_public_polls_are_disabled_in_htmx(
    user_client, other_user, thread, poll, poll_vote_factory
):
    poll_vote_factory(poll, other_user, "choice1")

    poll.is_public = True
    poll.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
        headers={"hx-request": "true"},
    )
    assert_contains(response, poll.question)
    assert_not_contains(response, "?poll=voters")
    assert_not_contains(response, other_user.username)


def test_poll_voters_falls_back_to_results_if_poll_is_not_public(
    user_client, other_user, thread, poll, poll_vote_factory
):
    poll_vote_factory(poll, other_user, "choice1")

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
    )
    assert_contains(response, poll.question)
    assert_not_contains(response, "?poll=voters")
    assert_not_contains(response, other_user.username)


def test_poll_voters_falls_back_to_results_if_poll_is_not_public_in_htmx(
    user_client, other_user, thread, poll, poll_vote_factory
):
    poll_vote_factory(poll, other_user, "choice1")

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + "?poll=voters",
        headers={"hx-request": "true"},
    )
    assert_contains(response, poll.question)
    assert_not_contains(response, "?poll=voters")
    assert_not_contains(response, other_user.username)
