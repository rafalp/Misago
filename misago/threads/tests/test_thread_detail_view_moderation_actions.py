import pytest
from django.urls import reverse

from ...permissions.enums import CategoryPermission
from ...permissions.models import Moderator
from ...polls.models import Poll
from ...postedits.models import PostEdit
from ...solutions.select import select_thread_solution
from ...test import UNORDERED, assert_contains, assert_not_contains
from ...testutils import grant_category_group_permissions
from ...threadupdates.enums import ThreadUpdateActionName
from ...threadupdates.models import ThreadUpdate
from ..enums import ThreadPinned
from ..models import Post, Thread


@pytest.fixture
def mock_thread_synchronize_categories(mocker):
    return mocker.patch("misago.moderation.thread.synchronize_categories")


@pytest.fixture
def mock_delete_duplicate_watched_threads(mocker):
    return mocker.patch("misago.moderation.thread.delete_duplicate_watched_threads")


@pytest.fixture
def mock_posts_synchronize_categories(mocker):
    return mocker.patch("misago.moderation.posts.synchronize_categories")


@pytest.fixture
def mock_posts_notify_on_new_thread_reply(mocker):
    return mocker.patch("misago.moderation.posts.notify_on_new_thread_reply")


@pytest.fixture
def mock_post_synchronize_categories(mocker):
    return mocker.patch("misago.moderation.post.synchronize_categories")


@pytest.fixture
def mock_post_notify_on_new_thread_reply(mocker):
    return mocker.patch("misago.moderation.post.notify_on_new_thread_reply")


def test_thread_detail_view_pin_everywhere_thread_moderation_action_pins_unpinned_thread(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "pin_everywhere"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.EVERYWHERE
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.PINNED_EVERYWHERE,
    )


def test_thread_detail_view_pin_everywhere_thread_moderation_action_pins_pinned_category_thread(
    moderator_client, thread
):
    thread.pinned = ThreadPinned.CATEGORY
    thread.save()

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "pin_everywhere"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.EVERYWHERE
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.PINNED_EVERYWHERE,
    )


def test_thread_detail_view_pin_category_thread_moderation_action_pins_unpinned_thread(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "pin_category"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.CATEGORY
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.PINNED_CATEGORY,
    )


def test_thread_detail_view_pin_category_thread_moderation_action_pins_pinned_everywhere_thread(
    moderator_client, thread
):
    thread.pinned = ThreadPinned.EVERYWHERE
    thread.save()

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "pin_category"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.CATEGORY
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.PINNED_CATEGORY,
    )


def test_thread_detail_view_unpin_thread_moderation_action_unpins_pinned_everywhere_thread(
    moderator_client, thread
):
    thread.pinned = ThreadPinned.EVERYWHERE
    thread.save()

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "unpin"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.NONE
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.UNPINNED,
    )


def test_thread_detail_view_unpin_thread_moderation_action_unpins_pinned_category_thread(
    moderator_client, thread
):
    thread.pinned = ThreadPinned.CATEGORY
    thread.save()

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "unpin"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.NONE
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.UNPINNED,
    )


def test_thread_detail_view_lock_thread_moderation_action_locks_thread(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "lock"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.is_locked
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.LOCKED,
    )


def test_thread_detail_view_unlock_thread_moderation_action_unlocks_thread(
    moderator_client, thread
):
    thread.is_locked = True
    thread.save()

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "unlock"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert not thread.is_locked
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.UNLOCKED,
    )


def test_thread_detail_view_hide_thread_moderation_action_hides_thread(
    moderator_client, moderator, thread, mock_thread_synchronize_categories
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "hide"},
    )
    assert_contains(response, "Hide thread")
    assert_contains(response, "Reason for hiding")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "hide",
            "moderation-hidden_reason": "Lorem ipsum",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.is_hidden
    assert thread.hidden_at
    assert thread.hidden_by == moderator
    assert thread.hidden_by_name == moderator.username
    assert thread.hidden_by_slug == moderator.slug
    assert thread.hidden_reason == "Lorem ipsum"
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.HIDDEN,
    )

    mock_thread_synchronize_categories.delay.assert_called_once_with(
        [thread.category_id]
    )


def test_thread_detail_view_unhide_thread_moderation_action_unhides_thread(
    moderator_client, thread, mock_thread_synchronize_categories
):
    thread.is_hidden = True
    thread.save()

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "unhide"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert not thread.is_hidden
    assert thread.hidden_at is None
    assert thread.hidden_by is None
    assert thread.hidden_by_name is None
    assert thread.hidden_by_slug is None
    assert thread.hidden_reason is None
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.UNHIDDEN,
    )

    mock_thread_synchronize_categories.delay.assert_called_once_with(
        [thread.category_id]
    )


def test_thread_detail_view_approve_thread_moderation_action_approves_thread(
    moderator_client, thread, mock_thread_synchronize_categories
):
    thread.is_unapproved = True
    thread.save()

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "approve"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert not thread.is_unapproved
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.APPROVED,
    )

    mock_thread_synchronize_categories.delay.assert_called_once_with(
        [thread.category_id]
    )


def test_thread_detail_view_require_reply_approval_thread_moderation_action_sets_thread_require_reply_approval_flag(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "require_reply_approval"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.require_reply_approval
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.REQUIRED_REPLY_APPROVAL,
    )


def test_thread_detail_view_remove_reply_approval_thread_moderation_action_removes_thread_require_reply_approval_flag(
    moderator_client, thread
):
    thread.require_reply_approval = True
    thread.save()

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "remove_reply_approval"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert not thread.require_reply_approval
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.REMOVED_REPLY_APPROVAL,
    )


def test_thread_detail_view_move_thread_moderation_action_moves_thread(
    thread_factory,
    moderator_client,
    moderators_group,
    default_category,
    sibling_category,
    mock_thread_synchronize_categories,
):
    grant_category_group_permissions(
        sibling_category,
        moderators_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
        CategoryPermission.START,
    )

    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "move"},
    )
    assert_contains(response, "Move thread")
    assert_contains(response, "Category")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "move",
            "moderation-category": sibling_category.id,
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.category == sibling_category
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.MOVED,
    )

    mock_thread_synchronize_categories.delay.assert_called_once_with(
        UNORDERED([default_category.id, sibling_category.id])
    )


def test_thread_detail_view_move_thread_moderation_action_requires_category(
    thread_factory,
    moderator_client,
    default_category,
    mock_thread_synchronize_categories,
):
    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "move"},
    )
    assert_contains(response, "Move thread")
    assert_contains(response, "Category")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "move",
            "confirm": "true",
        },
    )
    assert_contains(response, "This field is required.")

    thread.refresh_from_db()
    assert thread.category == default_category
    assert not thread.has_updates

    assert not ThreadUpdate.objects.exists()

    mock_thread_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_move_thread_moderation_action_validates_category_value(
    thread_factory,
    moderator_client,
    default_category,
    mock_thread_synchronize_categories,
):
    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "move"},
    )
    assert_contains(response, "Move thread")
    assert_contains(response, "Category")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "move",
            "moderation-category": "invalid",
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    thread.refresh_from_db()
    assert thread.category == default_category
    assert not thread.has_updates

    assert not ThreadUpdate.objects.exists()

    mock_thread_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_move_thread_moderation_action_validates_category_browse_permission(
    thread_factory,
    moderator_client,
    moderators_group,
    default_category,
    sibling_category,
    mock_thread_synchronize_categories,
):
    grant_category_group_permissions(
        sibling_category,
        moderators_group,
        CategoryPermission.SEE,
    )

    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "move"},
    )
    assert_contains(response, "Move thread")
    assert_contains(response, "Category")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "move",
            "moderation-category": sibling_category.id,
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    thread.refresh_from_db()
    assert thread.category == default_category
    assert not thread.has_updates

    assert not ThreadUpdate.objects.exists()

    mock_thread_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_move_thread_moderation_action_validates_category_moderator_permission(
    thread_factory,
    user_client,
    user,
    members_group,
    default_category,
    sibling_category,
    mock_thread_synchronize_categories,
):
    grant_category_group_permissions(
        sibling_category,
        members_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    thread = thread_factory(default_category, is_unapproved=True)

    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "move"},
    )
    assert_contains(response, "Move thread")
    assert_contains(response, "Category")

    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "move",
            "moderation-category": sibling_category.id,
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    thread.refresh_from_db()
    assert thread.category == default_category
    assert not thread.has_updates

    assert not ThreadUpdate.objects.exists()

    mock_thread_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_move_thread_moderation_action_validates_category_type(
    thread_factory,
    moderator_client,
    moderators_group,
    default_category,
    sibling_category,
    mock_thread_synchronize_categories,
):
    grant_category_group_permissions(
        sibling_category,
        moderators_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
        CategoryPermission.START,
    )

    sibling_category.is_vanilla = True
    sibling_category.save()

    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "move"},
    )
    assert_contains(response, "Move thread")
    assert_contains(response, "Category")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "move",
            "moderation-category": sibling_category.id,
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    thread.refresh_from_db()
    assert thread.category == default_category
    assert not thread.has_updates

    assert not ThreadUpdate.objects.exists()

    mock_thread_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_move_thread_moderation_action_validates_category_is_new(
    thread_factory,
    moderator_client,
    default_category,
    mock_thread_synchronize_categories,
):
    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "move"},
    )
    assert_contains(response, "Move thread")
    assert_contains(response, "Category")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "move",
            "moderation-category": default_category.id,
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    thread.refresh_from_db()
    assert thread.category == default_category
    assert not thread.has_updates

    assert not ThreadUpdate.objects.exists()

    mock_thread_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_merge_thread_moderation_action_merges_current_thread_into_other(
    moderator_client,
    default_category,
    thread,
    other_thread,
    mock_thread_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
    )
    assert_contains(response, "Merge thread")
    assert_contains(response, "Other thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "merge",
            "moderation-other_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-direction": "other",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
        )
        + f"#post-{other_thread.last_post_id}"
    )

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()

    other_thread.refresh_from_db()
    assert other_thread.replies == 1

    assert (
        ThreadUpdate.objects.filter(
            thread=other_thread,
            action=ThreadUpdateActionName.MERGED,
        ).count()
        == 1
    )

    mock_thread_synchronize_categories.delay.assert_called_once_with(
        [default_category.id]
    )
    mock_delete_duplicate_watched_threads.delay.assert_called_once_with(other_thread.id)


def test_thread_detail_view_merge_thread_moderation_action_merges_current_thread_into_other_in_htmx(
    moderator_client,
    default_category,
    thread,
    other_thread,
    mock_thread_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Other thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "merge",
            "moderation-other_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-direction": "other",
            "confirm": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 201
    assert (
        response["hx-redirect"]
        == reverse(
            "misago:thread",
            kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
        )
        + f"#post-{other_thread.last_post_id}"
    )

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()

    other_thread.refresh_from_db()
    assert other_thread.replies == 1

    assert (
        ThreadUpdate.objects.filter(
            thread=other_thread,
            action=ThreadUpdateActionName.MERGED,
        ).count()
        == 1
    )

    mock_thread_synchronize_categories.delay.assert_called_once_with(
        [default_category.id]
    )
    mock_delete_duplicate_watched_threads.delay.assert_called_once_with(other_thread.id)


def test_thread_detail_view_merge_thread_moderation_action_merges_other_thread_into_current(
    moderator_client,
    default_category,
    thread,
    other_thread,
    mock_thread_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
    )
    assert_contains(response, "Merge thread")
    assert_contains(response, "Other thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "merge",
            "moderation-other_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-direction": "current",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    with pytest.raises(Thread.DoesNotExist):
        other_thread.refresh_from_db()

    thread.refresh_from_db()
    assert thread.replies == 1

    assert (
        ThreadUpdate.objects.filter(
            thread=thread,
            action=ThreadUpdateActionName.MERGED,
        ).count()
        == 1
    )

    mock_thread_synchronize_categories.delay.assert_called_once_with(
        [default_category.id]
    )
    mock_delete_duplicate_watched_threads.delay.assert_called_once_with(thread.id)


def test_thread_detail_view_merge_thread_moderation_action_merges_other_thread_into_current_in_htmx(
    moderator_client,
    default_category,
    thread,
    other_thread,
    mock_thread_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Other thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "merge",
            "moderation-other_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-direction": "current",
            "confirm": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 201
    assert response["hx-refresh"] == "true"

    with pytest.raises(Thread.DoesNotExist):
        other_thread.refresh_from_db()

    thread.refresh_from_db()
    assert thread.replies == 1

    assert (
        ThreadUpdate.objects.filter(
            thread=thread,
            action=ThreadUpdateActionName.MERGED,
        ).count()
        == 1
    )

    mock_thread_synchronize_categories.delay.assert_called_once_with(
        [default_category.id]
    )
    mock_delete_duplicate_watched_threads.delay.assert_called_once_with(thread.id)


def test_thread_detail_view_merge_thread_moderation_action_merges_threads_without_conflicts(
    thread_reply_factory,
    poll_factory,
    moderator_client,
    default_category,
    thread,
    other_thread,
    mock_thread_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    solution = thread_reply_factory(thread, poster="Answer")
    select_thread_solution(thread, solution, user="JohnDoe")

    poll = poll_factory(other_thread)

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
    )
    assert_contains(response, "Merge thread")
    assert_contains(response, "Other thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "merge",
            "moderation-other_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-direction": "other",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
        )
        + f"#post-{solution.id}"
    )

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()

    other_thread.refresh_from_db()
    assert other_thread.replies == 2
    assert other_thread.solution == solution

    poll.refresh_from_db()
    assert poll.thread == other_thread

    assert (
        ThreadUpdate.objects.filter(
            thread=other_thread,
            action=ThreadUpdateActionName.MERGED,
        ).count()
        == 1
    )

    mock_thread_synchronize_categories.delay.assert_called_once_with(
        [default_category.id]
    )
    mock_delete_duplicate_watched_threads.delay.assert_called_once_with(other_thread.id)


def test_thread_detail_view_merge_thread_moderation_action_merges_threads_with_conflicts(
    thread_reply_factory,
    poll_factory,
    moderator_client,
    default_category,
    thread,
    other_thread,
    mock_thread_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    thread_solution = thread_reply_factory(thread, poster="Answer")
    other_thread_solution = thread_reply_factory(other_thread, poster="Answer")

    select_thread_solution(thread, thread_solution, user="JohnDoe")
    select_thread_solution(other_thread, other_thread_solution, user="JohnDoe")

    thread_poll = poll_factory(thread)
    other_thread_poll = poll_factory(other_thread)

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
    )
    assert_contains(response, "Merge thread")
    assert_contains(response, "Other thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "merge",
            "moderation-other_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-direction": "other",
            "confirm": "true",
        },
    )
    assert_contains(response, "Solution")
    assert_contains(response, "Poll")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "merge",
            "moderation-other_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-direction": "other",
            "moderation-solution": thread.id,
            "moderation-poll": thread_poll.id,
            "confirm": "true",
            "confirm_conflicts": "true",
        },
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
        )
        + f"#post-{other_thread_solution.id}"
    )

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()

    other_thread.refresh_from_db()
    assert other_thread.replies == 3
    assert other_thread.solution == thread_solution

    thread_poll.refresh_from_db()
    assert thread_poll.thread == other_thread

    with pytest.raises(Poll.DoesNotExist):
        other_thread_poll.refresh_from_db()

    assert (
        ThreadUpdate.objects.filter(
            thread=other_thread,
            action=ThreadUpdateActionName.MERGED,
        ).count()
        == 1
    )

    mock_thread_synchronize_categories.delay.assert_called_once_with(
        [default_category.id]
    )
    mock_delete_duplicate_watched_threads.delay.assert_called_once_with(other_thread.id)


def test_thread_detail_view_merge_thread_moderation_action_requires_other_thread_link(
    moderator_client,
    thread,
    other_thread,
    mock_thread_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
    )
    assert_contains(response, "Merge thread")
    assert_contains(response, "Other thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "merge",
            "moderation-direction": "this",
            "confirm": "true",
        },
    )
    assert_contains(response, "This field is required")

    thread.refresh_from_db()
    other_thread.refresh_from_db()

    assert not ThreadUpdate.objects.exists()

    mock_thread_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_thread_detail_view_merge_thread_moderation_action_validates_other_thread_link(
    moderator_client,
    thread,
    other_thread,
    mock_thread_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
    )
    assert_contains(response, "Merge thread")
    assert_contains(response, "Other thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "merge",
            "moderation-other_thread": reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-direction": "this",
            "confirm": "true",
        },
    )
    assert_contains(response, "Enter a valid link.")

    thread.refresh_from_db()
    other_thread.refresh_from_db()

    assert not ThreadUpdate.objects.exists()

    mock_thread_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_thread_detail_view_merge_thread_moderation_action_validates_other_thread_is_different_thread(
    moderator_client,
    thread,
    other_thread,
    mock_thread_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
    )
    assert_contains(response, "Merge thread")
    assert_contains(response, "Other thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "merge",
            "moderation-other_thread": "http://testserver"
            + reverse(
                "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
            ),
            "moderation-direction": "this",
            "confirm": "true",
        },
    )
    assert_contains(response, "Can&#x27;t merge a thread with itself.")

    thread.refresh_from_db()
    other_thread.refresh_from_db()

    assert not ThreadUpdate.objects.exists()

    mock_thread_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_thread_detail_view_merge_thread_moderation_action_validates_other_thread_exists(
    moderator_client,
    thread,
    other_thread,
    mock_thread_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
    )
    assert_contains(response, "Merge thread")
    assert_contains(response, "Other thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "merge",
            "moderation-other_thread": f"http://testserver/t/other-thread/{max(thread.id, other_thread.id) + 1}/",
            "moderation-direction": "this",
            "confirm": "true",
        },
    )
    assert_contains(
        response,
        "Thread doesn&#x27;t exist or you don&#x27;t have permission to see it.",
    )

    thread.refresh_from_db()
    other_thread.refresh_from_db()

    assert not ThreadUpdate.objects.exists()

    mock_thread_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_thread_detail_view_merge_thread_moderation_action_validates_other_thread_is_not_private_thread(
    moderator_client,
    thread,
    user_private_thread,
    mock_thread_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
    )
    assert_contains(response, "Merge thread")
    assert_contains(response, "Other thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "merge",
            "moderation-other_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={
                    "thread_id": user_private_thread.id,
                    "slug": user_private_thread.slug,
                },
            ),
            "moderation-direction": "this",
            "confirm": "true",
        },
    )
    assert_contains(
        response,
        "Thread doesn&#x27;t exist or you don&#x27;t have permission to see it.",
    )

    thread.refresh_from_db()
    user_private_thread.refresh_from_db()

    assert not ThreadUpdate.objects.exists()

    mock_thread_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_thread_detail_view_merge_thread_moderation_action_validates_other_thread_is_visible(
    thread_factory,
    moderator_client,
    sibling_category,
    thread,
    mock_thread_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    other_thread = thread_factory(sibling_category, starter="DeletedUser")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
    )
    assert_contains(response, "Merge thread")
    assert_contains(response, "Other thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "merge",
            "moderation-other_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-direction": "this",
            "confirm": "true",
        },
    )
    assert_contains(
        response,
        "Thread doesn&#x27;t exist or you don&#x27;t have permission to see it.",
    )

    thread.refresh_from_db()
    other_thread.refresh_from_db()

    assert not ThreadUpdate.objects.exists()

    mock_thread_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_thread_detail_view_merge_thread_moderation_action_validates_other_thread_can_be_moderated(
    thread_factory,
    user_client,
    user,
    members_group,
    sibling_category,
    thread,
    mock_thread_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    grant_category_group_permissions(
        sibling_category,
        members_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    other_thread = thread_factory(sibling_category, starter="DeletedUser")

    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
    )
    assert_contains(response, "Merge thread")
    assert_contains(response, "Other thread link")

    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "merge",
            "moderation-other_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-direction": "this",
            "confirm": "true",
        },
    )
    assert_contains(response, "You can&#x27;t moderate this thread.")

    thread.refresh_from_db()
    other_thread.refresh_from_db()

    assert not ThreadUpdate.objects.exists()

    mock_thread_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_thread_detail_view_merge_thread_moderation_action_requires_conflict_resolution(
    thread_reply_factory,
    poll_factory,
    moderator_client,
    thread,
    other_thread,
    mock_thread_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    thread_solution = thread_reply_factory(thread, poster="Answer")
    other_thread_solution = thread_reply_factory(other_thread, poster="Answer")

    select_thread_solution(thread, thread_solution, user="JohnDoe")
    select_thread_solution(other_thread, other_thread_solution, user="JohnDoe")

    thread_poll = poll_factory(thread)
    other_thread_poll = poll_factory(other_thread)

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
    )
    assert_contains(response, "Merge thread")
    assert_contains(response, "Other thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "merge",
            "moderation-other_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-direction": "other",
            "confirm": "true",
        },
    )
    assert_contains(response, "Solution")
    assert_contains(response, "Poll")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "merge",
            "moderation-other_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-direction": "other",
            "confirm": "true",
            "confirm_conflicts": "true",
        },
    )
    assert_contains(response, "This field is required.")

    thread.refresh_from_db()
    other_thread.refresh_from_db()

    thread_poll.refresh_from_db()
    other_thread_poll.refresh_from_db()

    assert not ThreadUpdate.objects.exists()

    mock_thread_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_thread_detail_view_merge_thread_moderation_action_validates_conflict_resolution(
    thread_reply_factory,
    poll_factory,
    moderator_client,
    thread,
    other_thread,
    mock_thread_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    thread_solution = thread_reply_factory(thread, poster="Answer")
    other_thread_solution = thread_reply_factory(other_thread, poster="Answer")

    select_thread_solution(thread, thread_solution, user="JohnDoe")
    select_thread_solution(other_thread, other_thread_solution, user="JohnDoe")

    thread_poll = poll_factory(thread)
    other_thread_poll = poll_factory(other_thread)

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
    )
    assert_contains(response, "Merge thread")
    assert_contains(response, "Other thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "merge",
            "moderation-other_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-direction": "other",
            "confirm": "true",
        },
    )
    assert_contains(response, "Solution")
    assert_contains(response, "Poll")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "merge",
            "moderation-other_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-direction": "other",
            "moderation-solution": "invalid",
            "moderation-poll": "invalid",
            "confirm": "true",
            "confirm_conflicts": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    thread.refresh_from_db()
    other_thread.refresh_from_db()

    thread_poll.refresh_from_db()
    other_thread_poll.refresh_from_db()

    assert not ThreadUpdate.objects.exists()

    mock_thread_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_thread_detail_view_delete_thread_moderation_action_deletes_thread(
    moderator_client, default_category, thread, mock_thread_synchronize_categories
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "delete"},
    )
    assert_contains(response, "Delete thread")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "delete",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:category-thread-list",
        kwargs={"category_id": default_category.id, "slug": default_category.slug},
    )

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()

    mock_thread_synchronize_categories.delay.assert_called_once_with(
        [default_category.id]
    )


def test_thread_detail_view_lock_posts_moderation_action_locks_posts(
    moderator_client, thread, reply
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "lock", "posts": [reply.id]},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    reply.refresh_from_db()
    assert reply.is_locked


def test_thread_detail_view_lock_posts_moderation_action_validates_posts(
    moderator_client, thread, reply
):
    reply.is_locked = True
    reply.save()

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "lock", "posts": [reply.id]},
    )
    assert_contains(response, "Posts are already locked.")


def test_thread_detail_view_unlock_posts_moderation_action_unlocks_posts(
    moderator_client, thread, reply
):
    reply.is_locked = True
    reply.save()

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "unlock", "posts": [reply.id]},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    reply.refresh_from_db()
    assert not reply.is_locked


def test_thread_detail_view_unlock_posts_moderation_action_validates_posts(
    moderator_client, thread, reply
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "unlock", "posts": [reply.id]},
    )
    assert_contains(response, "Posts are already unlocked.")


def test_thread_detail_view_hide_posts_moderation_action_hides_posts(
    moderator_client, moderator, thread, reply
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "hide", "posts": [reply.id]},
    )
    assert_contains(response, "Hide posts")
    assert_contains(response, "Reason for hiding")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "hide",
            "posts": [reply.id],
            "moderation-hidden_reason": "Lorem ipsum",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    reply.refresh_from_db()
    assert reply.is_hidden
    assert reply.hidden_at
    assert reply.hidden_by == moderator
    assert reply.hidden_by_name == moderator.username
    assert reply.hidden_by_slug == moderator.slug
    assert reply.hidden_reason == "Lorem ipsum"


def test_thread_detail_view_hide_posts_moderation_action_validates_posts(
    moderator_client, thread, reply
):
    reply.is_hidden = True
    reply.save()

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "hide", "posts": [reply.id]},
    )
    assert_contains(response, "Posts are already hidden.")


def test_thread_detail_view_hide_posts_moderation_action_validates_first_post(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "hide", "posts": [thread.first_post_id]},
    )
    assert_contains(response, "Thread&#x27;s first post can&#x27;t be hidden.")


def test_thread_detail_view_unhide_posts_moderation_action_unhides_posts(
    moderator_client, thread, reply
):
    reply.is_hidden = True
    reply.save()

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "unhide", "posts": [reply.id]},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    reply.refresh_from_db()
    assert not reply.is_hidden
    assert reply.hidden_at is None
    assert reply.hidden_by is None
    assert reply.hidden_by_name is None
    assert reply.hidden_by_slug is None
    assert reply.hidden_reason is None


def test_thread_detail_view_unhide_posts_moderation_action_validates_posts(
    moderator_client, thread, reply
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "unhide", "posts": [reply.id]},
    )
    assert_contains(response, "Posts are already unhidden.")


def test_thread_detail_view_approve_posts_moderation_action_approves_posts(
    post_factory,
    moderator_client,
    thread,
    mock_posts_synchronize_categories,
    mock_posts_notify_on_new_thread_reply,
):
    reply = post_factory(thread, is_unapproved=True)

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "approve", "posts": [reply.id]},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    reply.refresh_from_db()
    assert not reply.is_unapproved

    thread.refresh_from_db()
    assert thread.last_post == reply

    mock_posts_synchronize_categories.delay.assert_called_with([thread.category_id])
    mock_posts_notify_on_new_thread_reply.delay.assert_called_with(reply.id)


def test_thread_detail_view_approve_posts_moderation_action_validates_posts(
    moderator_client,
    thread,
    reply,
    mock_posts_synchronize_categories,
    mock_posts_notify_on_new_thread_reply,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "approve", "posts": [reply.id]},
    )
    assert_contains(response, "Posts are already approved.")

    mock_posts_synchronize_categories.delay.assert_not_called()
    mock_posts_notify_on_new_thread_reply.delay.assert_not_called()


def test_thread_detail_view_split_posts_moderation_action_splits_posts(
    moderator_client,
    default_category,
    thread,
    reply,
    mock_posts_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "split", "posts": [reply.id]},
    )
    assert_contains(response, "Split posts")
    assert_contains(response, "Category")
    assert_contains(response, "Title")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "split",
            "posts": [reply.id],
            "moderation-category": default_category.id,
            "moderation-title": "New thread",
            "moderation-redirect_to": "current",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.replies == 0

    new_thread = Thread.objects.get(slug="new-thread")
    assert new_thread.replies == 0

    reply.refresh_from_db()
    assert reply.thread == new_thread

    ThreadUpdate.objects.get(
        thread=new_thread,
        action=ThreadUpdateActionName.SPLIT_POSTS_FROM,
    )
    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.SPLIT_POSTS_INTO,
    )

    mock_posts_synchronize_categories.delay.assert_called_once_with(
        [default_category.id]
    )


def test_thread_detail_view_split_posts_moderation_action_splits_posts_in_htmx(
    moderator_client,
    default_category,
    thread,
    reply,
    mock_posts_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "split", "posts": [reply.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Category")
    assert_contains(response, "Title")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "split",
            "posts": [reply.id],
            "moderation-category": default_category.id,
            "moderation-title": "New thread",
            "moderation-redirect_to": "current",
            "confirm": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200

    thread.refresh_from_db()
    assert thread.replies == 0

    new_thread = Thread.objects.get(slug="new-thread")
    assert new_thread.replies == 0

    reply.refresh_from_db()
    assert reply.thread == new_thread

    ThreadUpdate.objects.get(
        thread=new_thread,
        action=ThreadUpdateActionName.SPLIT_POSTS_FROM,
    )
    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.SPLIT_POSTS_INTO,
    )

    mock_posts_synchronize_categories.delay.assert_called_once_with(
        [default_category.id]
    )


def test_thread_detail_view_split_posts_moderation_action_splits_posts_with_redirect_to_new_thread(
    moderator_client,
    default_category,
    thread,
    reply,
    mock_posts_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "split", "posts": [reply.id]},
    )
    assert_contains(response, "Split posts")
    assert_contains(response, "Category")
    assert_contains(response, "Title")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "split",
            "posts": [reply.id],
            "moderation-category": default_category.id,
            "moderation-title": "New thread",
            "moderation-redirect_to": "new",
            "confirm": "true",
        },
    )

    new_thread = Thread.objects.get(slug="new-thread")
    assert new_thread.replies == 0

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": new_thread.id, "slug": new_thread.slug}
    )

    thread.refresh_from_db()
    assert thread.replies == 0

    reply.refresh_from_db()
    assert reply.thread == new_thread

    ThreadUpdate.objects.get(
        thread=new_thread,
        action=ThreadUpdateActionName.SPLIT_POSTS_FROM,
    )
    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.SPLIT_POSTS_INTO,
    )

    mock_posts_synchronize_categories.delay.assert_called_once_with(
        [default_category.id]
    )


def test_thread_detail_view_split_posts_moderation_action_splits_posts_with_moderation_options(
    moderator_client,
    default_category,
    thread,
    reply,
    mock_posts_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "split", "posts": [reply.id]},
    )
    assert_contains(response, "Split posts")
    assert_contains(response, "Category")
    assert_contains(response, "Title")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "split",
            "posts": [reply.id],
            "moderation-category": default_category.id,
            "moderation-title": "New thread",
            "moderation-redirect_to": "current",
            "moderation-pin": ThreadPinned.EVERYWHERE,
            "moderation-is_hidden": "1",
            "moderation-is_locked": "1",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.replies == 0

    new_thread = Thread.objects.get(slug="new-thread")
    assert new_thread.replies == 0
    assert new_thread.pinned == ThreadPinned.EVERYWHERE
    assert new_thread.is_hidden
    assert new_thread.is_locked

    reply.refresh_from_db()
    assert reply.thread == new_thread

    ThreadUpdate.objects.get(
        thread=new_thread,
        action=ThreadUpdateActionName.SPLIT_POSTS_FROM,
    )
    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.SPLIT_POSTS_INTO,
    )

    mock_posts_synchronize_categories.delay.assert_called_once_with(
        [default_category.id]
    )


def test_thread_detail_view_split_posts_moderation_action_validates_first_post(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "split", "posts": [thread.first_post_id]},
    )
    assert_contains(response, "Thread&#x27;s first post can&#x27;t be split.")


def test_thread_detail_view_split_posts_moderation_action_validates_category_value(
    moderator_client, thread, reply, mock_posts_synchronize_categories
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "split", "posts": [reply.id]},
    )
    assert_contains(response, "Split posts")
    assert_contains(response, "Category")
    assert_contains(response, "Title")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "split",
            "posts": [reply.id],
            "moderation-category": "invalid",
            "moderation-title": "New thread",
            "moderation-redirect_to": "new",
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    reply.refresh_from_db()
    assert reply.thread == thread

    assert not ThreadUpdate.objects.exists()

    mock_posts_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_split_posts_moderation_action_validates_category_browse_permission(
    moderator_client,
    moderators_group,
    sibling_category,
    thread,
    reply,
    mock_posts_synchronize_categories,
):
    grant_category_group_permissions(
        sibling_category,
        moderators_group,
        CategoryPermission.SEE,
    )

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "split", "posts": [reply.id]},
    )
    assert_contains(response, "Split posts")
    assert_contains(response, "Category")
    assert_contains(response, "Title")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "split",
            "posts": [reply.id],
            "moderation-category": sibling_category.id,
            "moderation-title": "New thread",
            "moderation-redirect_to": "new",
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    reply.refresh_from_db()
    assert reply.thread == thread

    assert not ThreadUpdate.objects.exists()

    mock_posts_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_split_posts_moderation_action_validates_category_moderator_permission(
    user_client,
    user,
    members_group,
    default_category,
    sibling_category,
    thread,
    reply,
    mock_posts_synchronize_categories,
):
    grant_category_group_permissions(
        sibling_category,
        members_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "split", "posts": [reply.id]},
    )
    assert_contains(response, "Split posts")
    assert_contains(response, "Category")
    assert_contains(response, "Title")

    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "split",
            "posts": [reply.id],
            "moderation-category": sibling_category.id,
            "moderation-title": "New thread",
            "moderation-redirect_to": "new",
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    reply.refresh_from_db()
    assert reply.thread == thread

    assert not ThreadUpdate.objects.exists()

    mock_posts_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_split_posts_moderation_action_validates_category_type(
    moderator_client,
    moderators_group,
    sibling_category,
    thread,
    reply,
    mock_posts_synchronize_categories,
):
    grant_category_group_permissions(
        sibling_category,
        moderators_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    sibling_category.is_vanilla = True
    sibling_category.save()

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "split", "posts": [reply.id]},
    )
    assert_contains(response, "Split posts")
    assert_contains(response, "Category")
    assert_contains(response, "Title")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "split",
            "posts": [reply.id],
            "moderation-category": sibling_category.id,
            "moderation-title": "New thread",
            "moderation-redirect_to": "new",
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    reply.refresh_from_db()
    assert reply.thread == thread

    assert not ThreadUpdate.objects.exists()

    mock_posts_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_split_posts_moderation_action_requires_thread_title(
    moderator_client,
    moderators_group,
    default_category,
    thread,
    reply,
    mock_posts_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "split", "posts": [reply.id]},
    )
    assert_contains(response, "Split posts")
    assert_contains(response, "Category")
    assert_contains(response, "Title")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "split",
            "posts": [reply.id],
            "moderation-category": default_category.id,
            "moderation-redirect_to": "new",
            "confirm": "true",
        },
    )
    assert_contains(response, "This field is required.")

    reply.refresh_from_db()
    assert reply.thread == thread

    assert not ThreadUpdate.objects.exists()

    mock_posts_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_split_posts_moderation_action_validates_thread_title(
    moderator_client,
    default_category,
    thread,
    reply,
    mock_posts_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "split", "posts": [reply.id]},
    )
    assert_contains(response, "Split posts")
    assert_contains(response, "Category")
    assert_contains(response, "Title")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "split",
            "posts": [reply.id],
            "moderation-category": default_category.id,
            "moderation-title": "Q",
            "moderation-redirect_to": "new",
            "confirm": "true",
        },
    )
    assert_contains(response, "Thread title should be at least 5 characters long")

    reply.refresh_from_db()
    assert reply.thread == thread

    assert not ThreadUpdate.objects.exists()

    mock_posts_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_move_posts_moderation_action_moves_posts(
    moderator_client,
    default_category,
    thread,
    other_thread,
    reply,
    mock_posts_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "move", "posts": [reply.id]},
    )
    assert_contains(response, "Move posts")
    assert_contains(response, "Target thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "move",
            "posts": [reply.id],
            "moderation-target_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-redirect_to": "current",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.replies == 0

    other_thread.refresh_from_db()
    assert other_thread.replies == 1

    reply.refresh_from_db()
    assert reply.thread == other_thread

    ThreadUpdate.objects.get(
        thread=other_thread,
        action=ThreadUpdateActionName.MOVED_POSTS_FROM,
    )
    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.MOVED_POSTS_TO,
    )

    mock_posts_synchronize_categories.delay.assert_called_once_with(
        [default_category.id]
    )


def test_thread_detail_view_move_posts_moderation_action_moves_posts_in_htmx(
    moderator_client,
    default_category,
    thread,
    other_thread,
    reply,
    mock_posts_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "move", "posts": [reply.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Target thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "move",
            "posts": [reply.id],
            "moderation-target_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-redirect_to": "current",
            "confirm": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200

    thread.refresh_from_db()
    assert thread.replies == 0

    other_thread.refresh_from_db()
    assert other_thread.replies == 1

    reply.refresh_from_db()
    assert reply.thread == other_thread

    ThreadUpdate.objects.get(
        thread=other_thread,
        action=ThreadUpdateActionName.MOVED_POSTS_FROM,
    )
    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.MOVED_POSTS_TO,
    )

    mock_posts_synchronize_categories.delay.assert_called_once_with(
        [default_category.id]
    )


def test_thread_detail_view_move_posts_moderation_action_moves_posts_with_redirect_to_target_thread(
    moderator_client,
    default_category,
    thread,
    other_thread,
    reply,
    mock_posts_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "move", "posts": [reply.id]},
    )
    assert_contains(response, "Move posts")
    assert_contains(response, "Target thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "move",
            "posts": [reply.id],
            "moderation-target_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-redirect_to": "target",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread",
        kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
    )

    thread.refresh_from_db()
    assert thread.replies == 0

    other_thread.refresh_from_db()
    assert other_thread.replies == 1

    reply.refresh_from_db()
    assert reply.thread == other_thread

    ThreadUpdate.objects.get(
        thread=other_thread,
        action=ThreadUpdateActionName.MOVED_POSTS_FROM,
    )
    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.MOVED_POSTS_TO,
    )

    mock_posts_synchronize_categories.delay.assert_called_once_with(
        [default_category.id]
    )


def test_thread_detail_view_move_posts_moderation_action_validates_target_thread_link(
    moderator_client,
    thread,
    other_thread,
    reply,
    mock_posts_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "move", "posts": [reply.id]},
    )
    assert_contains(response, "Move posts")
    assert_contains(response, "Target thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "move",
            "posts": [reply.id],
            "moderation-target_thread": reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-redirect_to": "target",
            "confirm": "true",
        },
    )
    assert_contains(response, "Enter a valid link.")

    thread.refresh_from_db()
    assert thread.replies == 1

    other_thread.refresh_from_db()
    assert other_thread.replies == 0

    reply.refresh_from_db()
    assert reply.thread == thread

    assert not ThreadUpdate.objects.exists()

    mock_posts_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_move_posts_moderation_action_validates_target_thread_is_different_thread(
    moderator_client,
    thread,
    other_thread,
    reply,
    mock_posts_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "move", "posts": [reply.id]},
    )
    assert_contains(response, "Move posts")
    assert_contains(response, "Target thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "move",
            "posts": [reply.id],
            "moderation-target_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": thread.id, "slug": thread.slug},
            ),
            "moderation-redirect_to": "target",
            "confirm": "true",
        },
    )
    assert_contains(response, "Can&#x27;t move posts to the same thread.")

    thread.refresh_from_db()
    assert thread.replies == 1

    other_thread.refresh_from_db()
    assert other_thread.replies == 0

    reply.refresh_from_db()
    assert reply.thread == thread

    assert not ThreadUpdate.objects.exists()

    mock_posts_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_move_posts_moderation_action_validates_target_thread_exists(
    moderator_client,
    thread,
    other_thread,
    reply,
    mock_posts_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "move", "posts": [reply.id]},
    )
    assert_contains(response, "Move posts")
    assert_contains(response, "Target thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "move",
            "posts": [reply.id],
            "moderation-target_thread": f"http://testserver/t/other-thread/{max(thread.id, other_thread.id) + 1}/",
            "moderation-redirect_to": "target",
            "confirm": "true",
        },
    )
    assert_contains(
        response,
        "Thread doesn&#x27;t exist or you don&#x27;t have permission to see it.",
    )

    thread.refresh_from_db()
    assert thread.replies == 1

    other_thread.refresh_from_db()
    assert other_thread.replies == 0

    reply.refresh_from_db()
    assert reply.thread == thread

    assert not ThreadUpdate.objects.exists()

    mock_posts_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_move_posts_moderation_action_validates_target_thread_is_not_private_thread(
    moderator_client,
    thread,
    user_private_thread,
    reply,
    mock_posts_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "move", "posts": [reply.id]},
    )
    assert_contains(response, "Move posts")
    assert_contains(response, "Target thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "move",
            "posts": [reply.id],
            "moderation-target_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={
                    "thread_id": user_private_thread.id,
                    "slug": user_private_thread.slug,
                },
            ),
            "moderation-redirect_to": "target",
            "confirm": "true",
        },
    )
    assert_contains(
        response,
        "Thread doesn&#x27;t exist or you don&#x27;t have permission to see it.",
    )

    thread.refresh_from_db()
    assert thread.replies == 1

    user_private_thread.refresh_from_db()
    assert user_private_thread.replies == 0

    reply.refresh_from_db()
    assert reply.thread == thread

    assert not ThreadUpdate.objects.exists()

    mock_posts_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_move_posts_moderation_action_validates_target_thread_is_visible(
    thread_factory,
    moderator_client,
    sibling_category,
    thread,
    reply,
    mock_posts_synchronize_categories,
):
    other_thread = thread_factory(sibling_category, starter="DeletedUser")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "move", "posts": [reply.id]},
    )
    assert_contains(response, "Move posts")
    assert_contains(response, "Target thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "move",
            "posts": [reply.id],
            "moderation-target_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-redirect_to": "target",
            "confirm": "true",
        },
    )
    assert_contains(
        response,
        "Thread doesn&#x27;t exist or you don&#x27;t have permission to see it.",
    )

    thread.refresh_from_db()
    assert thread.replies == 1

    other_thread.refresh_from_db()
    assert other_thread.replies == 0

    reply.refresh_from_db()
    assert reply.thread == thread

    assert not ThreadUpdate.objects.exists()

    mock_posts_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_move_posts_moderation_action_validates_target_thread_can_be_moderated(
    thread_factory,
    user_client,
    user,
    members_group,
    sibling_category,
    thread,
    reply,
    mock_post_synchronize_categories,
):
    grant_category_group_permissions(
        sibling_category,
        members_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    other_thread = thread_factory(sibling_category, starter="DeletedUser")

    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "move", "posts": [reply.id]},
    )
    assert_contains(response, "Move post")
    assert_contains(response, "Target thread link")

    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "move",
            "posts": [reply.id],
            "moderation-target_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-redirect_to": "target",
            "confirm": "true",
        },
    )
    assert_contains(response, "You can&#x27;t moderate this thread.")

    thread.refresh_from_db()
    assert thread.replies == 1

    other_thread.refresh_from_db()
    assert other_thread.replies == 0

    reply.refresh_from_db()
    assert reply.thread == thread

    assert not ThreadUpdate.objects.exists()

    mock_post_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_merge_posts_moderation_action_merges_posts(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    default_category,
    thread,
    mock_posts_synchronize_categories,
):
    target_post = thread_reply_factory(thread, poster=user, original="Target body")
    other_post = thread_reply_factory(thread, poster=user, original="Other body")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "merge", "posts": [target_post.id, other_post.id]},
    )
    assert_contains(response, "Merge posts")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "merge",
            "posts": [target_post.id, other_post.id],
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    target_post.refresh_from_db()
    assert target_post.original == "Target body\n\nOther body"
    assert not target_post.last_edit_reason

    post_edit = PostEdit.objects.get(post=target_post)
    assert post_edit.user == moderator
    assert not post_edit.edit_reason
    assert post_edit.old_content == "Target body"
    assert post_edit.new_content == "Target body\n\nOther body"

    with pytest.raises(Post.DoesNotExist):
        other_post.refresh_from_db()

    mock_posts_synchronize_categories.delay.assert_called_with([default_category.id])


def test_thread_detail_view_merge_posts_moderation_action_merges_posts_in_htmx(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    default_category,
    thread,
    mock_posts_synchronize_categories,
):
    target_post = thread_reply_factory(thread, poster=user, original="Target body")
    other_post = thread_reply_factory(thread, poster=user, original="Other body")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "merge", "posts": [target_post.id, other_post.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "merge",
            "posts": [target_post.id, other_post.id],
            "confirm": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200

    target_post.refresh_from_db()
    assert target_post.original == "Target body\n\nOther body"
    assert not target_post.last_edit_reason

    post_edit = PostEdit.objects.get(post=target_post)
    assert post_edit.user == moderator
    assert not post_edit.edit_reason
    assert post_edit.old_content == "Target body"
    assert post_edit.new_content == "Target body\n\nOther body"

    with pytest.raises(Post.DoesNotExist):
        other_post.refresh_from_db()

    mock_posts_synchronize_categories.delay.assert_called_with([default_category.id])


def test_thread_detail_view_merge_posts_moderation_action_merges_posts_with_merge_reason(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    default_category,
    thread,
    mock_posts_synchronize_categories,
):
    target_post = thread_reply_factory(thread, poster=user, original="Target body")
    other_post = thread_reply_factory(thread, poster=user, original="Other body")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "merge", "posts": [target_post.id, other_post.id]},
    )
    assert_contains(response, "Merge posts")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "merge",
            "posts": [target_post.id, other_post.id],
            "moderation-edit_reason": "Test merge",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    target_post.refresh_from_db()
    assert target_post.original == "Target body\n\nOther body"
    assert target_post.last_edit_reason == "Test merge"

    post_edit = PostEdit.objects.get(post=target_post)
    assert post_edit.user == moderator
    assert post_edit.edit_reason == "Test merge"
    assert post_edit.old_content == "Target body"
    assert post_edit.new_content == "Target body\n\nOther body"

    with pytest.raises(Post.DoesNotExist):
        other_post.refresh_from_db()

    mock_posts_synchronize_categories.delay.assert_called_with([default_category.id])


def test_thread_detail_view_merge_posts_moderation_action_merges_other_post_into_solution(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    default_category,
    thread,
    mock_posts_synchronize_categories,
):
    target_post = thread_reply_factory(thread, poster=user, original="Target body")
    other_post = thread_reply_factory(thread, poster=user, original="Other body")

    select_thread_solution(thread, target_post, moderator)

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "merge", "posts": [target_post.id, other_post.id]},
    )
    assert_contains(response, "Merge posts")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "merge",
            "posts": [target_post.id, other_post.id],
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.solution == target_post

    target_post.refresh_from_db()
    assert target_post.original == "Target body\n\nOther body"
    assert not target_post.last_edit_reason

    post_edit = PostEdit.objects.get(post=target_post)
    assert post_edit.user == moderator
    assert not post_edit.edit_reason
    assert post_edit.old_content == "Target body"
    assert post_edit.new_content == "Target body\n\nOther body"

    with pytest.raises(Post.DoesNotExist):
        other_post.refresh_from_db()

    mock_posts_synchronize_categories.delay.assert_called_with([default_category.id])


def test_thread_detail_view_merge_posts_moderation_action_merges_solution_into_target_post(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    default_category,
    thread,
    mock_posts_synchronize_categories,
):
    target_post = thread_reply_factory(thread, poster=user, original="Target body")
    other_post = thread_reply_factory(thread, poster=user, original="Other body")

    select_thread_solution(thread, other_post, moderator)

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "merge", "posts": [target_post.id, other_post.id]},
    )
    assert_contains(response, "Merge posts")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "merge",
            "posts": [target_post.id, other_post.id],
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.solution == target_post

    target_post.refresh_from_db()
    assert target_post.original == "Target body\n\nOther body"
    assert not target_post.last_edit_reason

    post_edit = PostEdit.objects.get(post=target_post)
    assert post_edit.user == moderator
    assert not post_edit.edit_reason
    assert post_edit.old_content == "Target body"
    assert post_edit.new_content == "Target body\n\nOther body"

    with pytest.raises(Post.DoesNotExist):
        other_post.refresh_from_db()

    mock_posts_synchronize_categories.delay.assert_called_with([default_category.id])


def test_thread_detail_view_merge_posts_moderation_action_merges_posts_with_attachments(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    default_category,
    thread,
    text_attachment,
    image_attachment,
    mock_posts_synchronize_categories,
):
    target_post = thread_reply_factory(thread, poster=user, original="Target body")
    other_post = thread_reply_factory(thread, poster=user, original="Other body")

    text_attachment.associate_with_post(target_post)
    text_attachment.save()

    image_attachment.associate_with_post(other_post)
    image_attachment.save()

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "merge", "posts": [target_post.id, other_post.id]},
    )
    assert_contains(response, "Merge posts")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "merge",
            "posts": [target_post.id, other_post.id],
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    target_post.refresh_from_db()
    assert target_post.original == "Target body\n\nOther body"
    assert not target_post.last_edit_reason

    text_attachment.refresh_from_db()
    assert text_attachment.post == target_post

    image_attachment.refresh_from_db()
    assert image_attachment.post == target_post

    post_edit = PostEdit.objects.get(post=target_post)
    assert post_edit.user == moderator
    assert not post_edit.edit_reason
    assert post_edit.old_content == "Target body"
    assert post_edit.new_content == "Target body\n\nOther body"
    assert post_edit.attachments[0]["id"] == image_attachment.id
    assert post_edit.attachments[0]["change"] == "+"
    assert post_edit.attachments[1]["id"] == text_attachment.id
    assert post_edit.attachments[1]["change"] == "="

    with pytest.raises(Post.DoesNotExist):
        other_post.refresh_from_db()

    mock_posts_synchronize_categories.delay.assert_called_with([default_category.id])


def test_thread_detail_view_merge_posts_moderation_action_orders_posts_from_oldest(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    default_category,
    thread,
    mock_posts_synchronize_categories,
):
    target_post = thread_reply_factory(thread, poster=user, original="Target body")
    other_post = thread_reply_factory(thread, poster=user, original="Other body")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "merge", "posts": [other_post.id, target_post.id]},
    )
    assert_contains(response, "Merge posts")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "merge",
            "posts": [other_post.id, target_post.id],
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    target_post.refresh_from_db()
    assert target_post.original == "Target body\n\nOther body"
    assert not target_post.last_edit_reason

    post_edit = PostEdit.objects.get(post=target_post)
    assert post_edit.user == moderator
    assert not post_edit.edit_reason
    assert post_edit.old_content == "Target body"
    assert post_edit.new_content == "Target body\n\nOther body"

    with pytest.raises(Post.DoesNotExist):
        other_post.refresh_from_db()

    mock_posts_synchronize_categories.delay.assert_called_with([default_category.id])


def test_thread_detail_view_merge_posts_moderation_action_validates_multiple_posts_are_selected(
    thread_reply_factory,
    moderator_client,
    user,
    thread,
    mock_posts_synchronize_categories,
):
    target_post = thread_reply_factory(thread, poster=user, original="Target body")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "merge", "posts": [target_post.id]},
    )
    assert_contains(response, "Select at least two posts to merge.")

    target_post.refresh_from_db()
    assert target_post.original == "Target body"

    assert not PostEdit.objects.exists()

    mock_posts_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_merge_posts_moderation_action_validates_posts_are_by_same_user(
    thread_reply_factory,
    moderator_client,
    user,
    other_user,
    thread,
    mock_posts_synchronize_categories,
):
    target_post = thread_reply_factory(thread, poster=user, original="Target body")
    other_post = thread_reply_factory(thread, poster=other_user, original="Other body")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "merge", "posts": [target_post.id, other_post.id]},
    )
    assert_contains(response, "Merged posts must belong to the same user.")

    target_post.refresh_from_db()
    assert target_post.original == "Target body"

    other_post.refresh_from_db()
    assert other_post.original == "Other body"

    assert not PostEdit.objects.exists()

    mock_posts_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_merge_posts_moderation_action_validates_posts_are_by_same_deleted_user(
    thread_reply_factory, moderator_client, thread, mock_posts_synchronize_categories
):
    target_post = thread_reply_factory(thread, poster="John", original="Target body")
    other_post = thread_reply_factory(thread, poster="Alice", original="Other body")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "merge", "posts": [target_post.id, other_post.id]},
    )
    assert_contains(response, "Merged posts must belong to the same user.")

    target_post.refresh_from_db()
    assert target_post.original == "Target body"

    other_post.refresh_from_db()
    assert other_post.original == "Other body"

    assert not PostEdit.objects.exists()

    mock_posts_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_delete_posts_moderation_action_deletes_posts(
    moderator_client, default_category, thread, reply, mock_posts_synchronize_categories
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "delete", "posts": [reply.id]},
    )
    assert_contains(response, "Delete posts")
    assert_contains(response, "Are you sure you want to delete the selected posts?")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "delete",
            "posts": [reply.id],
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.DELETED_POSTS,
    )

    mock_posts_synchronize_categories.delay.assert_called_with([default_category.id])


def test_thread_detail_view_delete_posts_moderation_action_deletes_posts_in_htmx(
    moderator_client, default_category, thread, reply, mock_posts_synchronize_categories
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "delete", "posts": [reply.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Are you sure you want to delete the selected posts?")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "delete",
            "posts": [reply.id],
            "confirm": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.DELETED_POSTS,
    )

    mock_posts_synchronize_categories.delay.assert_called_with([default_category.id])


def test_thread_detail_view_delete_posts_moderation_action_validates_first_post(
    moderator_client, thread, mock_posts_synchronize_categories
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "delete", "posts": [thread.first_post_id]},
    )
    assert_contains(response, "Thread&#x27;s first post can&#x27;t be deleted.")

    thread.first_post.refresh_from_db()

    assert not ThreadUpdate.objects.exists()

    mock_posts_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_lock_post_moderation_action_locks_post(
    moderator_client, thread, reply
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "lock", "post": reply.id},
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
        )
        + f"#post-{reply.id}"
    )

    reply.refresh_from_db()
    assert reply.is_locked


def test_thread_detail_view_unlock_post_moderation_action_unlocks_post(
    moderator_client, thread, reply
):
    reply.is_locked = True
    reply.save()

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "unlock", "post": reply.id},
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
        )
        + f"#post-{reply.id}"
    )

    reply.refresh_from_db()
    assert not reply.is_locked


def test_thread_detail_view_hide_post_moderation_action_hides_post(
    moderator_client, moderator, thread, reply
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "hide", "post": reply.id},
    )
    assert_contains(response, "Reason for hiding")
    assert_contains(response, "Hide post")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "hide",
            "post": reply.id,
            "moderation-hidden_reason": "Lorem ipsum",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
        )
        + f"#post-{reply.id}"
    )

    reply.refresh_from_db()
    assert reply.is_hidden
    assert reply.hidden_at
    assert reply.hidden_by == moderator
    assert reply.hidden_by_name == moderator.username
    assert reply.hidden_by_slug == moderator.slug
    assert reply.hidden_reason == "Lorem ipsum"


def test_thread_detail_view_unhide_post_moderation_action_unhides_post(
    moderator_client, thread, reply
):
    reply.is_hidden = True
    reply.save()

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "unhide", "post": reply.id},
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
        )
        + f"#post-{reply.id}"
    )

    reply.refresh_from_db()
    assert not reply.is_hidden
    assert reply.hidden_at is None
    assert reply.hidden_by is None
    assert reply.hidden_by_name is None
    assert reply.hidden_by_slug is None
    assert reply.hidden_reason is None


def test_thread_detail_view_approve_post_moderation_action_approves_post(
    post_factory,
    moderator_client,
    thread,
    mock_post_synchronize_categories,
    mock_post_notify_on_new_thread_reply,
):
    reply = post_factory(thread, is_unapproved=True)

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "approve", "post": reply.id},
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
        )
        + f"#post-{reply.id}"
    )

    reply.refresh_from_db()
    assert not reply.is_unapproved

    thread.refresh_from_db()
    assert thread.last_post == reply

    mock_post_synchronize_categories.delay.assert_called_with([thread.category_id])
    mock_post_notify_on_new_thread_reply.delay.assert_called_with(reply.id)


def test_thread_detail_view_split_post_moderation_action_splits_post(
    moderator_client,
    default_category,
    thread,
    reply,
    mock_post_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "split", "post": reply.id},
    )
    assert_contains(response, "Split post")
    assert_contains(response, "Category")
    assert_contains(response, "Title")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "split",
            "post": reply.id,
            "moderation-category": default_category.id,
            "moderation-title": "New thread",
            "moderation-redirect_to": "current",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.replies == 0

    new_thread = Thread.objects.get(slug="new-thread")
    assert new_thread.replies == 0

    reply.refresh_from_db()
    assert reply.thread == new_thread

    ThreadUpdate.objects.get(
        thread=new_thread,
        action=ThreadUpdateActionName.SPLIT_POSTS_FROM,
    )
    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.SPLIT_POSTS_INTO,
    )

    mock_post_synchronize_categories.delay.assert_called_once_with(
        [default_category.id]
    )


def test_thread_detail_view_split_post_moderation_action_splits_post_in_htmx(
    moderator_client,
    default_category,
    thread,
    reply,
    mock_post_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "split", "post": reply.id},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Category")
    assert_contains(response, "Title")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "split",
            "post": reply.id,
            "moderation-category": default_category.id,
            "moderation-title": "New thread",
            "moderation-redirect_to": "current",
            "confirm": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200

    thread.refresh_from_db()
    assert thread.replies == 0

    new_thread = Thread.objects.get(slug="new-thread")
    assert new_thread.replies == 0

    reply.refresh_from_db()
    assert reply.thread == new_thread

    ThreadUpdate.objects.get(
        thread=new_thread,
        action=ThreadUpdateActionName.SPLIT_POSTS_FROM,
    )
    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.SPLIT_POSTS_INTO,
    )

    mock_post_synchronize_categories.delay.assert_called_once_with(
        [default_category.id]
    )


def test_thread_detail_view_split_post_moderation_action_splits_post_with_redirect_to_new_thread(
    moderator_client,
    default_category,
    thread,
    reply,
    mock_post_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "split", "post": reply.id},
    )
    assert_contains(response, "Split post")
    assert_contains(response, "Category")
    assert_contains(response, "Title")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "split",
            "post": reply.id,
            "moderation-category": default_category.id,
            "moderation-title": "New thread",
            "moderation-redirect_to": "new",
            "confirm": "true",
        },
    )

    new_thread = Thread.objects.get(slug="new-thread")
    assert new_thread.replies == 0

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": new_thread.id, "slug": new_thread.slug}
    )

    thread.refresh_from_db()
    assert thread.replies == 0

    reply.refresh_from_db()
    assert reply.thread == new_thread

    ThreadUpdate.objects.get(
        thread=new_thread,
        action=ThreadUpdateActionName.SPLIT_POSTS_FROM,
    )
    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.SPLIT_POSTS_INTO,
    )

    mock_post_synchronize_categories.delay.assert_called_once_with(
        [default_category.id]
    )


def test_thread_detail_view_split_post_moderation_action_splits_post_with_moderation_options(
    moderator_client,
    default_category,
    thread,
    reply,
    mock_post_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "split", "post": reply.id},
    )
    assert_contains(response, "Split post")
    assert_contains(response, "Category")
    assert_contains(response, "Title")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "split",
            "post": reply.id,
            "moderation-category": default_category.id,
            "moderation-title": "New thread",
            "moderation-redirect_to": "current",
            "moderation-pin": ThreadPinned.EVERYWHERE,
            "moderation-is_hidden": "1",
            "moderation-is_locked": "1",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.replies == 0

    new_thread = Thread.objects.get(slug="new-thread")
    assert new_thread.replies == 0
    assert new_thread.pinned == ThreadPinned.EVERYWHERE
    assert new_thread.is_hidden
    assert new_thread.is_locked

    reply.refresh_from_db()
    assert reply.thread == new_thread

    ThreadUpdate.objects.get(
        thread=new_thread,
        action=ThreadUpdateActionName.SPLIT_POSTS_FROM,
    )
    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.SPLIT_POSTS_INTO,
    )

    mock_post_synchronize_categories.delay.assert_called_once_with(
        [default_category.id]
    )


def test_thread_detail_view_split_post_moderation_action_validates_category_value(
    moderator_client, thread, reply, mock_post_synchronize_categories
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "split", "post": reply.id},
    )
    assert_contains(response, "Split post")
    assert_contains(response, "Category")
    assert_contains(response, "Title")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "split",
            "post": reply.id,
            "moderation-category": "invalid",
            "moderation-title": "New thread",
            "moderation-redirect_to": "new",
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    reply.refresh_from_db()
    assert reply.thread == thread

    assert not ThreadUpdate.objects.exists()

    mock_post_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_split_post_moderation_action_validates_category_browse_permission(
    moderator_client,
    moderators_group,
    sibling_category,
    thread,
    reply,
    mock_post_synchronize_categories,
):
    grant_category_group_permissions(
        sibling_category,
        moderators_group,
        CategoryPermission.SEE,
    )

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "split", "post": reply.id},
    )
    assert_contains(response, "Split post")
    assert_contains(response, "Category")
    assert_contains(response, "Title")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "split",
            "post": reply.id,
            "moderation-category": sibling_category.id,
            "moderation-title": "New thread",
            "moderation-redirect_to": "new",
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    reply.refresh_from_db()
    assert reply.thread == thread

    assert not ThreadUpdate.objects.exists()

    mock_post_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_split_post_moderation_action_validates_category_moderator_permission(
    user_client,
    user,
    members_group,
    default_category,
    sibling_category,
    thread,
    reply,
    mock_post_synchronize_categories,
):
    grant_category_group_permissions(
        sibling_category,
        members_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "split", "post": reply.id},
    )
    assert_contains(response, "Split post")
    assert_contains(response, "Category")
    assert_contains(response, "Title")

    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "split",
            "post": reply.id,
            "moderation-category": sibling_category.id,
            "moderation-title": "New thread",
            "moderation-redirect_to": "new",
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    reply.refresh_from_db()
    assert reply.thread == thread

    assert not ThreadUpdate.objects.exists()

    mock_post_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_split_post_moderation_action_validates_category_type(
    moderator_client,
    moderators_group,
    sibling_category,
    thread,
    reply,
    mock_post_synchronize_categories,
):
    grant_category_group_permissions(
        sibling_category,
        moderators_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    sibling_category.is_vanilla = True
    sibling_category.save()

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "split", "post": reply.id},
    )
    assert_contains(response, "Split post")
    assert_contains(response, "Category")
    assert_contains(response, "Title")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "split",
            "post": reply.id,
            "moderation-category": sibling_category.id,
            "moderation-title": "New thread",
            "moderation-redirect_to": "new",
            "confirm": "true",
        },
    )
    assert_contains(response, "Select a valid choice.")

    reply.refresh_from_db()
    assert reply.thread == thread

    assert not ThreadUpdate.objects.exists()

    mock_post_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_split_post_moderation_action_requires_thread_title(
    moderator_client,
    moderators_group,
    default_category,
    thread,
    reply,
    mock_post_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "split", "post": reply.id},
    )
    assert_contains(response, "Split post")
    assert_contains(response, "Category")
    assert_contains(response, "Title")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "split",
            "post": reply.id,
            "moderation-category": default_category.id,
            "moderation-redirect_to": "new",
            "confirm": "true",
        },
    )
    assert_contains(response, "This field is required.")

    reply.refresh_from_db()
    assert reply.thread == thread

    assert not ThreadUpdate.objects.exists()

    mock_post_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_split_post_moderation_action_validates_thread_title(
    moderator_client,
    default_category,
    thread,
    reply,
    mock_post_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "split", "post": reply.id},
    )
    assert_contains(response, "Split post")
    assert_contains(response, "Category")
    assert_contains(response, "Title")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "split",
            "post": reply.id,
            "moderation-category": default_category.id,
            "moderation-title": "Q",
            "moderation-redirect_to": "new",
            "confirm": "true",
        },
    )
    assert_contains(response, "Thread title should be at least 5 characters long")

    reply.refresh_from_db()
    assert reply.thread == thread

    assert not ThreadUpdate.objects.exists()

    mock_post_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_move_post_moderation_action_moves_post(
    moderator_client,
    default_category,
    thread,
    other_thread,
    reply,
    mock_post_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "move", "post": reply.id},
    )
    assert_contains(response, "Move post")
    assert_contains(response, "Target thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "move",
            "post": reply.id,
            "moderation-target_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-redirect_to": "current",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.replies == 0

    other_thread.refresh_from_db()
    assert other_thread.replies == 1

    reply.refresh_from_db()
    assert reply.thread == other_thread

    ThreadUpdate.objects.get(
        thread=other_thread,
        action=ThreadUpdateActionName.MOVED_POSTS_FROM,
    )
    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.MOVED_POSTS_TO,
    )

    mock_post_synchronize_categories.delay.assert_called_once_with(
        [default_category.id]
    )


def test_thread_detail_view_move_post_moderation_action_moves_post_in_htmx(
    moderator_client,
    default_category,
    thread,
    other_thread,
    reply,
    mock_post_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "move", "post": reply.id},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Target thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "move",
            "post": reply.id,
            "moderation-target_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-redirect_to": "current",
            "confirm": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200

    thread.refresh_from_db()
    assert thread.replies == 0

    other_thread.refresh_from_db()
    assert other_thread.replies == 1

    reply.refresh_from_db()
    assert reply.thread == other_thread

    ThreadUpdate.objects.get(
        thread=other_thread,
        action=ThreadUpdateActionName.MOVED_POSTS_FROM,
    )
    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.MOVED_POSTS_TO,
    )

    mock_post_synchronize_categories.delay.assert_called_once_with(
        [default_category.id]
    )


def test_thread_detail_view_move_post_moderation_action_moves_post_with_redirect_to_target_thread(
    moderator_client,
    default_category,
    thread,
    other_thread,
    reply,
    mock_post_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "move", "post": reply.id},
    )
    assert_contains(response, "Move post")
    assert_contains(response, "Target thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "move",
            "post": reply.id,
            "moderation-target_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-redirect_to": "target",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread",
        kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
    )

    thread.refresh_from_db()
    assert thread.replies == 0

    other_thread.refresh_from_db()
    assert other_thread.replies == 1

    reply.refresh_from_db()
    assert reply.thread == other_thread

    ThreadUpdate.objects.get(
        thread=other_thread,
        action=ThreadUpdateActionName.MOVED_POSTS_FROM,
    )
    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.MOVED_POSTS_TO,
    )

    mock_post_synchronize_categories.delay.assert_called_once_with(
        [default_category.id]
    )


def test_thread_detail_view_move_post_moderation_action_validates_target_thread_link(
    moderator_client,
    thread,
    other_thread,
    reply,
    mock_post_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "move", "post": reply.id},
    )
    assert_contains(response, "Move post")
    assert_contains(response, "Target thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "move",
            "post": reply.id,
            "moderation-target_thread": reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-redirect_to": "target",
            "confirm": "true",
        },
    )
    assert_contains(response, "Enter a valid link.")

    thread.refresh_from_db()
    assert thread.replies == 1

    other_thread.refresh_from_db()
    assert other_thread.replies == 0

    reply.refresh_from_db()
    assert reply.thread == thread

    assert not ThreadUpdate.objects.exists()

    mock_post_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_move_post_moderation_action_validates_target_thread_is_different_thread(
    moderator_client,
    thread,
    other_thread,
    reply,
    mock_post_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "move", "post": reply.id},
    )
    assert_contains(response, "Move post")
    assert_contains(response, "Target thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "move",
            "post": reply.id,
            "moderation-target_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": thread.id, "slug": thread.slug},
            ),
            "moderation-redirect_to": "target",
            "confirm": "true",
        },
    )
    assert_contains(response, "Can&#x27;t move posts to the same thread.")

    thread.refresh_from_db()
    assert thread.replies == 1

    other_thread.refresh_from_db()
    assert other_thread.replies == 0

    reply.refresh_from_db()
    assert reply.thread == thread

    assert not ThreadUpdate.objects.exists()

    mock_post_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_move_post_moderation_action_validates_target_thread_exists(
    moderator_client,
    thread,
    other_thread,
    reply,
    mock_post_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "move", "post": reply.id},
    )
    assert_contains(response, "Move post")
    assert_contains(response, "Target thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "move",
            "post": reply.id,
            "moderation-target_thread": f"http://testserver/t/other-thread/{max(thread.id, other_thread.id) + 1}/",
            "moderation-redirect_to": "target",
            "confirm": "true",
        },
    )
    assert_contains(
        response,
        "Thread doesn&#x27;t exist or you don&#x27;t have permission to see it.",
    )

    thread.refresh_from_db()
    assert thread.replies == 1

    other_thread.refresh_from_db()
    assert other_thread.replies == 0

    reply.refresh_from_db()
    assert reply.thread == thread

    assert not ThreadUpdate.objects.exists()

    mock_post_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_move_post_moderation_action_validates_target_thread_is_not_private_thread(
    thread_factory,
    moderator_client,
    thread,
    user_private_thread,
    reply,
    mock_post_synchronize_categories,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "move", "post": reply.id},
    )
    assert_contains(response, "Move post")
    assert_contains(response, "Target thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "move",
            "post": reply.id,
            "moderation-target_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={
                    "thread_id": user_private_thread.id,
                    "slug": user_private_thread.slug,
                },
            ),
            "moderation-redirect_to": "target",
            "confirm": "true",
        },
    )
    assert_contains(
        response,
        "Thread doesn&#x27;t exist or you don&#x27;t have permission to see it.",
    )

    thread.refresh_from_db()
    assert thread.replies == 1

    user_private_thread.refresh_from_db()
    assert user_private_thread.replies == 0

    reply.refresh_from_db()
    assert reply.thread == thread

    assert not ThreadUpdate.objects.exists()

    mock_post_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_move_post_moderation_action_validates_target_thread_is_visible(
    thread_factory,
    moderator_client,
    sibling_category,
    thread,
    reply,
    mock_post_synchronize_categories,
):
    other_thread = thread_factory(sibling_category, starter="DeletedUser")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "move", "post": reply.id},
    )
    assert_contains(response, "Move post")
    assert_contains(response, "Target thread link")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "move",
            "post": reply.id,
            "moderation-target_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-redirect_to": "target",
            "confirm": "true",
        },
    )
    assert_contains(
        response,
        "Thread doesn&#x27;t exist or you don&#x27;t have permission to see it.",
    )

    thread.refresh_from_db()
    assert thread.replies == 1

    other_thread.refresh_from_db()
    assert other_thread.replies == 0

    reply.refresh_from_db()
    assert reply.thread == thread

    assert not ThreadUpdate.objects.exists()

    mock_post_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_move_post_moderation_action_validates_target_thread_can_be_moderated(
    thread_factory,
    user_client,
    user,
    members_group,
    sibling_category,
    thread,
    reply,
    mock_post_synchronize_categories,
):
    grant_category_group_permissions(
        sibling_category,
        members_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    other_thread = thread_factory(sibling_category, starter="DeletedUser")

    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "move", "post": reply.id},
    )
    assert_contains(response, "Move post")
    assert_contains(response, "Target thread link")

    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "move",
            "post": reply.id,
            "moderation-target_thread": "http://testserver"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-redirect_to": "target",
            "confirm": "true",
        },
    )
    assert_contains(response, "You can&#x27;t moderate this thread.")

    thread.refresh_from_db()
    assert thread.replies == 1

    other_thread.refresh_from_db()
    assert other_thread.replies == 0

    reply.refresh_from_db()
    assert reply.thread == thread

    assert not ThreadUpdate.objects.exists()

    mock_post_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_merge_post_moderation_action_merges_other_post_into_first_post(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    default_category,
    user_thread,
    mock_post_synchronize_categories,
):
    current_post = user_thread.first_post
    other_post = thread_reply_factory(user_thread, poster=user, original="Other body")

    current_post_content = current_post.original

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_not_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:thread-post",
                kwargs={
                    "thread_id": user_thread.id,
                    "slug": user_thread.slug,
                    "post_id": other_post.id,
                },
            ),
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        )
        + f"#post-{current_post.id}"
    )

    current_post.refresh_from_db()
    assert current_post.original == f"{current_post_content}\n\nOther body"
    assert not current_post.last_edit_reason

    post_edit = PostEdit.objects.get(post=current_post)
    assert post_edit.user == moderator
    assert not post_edit.edit_reason
    assert post_edit.old_content == current_post_content
    assert post_edit.new_content == f"{current_post_content}\n\nOther body"

    with pytest.raises(Post.DoesNotExist):
        other_post.refresh_from_db()

    mock_post_synchronize_categories.delay.assert_called_with([default_category.id])


def test_thread_detail_view_merge_post_moderation_action_merges_other_post_into_first_post_in_htmx(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    default_category,
    user_thread,
    mock_post_synchronize_categories,
):
    current_post = user_thread.first_post
    other_post = thread_reply_factory(user_thread, poster=user, original="Other body")

    current_post_content = current_post.original

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {"post_moderation": "merge", "post": current_post.id},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Other post link")
    assert_not_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:thread-post",
                kwargs={
                    "thread_id": user_thread.id,
                    "slug": user_thread.slug,
                    "post_id": other_post.id,
                },
            ),
            "confirm": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 201
    assert response["hx-refresh"] == "true"

    current_post.refresh_from_db()
    assert current_post.original == f"{current_post_content}\n\nOther body"
    assert not current_post.last_edit_reason

    post_edit = PostEdit.objects.get(post=current_post)
    assert post_edit.user == moderator
    assert not post_edit.edit_reason
    assert post_edit.old_content == current_post_content
    assert post_edit.new_content == f"{current_post_content}\n\nOther body"

    with pytest.raises(Post.DoesNotExist):
        other_post.refresh_from_db()

    mock_post_synchronize_categories.delay.assert_called_with([default_category.id])


def test_thread_detail_view_merge_post_moderation_action_merges_current_post_into_other(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    default_category,
    user_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_thread, poster=user, original="Current body"
    )
    other_post = thread_reply_factory(user_thread, poster=user, original="Other body")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:thread-post",
                kwargs={
                    "thread_id": user_thread.id,
                    "slug": user_thread.slug,
                    "post_id": other_post.id,
                },
            ),
            "moderation-direction": "other",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        )
        + f"#post-{other_post.id}"
    )

    other_post.refresh_from_db()
    assert other_post.original == "Current body\n\nOther body"
    assert not other_post.last_edit_reason

    post_edit = PostEdit.objects.get(post=other_post)
    assert post_edit.user == moderator
    assert not post_edit.edit_reason
    assert post_edit.old_content == "Other body"
    assert post_edit.new_content == "Current body\n\nOther body"

    with pytest.raises(Post.DoesNotExist):
        current_post.refresh_from_db()

    mock_post_synchronize_categories.delay.assert_called_with([default_category.id])


def test_thread_detail_view_merge_post_moderation_action_merges_current_post_into_other_in_htmx(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    default_category,
    user_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_thread, poster=user, original="Current body"
    )
    other_post = thread_reply_factory(user_thread, poster=user, original="Other body")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {"post_moderation": "merge", "post": current_post.id},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:thread-post",
                kwargs={
                    "thread_id": user_thread.id,
                    "slug": user_thread.slug,
                    "post_id": other_post.id,
                },
            ),
            "moderation-direction": "other",
            "confirm": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 201
    assert response["hx-refresh"] == "true"

    other_post.refresh_from_db()
    assert other_post.original == "Current body\n\nOther body"
    assert not other_post.last_edit_reason

    post_edit = PostEdit.objects.get(post=other_post)
    assert post_edit.user == moderator
    assert not post_edit.edit_reason
    assert post_edit.old_content == "Other body"
    assert post_edit.new_content == "Current body\n\nOther body"

    with pytest.raises(Post.DoesNotExist):
        current_post.refresh_from_db()

    mock_post_synchronize_categories.delay.assert_called_with([default_category.id])


def test_thread_detail_view_merge_post_moderation_action_merges_other_post_into_current(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    default_category,
    user_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_thread, poster=user, original="Current body"
    )
    other_post = thread_reply_factory(user_thread, poster=user, original="Other body")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:thread-post",
                kwargs={
                    "thread_id": user_thread.id,
                    "slug": user_thread.slug,
                    "post_id": other_post.id,
                },
            ),
            "moderation-direction": "current",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        )
        + f"#post-{current_post.id}"
    )

    current_post.refresh_from_db()
    assert current_post.original == "Current body\n\nOther body"
    assert not current_post.last_edit_reason

    post_edit = PostEdit.objects.get(post=current_post)
    assert post_edit.user == moderator
    assert not post_edit.edit_reason
    assert post_edit.old_content == "Current body"
    assert post_edit.new_content == "Current body\n\nOther body"

    with pytest.raises(Post.DoesNotExist):
        other_post.refresh_from_db()

    mock_post_synchronize_categories.delay.assert_called_with([default_category.id])


def test_thread_detail_view_merge_post_moderation_action_merges_other_post_into_current_in_htmx(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    default_category,
    user_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_thread, poster=user, original="Current body"
    )
    other_post = thread_reply_factory(user_thread, poster=user, original="Other body")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {"post_moderation": "merge", "post": current_post.id},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:thread-post",
                kwargs={
                    "thread_id": user_thread.id,
                    "slug": user_thread.slug,
                    "post_id": other_post.id,
                },
            ),
            "moderation-direction": "current",
            "confirm": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 201
    assert response["hx-refresh"] == "true"

    current_post.refresh_from_db()
    assert current_post.original == "Current body\n\nOther body"
    assert not current_post.last_edit_reason

    post_edit = PostEdit.objects.get(post=current_post)
    assert post_edit.user == moderator
    assert not post_edit.edit_reason
    assert post_edit.old_content == "Current body"
    assert post_edit.new_content == "Current body\n\nOther body"

    with pytest.raises(Post.DoesNotExist):
        other_post.refresh_from_db()

    mock_post_synchronize_categories.delay.assert_called_with([default_category.id])


def test_thread_detail_view_merge_post_moderation_action_merges_posts_with_merge_reason(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    default_category,
    user_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_thread, poster=user, original="Current body"
    )
    other_post = thread_reply_factory(user_thread, poster=user, original="Other body")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:thread-post",
                kwargs={
                    "thread_id": user_thread.id,
                    "slug": user_thread.slug,
                    "post_id": other_post.id,
                },
            ),
            "moderation-direction": "current",
            "moderation-edit_reason": "Test merge",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        )
        + f"#post-{current_post.id}"
    )

    current_post.refresh_from_db()
    assert current_post.original == "Current body\n\nOther body"
    assert current_post.last_edit_reason == "Test merge"

    post_edit = PostEdit.objects.get(post=current_post)
    assert post_edit.user == moderator
    assert post_edit.edit_reason == "Test merge"
    assert post_edit.old_content == "Current body"
    assert post_edit.new_content == "Current body\n\nOther body"

    with pytest.raises(Post.DoesNotExist):
        other_post.refresh_from_db()

    mock_post_synchronize_categories.delay.assert_called_with([default_category.id])


def test_thread_detail_view_merge_post_moderation_action_merges_other_post_into_solution(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    default_category,
    user_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_thread, poster=user, original="Current body"
    )
    other_post = thread_reply_factory(user_thread, poster=user, original="Other body")

    select_thread_solution(user_thread, current_post, moderator)

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:thread-post",
                kwargs={
                    "thread_id": user_thread.id,
                    "slug": user_thread.slug,
                    "post_id": other_post.id,
                },
            ),
            "moderation-direction": "current",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        )
        + f"#post-{current_post.id}"
    )

    user_thread.refresh_from_db()
    assert user_thread.solution == current_post

    current_post.refresh_from_db()
    assert current_post.original == "Current body\n\nOther body"
    assert not current_post.last_edit_reason

    post_edit = PostEdit.objects.get(post=current_post)
    assert post_edit.user == moderator
    assert not post_edit.edit_reason
    assert post_edit.old_content == "Current body"
    assert post_edit.new_content == "Current body\n\nOther body"

    with pytest.raises(Post.DoesNotExist):
        other_post.refresh_from_db()

    mock_post_synchronize_categories.delay.assert_called_with([default_category.id])


def test_thread_detail_view_merge_post_moderation_action_merges_solution_into_current_post(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    default_category,
    user_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_thread, poster=user, original="Current body"
    )
    other_post = thread_reply_factory(user_thread, poster=user, original="Other body")

    select_thread_solution(user_thread, other_post, moderator)

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:thread-post",
                kwargs={
                    "thread_id": user_thread.id,
                    "slug": user_thread.slug,
                    "post_id": other_post.id,
                },
            ),
            "moderation-direction": "current",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        )
        + f"#post-{current_post.id}"
    )

    user_thread.refresh_from_db()
    assert user_thread.solution == current_post

    current_post.refresh_from_db()
    assert current_post.original == "Current body\n\nOther body"
    assert not current_post.last_edit_reason

    post_edit = PostEdit.objects.get(post=current_post)
    assert post_edit.user == moderator
    assert not post_edit.edit_reason
    assert post_edit.old_content == "Current body"
    assert post_edit.new_content == "Current body\n\nOther body"

    with pytest.raises(Post.DoesNotExist):
        other_post.refresh_from_db()

    mock_post_synchronize_categories.delay.assert_called_with([default_category.id])


def test_thread_detail_view_merge_post_moderation_action_merges_posts_with_attachments(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    default_category,
    user_thread,
    text_attachment,
    image_attachment,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_thread, poster=user, original="Current body"
    )
    other_post = thread_reply_factory(user_thread, poster=user, original="Other body")

    text_attachment.associate_with_post(current_post)
    text_attachment.save()

    image_attachment.associate_with_post(other_post)
    image_attachment.save()

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:thread-post",
                kwargs={
                    "thread_id": user_thread.id,
                    "slug": user_thread.slug,
                    "post_id": other_post.id,
                },
            ),
            "moderation-direction": "current",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        )
        + f"#post-{current_post.id}"
    )

    current_post.refresh_from_db()
    assert current_post.original == "Current body\n\nOther body"
    assert not current_post.last_edit_reason

    text_attachment.refresh_from_db()
    assert text_attachment.post == current_post

    image_attachment.refresh_from_db()
    assert image_attachment.post == current_post

    post_edit = PostEdit.objects.get(post=current_post)
    assert post_edit.user == moderator
    assert not post_edit.edit_reason
    assert post_edit.old_content == "Current body"
    assert post_edit.new_content == "Current body\n\nOther body"
    assert post_edit.attachments[0]["id"] == image_attachment.id
    assert post_edit.attachments[0]["change"] == "+"
    assert post_edit.attachments[1]["id"] == text_attachment.id
    assert post_edit.attachments[1]["change"] == "="

    with pytest.raises(Post.DoesNotExist):
        other_post.refresh_from_db()

    mock_post_synchronize_categories.delay.assert_called_with([default_category.id])


def test_thread_detail_view_merge_post_moderation_action_merges_posts_using_global_post_link(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    default_category,
    user_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_thread, poster=user, original="Current body"
    )
    other_post = thread_reply_factory(user_thread, poster=user, original="Other body")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse("misago:post", kwargs={"post_id": other_post.id}),
            "moderation-direction": "current",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        )
        + f"#post-{current_post.id}"
    )

    current_post.refresh_from_db()
    assert current_post.original == "Current body\n\nOther body"
    assert not current_post.last_edit_reason

    post_edit = PostEdit.objects.get(post=current_post)
    assert post_edit.user == moderator
    assert not post_edit.edit_reason
    assert post_edit.old_content == "Current body"
    assert post_edit.new_content == "Current body\n\nOther body"

    with pytest.raises(Post.DoesNotExist):
        other_post.refresh_from_db()

    mock_post_synchronize_categories.delay.assert_called_with([default_category.id])


def test_thread_detail_view_merge_post_moderation_action_validates_other_post_link(
    thread_reply_factory,
    moderator_client,
    user,
    user_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_thread, poster=user, original="Current body"
    )
    other_post = thread_reply_factory(user_thread, poster=user, original="Other body")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": reverse(
                "misago:post", kwargs={"post_id": other_post.id}
            ),
            "moderation-direction": "current",
            "confirm": "true",
        },
    )
    assert_contains(response, "Enter a valid link.")

    current_post.refresh_from_db()
    assert current_post.original == "Current body"

    other_post.refresh_from_db()
    assert other_post.original == "Other body"

    mock_post_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_merge_post_moderation_action_validates_thread_post_link_post_exists(
    thread_reply_factory,
    moderator_client,
    user,
    user_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_thread, poster=user, original="Current body"
    )

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:thread-post",
                kwargs={
                    "thread_id": user_thread.id,
                    "slug": user_thread.slug,
                    "post_id": current_post.id + 1,
                },
            ),
            "moderation-direction": "current",
            "confirm": "true",
        },
    )
    assert_contains(response, "Post doesn&#x27;t exist")

    current_post.refresh_from_db()
    assert current_post.original == "Current body"

    mock_post_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_merge_post_moderation_action_validates_thread_post_link_is_current_thread(
    thread_reply_factory,
    moderator_client,
    user,
    thread,
    user_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_thread, poster=user, original="Current body"
    )
    other_post = thread_reply_factory(thread, poster=user, original="Other body")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:thread-post",
                kwargs={
                    "thread_id": thread.id,
                    "slug": thread.slug,
                    "post_id": other_post.id,
                },
            ),
            "moderation-direction": "current",
            "confirm": "true",
        },
    )
    assert_contains(response, "Enter a link to a post in the current thread.")

    current_post.refresh_from_db()
    assert current_post.original == "Current body"

    other_post.refresh_from_db()
    assert other_post.original == "Other body"

    mock_post_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_merge_post_moderation_action_validates_thread_post_link_is_different_post(
    thread_reply_factory,
    moderator_client,
    user,
    user_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_thread, poster=user, original="Current body"
    )

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:thread-post",
                kwargs={
                    "thread_id": user_thread.id,
                    "slug": user_thread.slug,
                    "post_id": current_post.id,
                },
            ),
            "moderation-direction": "current",
            "confirm": "true",
        },
    )
    assert_contains(response, "Can&#x27;t merge a post with itself.")

    current_post.refresh_from_db()
    assert current_post.original == "Current body"

    mock_post_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_merge_post_moderation_action_validates_global_post_link_post_exists(
    thread_reply_factory,
    moderator_client,
    user,
    user_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_thread, poster=user, original="Current body"
    )

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse("misago:post", kwargs={"post_id": current_post.id + 1}),
            "moderation-direction": "current",
            "confirm": "true",
        },
    )
    assert_contains(response, "Post doesn&#x27;t exist")

    current_post.refresh_from_db()
    assert current_post.original == "Current body"

    mock_post_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_merge_post_moderation_action_validates_global_post_link_post_permission(
    thread_factory,
    thread_reply_factory,
    moderator_client,
    user,
    sibling_category,
    user_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_thread, poster=user, original="Current body"
    )
    other_post = thread_factory(sibling_category).first_post

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse("misago:post", kwargs={"post_id": other_post.id}),
            "moderation-direction": "current",
            "confirm": "true",
        },
    )
    assert_contains(response, "Post doesn&#x27;t exist")

    current_post.refresh_from_db()
    assert current_post.original == "Current body"

    mock_post_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_merge_post_moderation_action_validates_global_post_link_post_is_in_current_thread(
    thread_reply_factory,
    moderator_client,
    user,
    thread,
    user_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_thread, poster=user, original="Current body"
    )
    other_post = thread_reply_factory(thread, poster=user, original="Other body")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse("misago:post", kwargs={"post_id": other_post.id}),
            "moderation-direction": "current",
            "confirm": "true",
        },
    )
    assert_contains(response, "Post doesn&#x27;t exist in this thread")

    current_post.refresh_from_db()
    assert current_post.original == "Current body"

    other_post.refresh_from_db()
    assert other_post.original == "Other body"

    mock_post_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_merge_post_moderation_action_validates_global_post_link_post_is_different_post(
    thread_reply_factory,
    moderator_client,
    user,
    user_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_thread, poster=user, original="Current body"
    )

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse("misago:post", kwargs={"post_id": current_post.id}),
            "moderation-direction": "current",
            "confirm": "true",
        },
    )
    assert_contains(response, "Can&#x27;t merge a post with itself.")

    current_post.refresh_from_db()
    assert current_post.original == "Current body"

    mock_post_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_merge_post_moderation_action_validates_first_post_merge_into_current_post(
    thread_reply_factory,
    moderator_client,
    user,
    user_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_thread, poster=user, original="Current body"
    )
    first_post_content = user_thread.first_post.original

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:thread-post",
                kwargs={
                    "thread_id": user_thread.id,
                    "slug": user_thread.slug,
                    "post_id": user_thread.first_post.id,
                },
            ),
            "moderation-direction": "current",
            "confirm": "true",
        },
    )
    assert_contains(
        response, "Thread&#x27;s first post can&#x27;t be merged into another post"
    )

    current_post.refresh_from_db()
    assert current_post.original == "Current body"

    user_thread.first_post.refresh_from_db()
    assert user_thread.first_post.original == first_post_content

    mock_post_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_merge_post_moderation_action_validates_posts_are_by_same_user(
    thread_reply_factory,
    moderator_client,
    user,
    other_user,
    user_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_thread, poster=user, original="Current body"
    )
    other_post = thread_reply_factory(
        user_thread, poster=other_user, original="Other body"
    )

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:thread-post",
                kwargs={
                    "thread_id": user_thread.id,
                    "slug": user_thread.slug,
                    "post_id": other_post.id,
                },
            ),
            "moderation-direction": "current",
            "confirm": "true",
        },
    )
    assert_contains(response, "Merged posts must belong to the same user.")

    current_post.refresh_from_db()
    assert current_post.original == "Current body"

    other_post.refresh_from_db()
    assert other_post.original == "Other body"

    mock_post_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_merge_post_moderation_action_validates_posts_are_by_same_deleted_user(
    thread_reply_factory,
    moderator_client,
    user_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_thread, poster="Bob", original="Current body"
    )
    other_post = thread_reply_factory(
        user_thread, poster="Elice", original="Other body"
    )

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:thread",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:thread-post",
                kwargs={
                    "thread_id": user_thread.id,
                    "slug": user_thread.slug,
                    "post_id": other_post.id,
                },
            ),
            "moderation-direction": "current",
            "confirm": "true",
        },
    )
    assert_contains(response, "Merged posts must belong to the same user.")

    current_post.refresh_from_db()
    assert current_post.original == "Current body"

    other_post.refresh_from_db()
    assert other_post.original == "Other body"

    mock_post_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_delete_post_moderation_action_deletes_post(
    moderator_client, default_category, thread, reply, mock_post_synchronize_categories
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "delete", "post": reply.id},
    )
    assert_contains(response, "Delete post")
    assert_contains(response, "Are you sure you want to delete this post?")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "delete",
            "post": reply.id,
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.DELETED_POSTS,
    )

    mock_post_synchronize_categories.delay.assert_called_with([default_category.id])


def test_thread_detail_view_delete_post_moderation_action_deletes_post_in_htmx(
    moderator_client, default_category, thread, reply, mock_post_synchronize_categories
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "delete", "post": reply.id},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Are you sure you want to delete this post?")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "delete",
            "post": reply.id,
            "confirm": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.DELETED_POSTS,
    )

    mock_post_synchronize_categories.delay.assert_called_with([default_category.id])
