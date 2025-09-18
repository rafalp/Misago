from django.urls import reverse

from ...test import assert_contains
from ..create import (
    create_added_member_thread_update,
    create_approved_thread_update,
    create_changed_owner_thread_update,
    create_changed_title_thread_update,
    create_closed_poll_thread_update,
    create_deleted_poll_thread_update,
    create_hid_thread_update,
    create_joined_thread_update,
    create_left_thread_update,
    create_locked_thread_update,
    create_merged_thread_update,
    create_moved_thread_update,
    create_opened_poll_thread_update,
    create_opened_thread_update,
    create_pinned_globally_thread_update,
    create_pinned_in_category_thread_update,
    create_removed_member_thread_update,
    create_split_thread_update,
    create_started_poll_thread_update,
    create_test_thread_update,
    create_took_ownership_thread_update,
    create_unhid_thread_update,
    create_unpinned_thread_update,
)


def test_create_test_thread_update(client, thread, user):
    thread_update = create_test_thread_update(thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, f"UPDATE [{thread_update.id}]")


def test_create_test_thread_update_with_context(client, thread, user):
    thread_update = create_test_thread_update(thread, user, "LOREM IPSUM DOLOR")
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, f"UPDATE [{thread_update.id}]")
    assert_contains(response, "LOREM IPSUM DOLOR")


def test_create_test_thread_update_with_context_object(
    client, thread, user, default_category
):
    thread_update = create_test_thread_update(
        thread, user, context_object=default_category
    )
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, f"UPDATE [{thread_update.id}]")


def test_approved_thread_update(client, thread, user):
    create_approved_thread_update(thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Approved thread")


def test_pinned_globally_thread_update(client, thread, user):
    create_pinned_globally_thread_update(thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Pinned thread globally")


def test_pinned_in_category_thread_update(client, thread, user):
    create_pinned_in_category_thread_update(thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Pinned thread in category")


def test_unpinned_thread_update(client, thread, user):
    create_unpinned_thread_update(thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Unpinned thread")


def test_locked_thread_update(client, thread, user):
    create_locked_thread_update(thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Locked thread")


def test_opened_thread_update(client, thread, user):
    create_opened_thread_update(thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Opened thread")


def test_moved_thread_update(client, thread, user, default_category):
    create_moved_thread_update(thread, default_category, user)
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Moved thread from")
    assert_contains(response, default_category.name)


def test_moved_thread_update_without_context_object(
    client, thread, user, default_category
):
    thread_update = create_moved_thread_update(thread, default_category, user)

    thread_update.clear_context_object()
    thread_update.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Moved thread from")
    assert_contains(response, default_category.name)


def test_merged_thread_update(client, thread, user_thread, user):
    create_merged_thread_update(thread, user_thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Merged")
    assert_contains(response, "with this thread")
    assert_contains(response, user_thread.title)


def test_merged_thread_update_without_context_object(client, thread, user_thread, user):
    thread_update = create_merged_thread_update(thread, user_thread, user)

    thread_update.clear_context_object()
    thread_update.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Merged")
    assert_contains(response, "with this thread")
    assert_contains(response, user_thread.title)


def test_split_thread_update(client, thread, user_thread, user):
    create_split_thread_update(thread, user_thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Split this thread from")
    assert_contains(response, user_thread.title)


def test_split_thread_update_without_context_object(client, thread, user_thread, user):
    thread_update = create_split_thread_update(thread, user_thread, user)

    thread_update.clear_context_object()
    thread_update.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Split this thread from")
    assert_contains(response, user_thread.title)


def test_hid_thread_update(client, thread, user):
    create_hid_thread_update(thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Hid thread")


def test_unhid_thread_update(client, thread, user):
    create_unhid_thread_update(thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Unhid thread")


def test_changed_title_thread_update(client, thread, user):
    create_changed_title_thread_update(thread, "Old title", user)
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Changed thread title from")
    assert_contains(response, "Old title")


def test_create_started_poll_thread_update(client, thread, poll, user):
    create_started_poll_thread_update(thread, poll, user)
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Started poll")
    assert_contains(response, poll.question)


def test_create_closed_poll_thread_update(client, thread, user):
    create_closed_poll_thread_update(thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Closed poll")


def test_create_opened_poll_thread_update(client, thread, user):
    create_opened_poll_thread_update(thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Opened poll")


def test_create_deleted_poll_thread_update(client, thread, poll, user):
    create_deleted_poll_thread_update(thread, poll, user)
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Deleted poll")
    assert_contains(response, poll.question)


def test_changed_owner_thread_update(client, thread, user, other_user):
    create_changed_owner_thread_update(thread, other_user, user)
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Changed thread owner to")
    assert_contains(response, other_user.username)


def test_changed_owner_thread_update_without_context_object(
    client, thread, user, other_user
):
    thread_update = create_changed_owner_thread_update(thread, other_user, user)

    thread_update.clear_context_object()
    thread_update.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Changed thread owner to")
    assert_contains(response, other_user.username)


def test_took_ownership_thread_update(client, thread, user):
    create_took_ownership_thread_update(thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Took thread ownership")


def test_joined_thread_update(client, thread, user):
    create_joined_thread_update(thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Joined thread")


def test_left_thread_update(client, thread, user):
    create_left_thread_update(thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Left thread")


def test_added_member_thread_update(client, thread, user, other_user):
    create_added_member_thread_update(thread, other_user, user)
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Added")
    assert_contains(response, other_user.username)


def test_invited_thread_update_without_context_object(client, thread, user, other_user):
    thread_update = create_added_member_thread_update(thread, other_user, user)

    thread_update.clear_context_object()
    thread_update.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Added")
    assert_contains(response, other_user.username)


def test_removed_member_thread_update(client, thread, user, other_user):
    create_removed_member_thread_update(thread, other_user, user)
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Removed")
    assert_contains(response, other_user.username)


def test_removed_member_thread_update_without_context_object(
    client, thread, user, other_user
):
    thread_update = create_removed_member_thread_update(thread, other_user, user)

    thread_update.clear_context_object()
    thread_update.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Removed")
    assert_contains(response, other_user.username)
