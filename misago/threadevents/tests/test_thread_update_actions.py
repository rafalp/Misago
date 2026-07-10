from django.urls import reverse

from ...test import assert_contains
from ..create import (
    create_added_member_thread_update,
    create_approved_thread_update,
    create_changed_owner_thread_update,
    create_changed_title_thread_update,
    create_closed_poll_thread_update,
    create_deleted_poll_thread_update,
    create_deleted_posts_thread_update,
    create_hidden_thread_update,
    create_joined_thread_update,
    create_left_thread_update,
    create_locked_thread_update,
    create_merged_thread_update,
    create_moved_posts_from_thread_update,
    create_moved_posts_to_thread_update,
    create_moved_thread_update,
    create_opened_poll_thread_update,
    create_pinned_category_thread_update,
    create_pinned_everywhere_thread_update,
    create_removed_member_thread_update,
    create_removed_reply_approval_thread_update,
    create_required_reply_approval_thread_update,
    create_split_posts_from_thread_update,
    create_split_posts_into_thread_update,
    create_started_poll_thread_update,
    create_test_thread_update,
    create_took_ownership_thread_update,
    create_unhidden_thread_update,
    create_unlocked_thread_update,
    create_unpinned_thread_update,
)


def test_create_test_thread_update(client, thread, user):
    thread_update = create_test_thread_update(thread, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, f"UPDATE [{thread_update.id}]")


def test_create_test_thread_update_with_context(client, thread, user):
    thread_update = create_test_thread_update(thread, user, "LOREM IPSUM DOLOR")

    thread.has_updates = True
    thread.save()

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

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, f"UPDATE [{thread_update.id}]")


def test_create_pinned_everywhere_thread_update(client, thread, user):
    create_pinned_everywhere_thread_update(thread, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Pinned everywhere")


def test_create_pinned_category_thread_update(client, thread, user):
    create_pinned_category_thread_update(thread, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Pinned in category")


def test_create_unpinned_thread_update(client, thread, user):
    create_unpinned_thread_update(thread, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Unpinned")


def test_create_locked_thread_update(client, thread, user):
    create_locked_thread_update(thread, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Locked")


def test_create_unlocked_thread_update(client, thread, user):
    create_unlocked_thread_update(thread, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Unlocked")


def test_create_hidden_thread_update(client, thread, user):
    create_hidden_thread_update(thread, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Hidden")


def test_create_unhidden_thread_update(client, thread, user):
    create_unhidden_thread_update(thread, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Unhidden")


def test_create_approved_thread_update(client, thread, user):
    create_approved_thread_update(thread, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Approved")


def test_create_required_reply_approval_thread_update(client, thread, user):
    create_required_reply_approval_thread_update(thread, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Required reply approval")


def test_create_removed_reply_approval_thread_update(client, thread, user):
    create_removed_reply_approval_thread_update(thread, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Removed reply approval")


def test_create_moved_thread_update(client, thread, user, default_category):
    create_moved_thread_update(thread, default_category, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Moved from")
    assert_contains(response, default_category.name)


def test_create_moved_thread_update_without_context_object(
    client, thread, user, default_category
):
    thread_update = create_moved_thread_update(thread, default_category, user)

    thread_update.clear_context_object()
    thread_update.save()

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Moved from")
    assert_contains(response, default_category.name)


def test_create_merged_thread_update(client, thread, user_thread, user):
    create_merged_thread_update(thread, user_thread, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Merged")
    assert_contains(response, "with this thread")
    assert_contains(response, user_thread.title)


def test_create_merged_thread_update_without_context_object(
    client, thread, user_thread, user
):
    thread_update = create_merged_thread_update(thread, user_thread, user)

    thread_update.clear_context_object()
    thread_update.save()

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Merged")
    assert_contains(response, "with this thread")
    assert_contains(response, user_thread.title)


def test_create_changed_title_thread_update(client, thread, user):
    create_changed_title_thread_update(thread, "Old title", user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Changed title from")
    assert_contains(response, "Old title")


def test_create_moved_posts_to_thread_update(client, thread, user_thread, user):
    create_moved_posts_to_thread_update(thread, user_thread, 21, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Moved 21 posts to")
    assert_contains(response, user_thread.title)


def test_create_moved_posts_to_thread_update_without_context_object(
    client, thread, user_thread, user
):
    thread_update = create_moved_posts_to_thread_update(thread, user_thread, 21, user)

    thread_update.clear_context_object()
    thread_update.save()

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Moved 21 posts to")
    assert_contains(response, user_thread.title)


def test_create_moved_posts_from_thread_update(client, thread, user_thread, user):
    create_moved_posts_from_thread_update(thread, user_thread, 21, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Moved 21 posts from")
    assert_contains(response, user_thread.title)


def test_create_moved_posts_from_thread_update_without_context_object(
    client, thread, user_thread, user
):
    thread_update = create_moved_posts_from_thread_update(thread, user_thread, 21, user)

    thread_update.clear_context_object()
    thread_update.save()

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Moved 21 posts from")
    assert_contains(response, user_thread.title)


def test_create_split_posts_into_thread_update(client, thread, user_thread, user):
    create_split_posts_into_thread_update(thread, user_thread, 21, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Split 21 posts into")
    assert_contains(response, user_thread.title)


def test_create_split_posts_into_thread_update_without_items(
    client, thread, user_thread, user
):
    create_split_posts_into_thread_update(thread, user_thread, actor=user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Split into")
    assert_contains(response, user_thread.title)


def test_create_split_posts_into_thread_update_without_context_object(
    client, thread, user_thread, user
):
    thread_update = create_split_posts_into_thread_update(thread, user_thread, 21, user)

    thread_update.clear_context_object()
    thread_update.save()

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Split 21 posts into")
    assert_contains(response, user_thread.title)


def test_create_split_posts_from_thread_update(client, thread, user_thread, user):
    create_split_posts_from_thread_update(thread, user_thread, 21, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Split 21 posts from")
    assert_contains(response, user_thread.title)


def test_create_split_posts_from_thread_update_without_items(
    client, thread, user_thread, user
):
    create_split_posts_from_thread_update(thread, user_thread, actor=user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Split from")
    assert_contains(response, user_thread.title)


def test_create_split_thread_update_without_context_object(
    client, thread, user_thread, user
):
    thread_update = create_split_posts_from_thread_update(thread, user_thread, 21, user)

    thread_update.clear_context_object()
    thread_update.save()

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Split 21 posts from")
    assert_contains(response, user_thread.title)


def test_create_deleted_posts_thread_update(client, thread, user):
    create_deleted_posts_thread_update(thread, 21, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Deleted 21 posts")


def test_create_started_poll_thread_update(client, thread, poll, user):
    create_started_poll_thread_update(thread, poll, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Started poll")
    assert_contains(response, poll.question)


def test_create_closed_poll_thread_update(client, thread, user):
    create_closed_poll_thread_update(thread, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Closed poll")


def test_create_opened_poll_thread_update(client, thread, user):
    create_opened_poll_thread_update(thread, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Opened poll")


def test_create_deleted_poll_thread_update(client, thread, poll, user):
    create_deleted_poll_thread_update(thread, poll, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Deleted poll")
    assert_contains(response, poll.question)


def test_create_changed_owner_thread_update(client, thread, user, other_user):
    create_changed_owner_thread_update(thread, other_user, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Changed owner to")
    assert_contains(response, other_user.username)


def test_create_changed_owner_thread_update_without_context_object(
    client, thread, user, other_user
):
    thread_update = create_changed_owner_thread_update(thread, other_user, user)

    thread_update.clear_context_object()
    thread_update.save()

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Changed owner to")
    assert_contains(response, other_user.username)


def test_create_took_ownership_thread_update(client, thread, user):
    create_took_ownership_thread_update(thread, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Took ownership")


def test_create_joined_thread_update(client, thread, user):
    create_joined_thread_update(thread, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Joined")


def test_create_left_thread_update(client, thread, user):
    create_left_thread_update(thread, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Left")


def test_create_added_member_thread_update(client, thread, user, other_user):
    create_added_member_thread_update(thread, other_user, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Added")
    assert_contains(response, other_user.username)


def test_create_invited_thread_update_without_context_object(
    client, thread, user, other_user
):
    thread_update = create_added_member_thread_update(thread, other_user, user)

    thread_update.clear_context_object()
    thread_update.save()

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Added")
    assert_contains(response, other_user.username)


def test_create_removed_member_thread_update(client, thread, user, other_user):
    create_removed_member_thread_update(thread, other_user, user)

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Removed")
    assert_contains(response, other_user.username)


def test_create_removed_member_thread_update_without_context_object(
    client, thread, user, other_user
):
    thread_update = create_removed_member_thread_update(thread, other_user, user)

    thread_update.clear_context_object()
    thread_update.save()

    thread.has_updates = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, "Removed")
    assert_contains(response, other_user.username)
