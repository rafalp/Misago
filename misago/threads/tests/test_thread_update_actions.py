from django.urls import reverse

from ...test import assert_contains
from ..threadupdates import (
    create_approved_thread_update,
    create_changed_owner_thread_update,
    create_changed_title_thread_update,
    create_hid_thread_update,
    create_invited_thread_update,
    create_joined_thread_update,
    create_left_thread_update,
    create_locked_thread_update,
    create_merged_thread_update,
    create_moved_thread_update,
    create_opened_thread_update,
    create_pinned_globally_thread_update,
    create_pinned_in_category_thread_update,
    create_removed_participants_thread_update,
    create_split_thread_update,
    create_took_ownership_thread_update,
    create_unhid_thread_update,
    create_unpinned_thread_update,
)


def test_approved_thread_update(client, thread, user):
    create_approved_thread_update(thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Approved thread")


def test_pinned_globally_thread_update(client, thread, user):
    create_pinned_globally_thread_update(thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Pinned thread globally")


def test_pinned_in_category_thread_update(client, thread, user):
    create_pinned_in_category_thread_update(thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Pinned thread in category")


def test_unpinned_thread_update(client, thread, user):
    create_unpinned_thread_update(thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Unpinned thread")


def test_locked_thread_update(client, thread, user):
    create_locked_thread_update(thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Locked thread")


def test_opened_thread_update(client, thread, user):
    create_opened_thread_update(thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Opened thread")


def test_moved_thread_update(client, thread, user, default_category):
    create_moved_thread_update(thread, default_category, user)
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Moved thread from")


def test_moved_thread_update_without_context_object(
    client, thread, user, default_category
):
    thread_update = create_moved_thread_update(thread, default_category, user)

    thread_update.clear_context_object()
    thread_update.save()

    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Moved thread from")


def test_merged_thread_update(client, thread, user_thread, user):
    create_merged_thread_update(thread, user_thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Merged")
    assert_contains(response, "with this thread")


def test_merged_thread_update_without_context_object(client, thread, user_thread, user):
    thread_update = create_merged_thread_update(thread, user_thread, user)

    thread_update.clear_context_object()
    thread_update.save()

    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Merged")
    assert_contains(response, "with this thread")


def test_split_thread_update(client, thread, user_thread, user):
    create_split_thread_update(thread, user_thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Split this thread from")


def test_split_thread_update_without_context_object(client, thread, user_thread, user):
    thread_update = create_split_thread_update(thread, user_thread, user)

    thread_update.clear_context_object()
    thread_update.save()

    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Split this thread from")


def test_hid_thread_update(client, thread, user):
    create_hid_thread_update(thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Hid thread")


def test_unhid_thread_update(client, thread, user):
    create_unhid_thread_update(thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Unhid thread")


def test_changed_owner_thread_update(client, thread, user, other_user):
    create_changed_owner_thread_update(thread, other_user, user)
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Changed thread owner")


def test_changed_owner_thread_update_without_context_object(
    client, thread, user, other_user
):
    thread_update = create_changed_owner_thread_update(thread, other_user, user)

    thread_update.clear_context_object()
    thread_update.save()

    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Changed thread owner")


def test_took_ownership_thread_update(client, thread, user):
    create_took_ownership_thread_update(thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Took thread ownership")


def test_joined_thread_update(client, thread, user):
    create_joined_thread_update(thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Joined thread")


def test_invited_thread_update(client, thread, user, other_user):
    create_invited_thread_update(thread, other_user, user)
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Invited")


def test_invited_thread_update_without_context_object(client, thread, user, other_user):
    thread_update = create_invited_thread_update(thread, other_user, user)

    thread_update.clear_context_object()
    thread_update.save()

    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Invited")


def test_left_thread_update(client, thread, user):
    create_left_thread_update(thread, user)
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Left thread")


def test_removed_participants_thread_update(client, thread, user, other_user):
    create_removed_participants_thread_update(thread, other_user, user)
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Removed")


def test_removed_participants_thread_update_without_context_object(
    client, thread, user, other_user
):
    thread_update = create_removed_participants_thread_update(thread, other_user, user)

    thread_update.clear_context_object()
    thread_update.save()

    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Removed")


def test_changed_owner_thread_update(client, thread, user, other_user):
    create_changed_owner_thread_update(thread, other_user, user)
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Changed thread owner to")


def test_changed_owner_thread_update_without_context_object(
    client, thread, user, other_user
):
    thread_update = create_changed_owner_thread_update(thread, other_user, user)

    thread_update.clear_context_object()
    thread_update.save()

    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Changed thread owner to")
