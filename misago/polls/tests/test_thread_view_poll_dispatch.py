from datetime import timedelta

from django.urls import reverse

from ...test import assert_contains, assert_not_contains


def test_thread_view_displays_poll_results_to_guest(client, thread, poll):
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug}),
    )
    assert_contains(response, thread.title)
    assert_contains(response, poll.question)
    assert_contains(response, "0 votes")
    assert_not_contains(response, "Submit vote")


def test_thread_view_displays_single_choice_poll_vote_form_to_user(
    user_client, thread, poll
):
    poll.max_choices = 1
    poll.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug}),
    )
    assert_contains(response, thread.title)
    assert_contains(response, poll.question)
    assert_contains(response, "Submit vote")


def test_thread_view_displays_multiple_choice_poll_vote_form_to_user(
    user_client, thread, poll
):
    poll.max_choices = 2
    poll.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug}),
    )
    assert_contains(response, thread.title)
    assert_contains(response, poll.question)
    assert_contains(response, "Submit vote")


def test_thread_view_displays_poll_results_to_user_who_voted_in_poll(
    user, user_client, thread, poll, poll_vote_factory
):
    poll_vote_factory(poll, user, "choice1")

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug}),
    )
    assert_contains(response, thread.title)
    assert_contains(response, poll.question)
    assert_contains(response, "1 vote")
    assert_not_contains(response, "Submit vote")


def test_thread_view_displays_poll_results_to_user_if_poll_has_ended(
    user_client, thread, poll
):
    poll.started_at -= timedelta(days=14)
    poll.length = 5
    poll.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug}),
    )
    assert_contains(response, thread.title)
    assert_contains(response, poll.question)
    assert_contains(response, "Poll has ended")
    assert_not_contains(response, "Submit vote")


def test_thread_view_displays_poll_results_to_user_if_poll_is_closed(
    user_client, thread, closed_poll
):
    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug}),
    )
    assert_contains(response, thread.title)
    assert_contains(response, closed_poll.question)
    assert_contains(response, "Poll is closed.")
    assert_not_contains(response, "Submit vote")
