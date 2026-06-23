import pytest
from django.urls import reverse

from ...permissions.enums import CategoryPermission
from ...permissions.models import Moderator
from ...polls.models import Poll
from ...solutions.select import select_thread_solution
from ...test import UNORDERED, assert_contains
from ...testutils import grant_category_group_permissions
from ...threadupdates.enums import ThreadUpdateActionName
from ...threadupdates.models import ThreadUpdate
from ..enums import ThreadPinned
from ..models import Thread


@pytest.fixture
def mock_synchronize_categories(mocker):
    return mocker.patch("misago.moderation.thread.synchronize_categories")


@pytest.fixture
def mock_delete_duplicate_watched_threads(mocker):
    return mocker.patch("misago.moderation.thread.delete_duplicate_watched_threads")


def test_thread_detail_view_executes_pin_everywhere_thread_moderation_action(
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


def test_thread_detail_view_executes_pin_category_thread_moderation_action(
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


def test_thread_detail_view_executes_unpin_pinned_everywhere_thread_moderation_action(
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


def test_thread_detail_view_executes_unpin_pinned_category_thread_moderation_action(
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


def test_thread_detail_view_executes_lock_thread_moderation_action(
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


def test_thread_detail_view_executes_unlock_thread_moderation_action(
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


def test_thread_detail_view_executes_hide_thread_moderation_action(
    moderator_client, moderator, thread, mock_synchronize_categories
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "hide"},
    )
    assert_contains(response, "Reason for hiding")
    assert_contains(response, "Hide thread")

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

    mock_synchronize_categories.delay.assert_called_once_with([thread.category_id])


def test_thread_detail_view_executes_unhide_thread_moderation_action(
    moderator_client, thread, mock_synchronize_categories
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

    mock_synchronize_categories.delay.assert_called_once_with([thread.category_id])


def test_thread_detail_view_executes_approve_thread_moderation_action(
    moderator_client, thread, mock_synchronize_categories
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

    mock_synchronize_categories.delay.assert_called_once_with([thread.category_id])


def test_thread_detail_view_executes_require_reply_approval_thread_moderation_action(
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


def test_thread_detail_view_executes_remove_reply_approval_thread_moderation_action(
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


def test_thread_detail_view_executes_move_thread_moderation_action(
    thread_factory,
    moderator_client,
    moderators_group,
    default_category,
    sibling_category,
    mock_synchronize_categories,
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

    mock_synchronize_categories.delay.assert_called_once_with(
        UNORDERED([default_category.id, sibling_category.id])
    )


def test_thread_detail_view_move_moderation_action_requires_category(
    thread_factory, moderator_client, default_category, mock_synchronize_categories
):
    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "move"},
    )
    assert_contains(response, "Move thread")

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

    mock_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_move_moderation_action_validates_category_value(
    thread_factory, moderator_client, default_category, mock_synchronize_categories
):
    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "move"},
    )
    assert_contains(response, "Move thread")

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

    mock_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_move_moderation_action_validates_category_permission(
    thread_factory,
    moderator_client,
    moderators_group,
    default_category,
    sibling_category,
    mock_synchronize_categories,
):
    grant_category_group_permissions(
        sibling_category,
        moderators_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "move"},
    )
    assert_contains(response, "Move thread")

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

    mock_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_move_moderation_action_validates_category_type(
    thread_factory,
    moderator_client,
    moderators_group,
    default_category,
    sibling_category,
    mock_synchronize_categories,
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

    mock_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_move_moderation_action_validates_category_is_new(
    thread_factory, moderator_client, default_category, mock_synchronize_categories
):
    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "move"},
    )
    assert_contains(response, "Move thread")

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

    mock_synchronize_categories.delay.assert_not_called()


def test_thread_detail_view_merge_moderation_action_merges_current_thread_into_other(
    moderator_client,
    default_category,
    thread,
    other_thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
    )
    assert_contains(response, "Merge thread")

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

    mock_synchronize_categories.delay.assert_called_once_with([default_category.id])
    mock_delete_duplicate_watched_threads.delay.assert_called_once_with(other_thread.id)


def test_thread_detail_view_merge_moderation_action_merges_current_thread_into_other_in_htmx(
    moderator_client,
    default_category,
    thread,
    other_thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Merge")

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

    mock_synchronize_categories.delay.assert_called_once_with([default_category.id])
    mock_delete_duplicate_watched_threads.delay.assert_called_once_with(other_thread.id)


def test_thread_detail_view_merge_moderation_action_merges_other_thread_into_current(
    moderator_client,
    default_category,
    thread,
    other_thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
    )
    assert_contains(response, "Merge thread")

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

    mock_synchronize_categories.delay.assert_called_once_with([default_category.id])
    mock_delete_duplicate_watched_threads.delay.assert_called_once_with(thread.id)


def test_thread_detail_view_merge_moderation_action_merges_other_thread_into_current_in_htmx(
    moderator_client,
    default_category,
    thread,
    other_thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Merge")

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

    mock_synchronize_categories.delay.assert_called_once_with([default_category.id])
    mock_delete_duplicate_watched_threads.delay.assert_called_once_with(thread.id)


def test_thread_detail_view_merge_moderation_action_merges_threads_without_conflicts(
    thread_reply_factory,
    poll_factory,
    moderator_client,
    default_category,
    thread,
    other_thread,
    mock_synchronize_categories,
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

    mock_synchronize_categories.delay.assert_called_once_with([default_category.id])
    mock_delete_duplicate_watched_threads.delay.assert_called_once_with(other_thread.id)


def test_thread_detail_view_merge_moderation_action_merges_threads_with_conflicts(
    thread_reply_factory,
    poll_factory,
    moderator_client,
    default_category,
    thread,
    other_thread,
    mock_synchronize_categories,
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

    mock_synchronize_categories.delay.assert_called_once_with([default_category.id])
    mock_delete_duplicate_watched_threads.delay.assert_called_once_with(other_thread.id)


def test_thread_detail_view_merge_moderation_action_requires_other_thread_link(
    moderator_client,
    thread,
    other_thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
    )
    assert_contains(response, "Merge thread")

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

    mock_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_thread_detail_view_merge_moderation_action_validates_other_thread_link_has_hostname(
    moderator_client,
    thread,
    other_thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
    )
    assert_contains(response, "Merge thread")

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

    mock_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_thread_detail_view_merge_moderation_action_validates_other_thread_link_has_path(
    moderator_client,
    thread,
    other_thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
    )
    assert_contains(response, "Merge thread")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "merge",
            "moderation-other_thread": "http://localhost/",
            "moderation-direction": "this",
            "confirm": "true",
        },
    )
    assert_contains(response, "Enter a valid link.")

    thread.refresh_from_db()
    other_thread.refresh_from_db()

    assert not ThreadUpdate.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_thread_detail_view_merge_moderation_action_validates_other_thread_link_has_site_hostname(
    moderator_client,
    thread,
    other_thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
    )
    assert_contains(response, "Merge thread")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "merge",
            "moderation-other_thread": "http://misago-project.org/"
            + reverse(
                "misago:thread",
                kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
            ),
            "moderation-direction": "this",
            "confirm": "true",
        },
    )
    assert_contains(response, "Enter a link to this site.")

    thread.refresh_from_db()
    other_thread.refresh_from_db()

    assert not ThreadUpdate.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_thread_detail_view_merge_moderation_action_validates_other_thread_link_has_valid_url(
    moderator_client,
    thread,
    other_thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
    )
    assert_contains(response, "Merge thread")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "merge",
            "moderation-other_thread": "http://testserver/invalid-url/",
            "moderation-direction": "this",
            "confirm": "true",
        },
    )
    assert_contains(response, "Enter a link to this site.")

    thread.refresh_from_db()
    other_thread.refresh_from_db()

    assert not ThreadUpdate.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_thread_detail_view_merge_moderation_action_validates_other_thread_link_is_thread_link(
    moderator_client,
    thread,
    other_thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
    )
    assert_contains(response, "Merge thread")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "merge",
            "moderation-other_thread": "http://testserver"
            + reverse("misago:account-settings"),
            "moderation-direction": "this",
            "confirm": "true",
        },
    )
    assert_contains(response, "This link doesn&#x27;t point to a valid thread.")

    thread.refresh_from_db()
    other_thread.refresh_from_db()

    assert not ThreadUpdate.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_thread_detail_view_merge_moderation_action_validates_other_thread_is_different_thread(
    moderator_client,
    thread,
    other_thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
    )
    assert_contains(response, "Merge thread")

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
    assert_contains(response, "This link doesn&#x27;t point to a different thread.")

    thread.refresh_from_db()
    other_thread.refresh_from_db()

    assert not ThreadUpdate.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_thread_detail_view_merge_moderation_action_validates_other_thread_exists(
    moderator_client,
    thread,
    other_thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
    )
    assert_contains(response, "Merge thread")

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

    mock_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_thread_detail_view_merge_moderation_action_validates_other_thread_is_visible(
    thread_factory,
    moderator_client,
    sibling_category,
    thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    other_thread = thread_factory(sibling_category, starter="DeletedUser")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
    )
    assert_contains(response, "Merge thread")

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

    mock_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_thread_detail_view_merge_moderation_action_validates_other_thread_can_be_moderated(
    thread_factory,
    user_client,
    user,
    members_group,
    sibling_category,
    thread,
    mock_synchronize_categories,
    mock_delete_duplicate_watched_threads,
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    grant_category_group_permissions(
        sibling_category,
        members_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    other_thread = thread_factory(sibling_category, starter="DeletedUser")

    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "merge"},
    )
    assert_contains(response, "Merge thread")

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
    assert_contains(response, "You can&#x27;t moderate the other thread.")

    thread.refresh_from_db()
    other_thread.refresh_from_db()

    assert not ThreadUpdate.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_thread_detail_view_merge_moderation_action_requires_conflict_resolution(
    thread_reply_factory,
    poll_factory,
    moderator_client,
    thread,
    other_thread,
    mock_synchronize_categories,
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

    mock_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_thread_detail_view_merge_moderation_action_validates_conflict_resolution(
    thread_reply_factory,
    poll_factory,
    moderator_client,
    thread,
    other_thread,
    mock_synchronize_categories,
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

    mock_synchronize_categories.delay.assert_not_called()
    mock_delete_duplicate_watched_threads.delay.assert_not_called()


def test_thread_detail_view_executes_delete_thread_moderation_action(
    moderator_client, default_category, thread, mock_synchronize_categories
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

    mock_synchronize_categories.delay.assert_called_once_with([default_category.id])


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


def test_thread_detail_view_executes_lock_post_moderation_action(
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


def test_thread_detail_view_executes_unlock_post_moderation_action(
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
