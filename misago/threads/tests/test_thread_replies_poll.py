from django.urls import reverse

from ...test import assert_contains, assert_not_contains


def test_thread_replies_view_displays_poll(client, thread, poll):
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug}),
    )
    assert_contains(response, thread.title)
    assert_contains(response, poll.question)
    assert_contains(response, "0 votes")
    assert_not_contains(response, "Submit vote")


def test_thread_replies_view_shows_start_poll_button_to_thread_starter_with_permission(
    user_client, user_thread
):
    response = user_client.get(
        reverse(
            "misago:thread", kwargs={"id": user_thread.id, "slug": user_thread.slug}
        ),
    )
    assert_contains(response, user_thread.title)
    assert_contains(response, "Start poll")
    assert_contains(
        response,
        reverse(
            "misago:start-thread-poll",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
    )


def test_thread_replies_view_doesnt_show_start_poll_button_to_user_with_permission_who_is_not_starter(
    user_client, thread
):
    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug}),
    )
    assert_contains(response, thread.title)
    assert_not_contains(response, "Start poll")
    assert_not_contains(
        response,
        reverse(
            "misago:start-thread-poll",
            kwargs={"id": thread.id, "slug": thread.slug},
        ),
    )


def test_thread_replies_view_doesnt_show_start_poll_button_to_thread_starter_without_permission(
    user_client, members_group, user_thread
):
    members_group.can_start_polls = False
    members_group.save()

    response = user_client.get(
        reverse(
            "misago:thread", kwargs={"id": user_thread.id, "slug": user_thread.slug}
        ),
    )
    assert_contains(response, user_thread.title)
    assert_not_contains(response, "Start poll")
    assert_not_contains(
        response,
        reverse(
            "misago:start-thread-poll",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
    )


def test_thread_replies_view_doesnt_show_start_poll_button_to_thread_starter_with_permission_if_poll_already_exists(
    user_client, user_thread, user_poll
):
    response = user_client.get(
        reverse(
            "misago:thread", kwargs={"id": user_thread.id, "slug": user_thread.slug}
        ),
    )
    assert_contains(response, user_thread.title)
    assert_contains(response, user_poll.question)
    assert_not_contains(response, "Start poll")
    assert_not_contains(
        response,
        reverse(
            "misago:start-thread-poll",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
    )
