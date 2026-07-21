import pytest
from django.urls import reverse

from ...postedits.models import PostEdit
from ...privatethreads.members import get_private_thread_members
from ...privatethreads.models import PrivateThreadMember
from ...test import UNORDERED, assert_contains, assert_not_contains
from ...threadevents.enums import ThreadEventActionName
from ...threadevents.models import ThreadEvent
from ...threads.models import Post, Thread


@pytest.fixture
def mock_thread_synchronize_categories(mocker):
    return mocker.patch("misago.moderation.thread.synchronize_categories")


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


def test_private_thread_detail_view_lock_thread_moderation_action_locks_thread(
    moderator_client, moderator, user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "lock"},
    )
    assert_contains(response, "Lock thread")
    assert_contains(response, "Reason for locking")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "thread_moderation": "lock",
            "moderation-lock_reason": "Lorem ipsum",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"thread_id": user_private_thread.id, "slug": user_private_thread.slug},
    )

    user_private_thread.refresh_from_db()
    assert user_private_thread.is_locked
    assert user_private_thread.locked_at
    assert user_private_thread.locked_by == moderator
    assert user_private_thread.locked_by_name == moderator.username
    assert user_private_thread.locked_by_slug == moderator.slug
    assert user_private_thread.lock_reason == "Lorem ipsum"
    assert user_private_thread.has_events

    ThreadEvent.objects.get(
        thread=user_private_thread,
        action=ThreadEventActionName.LOCKED,
    )


def test_private_thread_detail_view_unlock_thread_moderation_action_unlocks_thread(
    moderator_client, user_private_thread
):
    user_private_thread.is_locked = True
    user_private_thread.save()

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "unlock"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )

    user_private_thread.refresh_from_db()
    assert not user_private_thread.is_locked
    assert user_private_thread.has_events

    ThreadEvent.objects.get(
        thread=user_private_thread,
        action=ThreadEventActionName.UNLOCKED,
    )


def test_private_thread_detail_view_hide_thread_moderation_action_hides_thread(
    moderator_client, moderator, user_private_thread, mock_thread_synchronize_categories
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "hide"},
    )
    assert_contains(response, "Hide thread")
    assert_contains(response, "Reason for hiding")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "thread_moderation": "hide",
            "moderation-hide_reason": "Lorem ipsum",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"thread_id": user_private_thread.id, "slug": user_private_thread.slug},
    )

    user_private_thread.refresh_from_db()
    assert user_private_thread.is_hidden
    assert user_private_thread.hidden_at
    assert user_private_thread.hidden_by == moderator
    assert user_private_thread.hidden_by_name == moderator.username
    assert user_private_thread.hidden_by_slug == moderator.slug
    assert user_private_thread.hide_reason == "Lorem ipsum"
    assert user_private_thread.has_events

    ThreadEvent.objects.get(
        thread=user_private_thread,
        action=ThreadEventActionName.HIDDEN,
    )

    mock_thread_synchronize_categories.delay.assert_called_once_with(
        [user_private_thread.category_id]
    )


def test_private_thread_detail_view_unhide_thread_moderation_action_unhides_thread(
    moderator_client, user_private_thread, mock_thread_synchronize_categories
):
    user_private_thread.is_hidden = True
    user_private_thread.save()

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "unhide"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"thread_id": user_private_thread.id, "slug": user_private_thread.slug},
    )

    user_private_thread.refresh_from_db()
    assert not user_private_thread.is_hidden
    assert user_private_thread.hidden_at is None
    assert user_private_thread.hidden_by is None
    assert user_private_thread.hidden_by_name is None
    assert user_private_thread.hidden_by_slug is None
    assert user_private_thread.hide_reason is None
    assert user_private_thread.has_events

    ThreadEvent.objects.get(
        thread=user_private_thread,
        action=ThreadEventActionName.UNHIDDEN,
    )

    mock_thread_synchronize_categories.delay.assert_called_once_with(
        [user_private_thread.category_id]
    )


def test_private_thread_detail_view_ownership_thread_moderation_action_makes_moderator_thread_owner(
    moderator_client,
    user,
    other_user,
    moderator,
    user_private_thread,
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "ownership"},
    )
    assert_contains(response, "Take thread ownership")
    assert_contains(response, "Take ownership of this thread?")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "ownership", "confirm": "true"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"thread_id": user_private_thread.id, "slug": user_private_thread.slug},
    )

    user_private_thread.refresh_from_db()
    assert user_private_thread.has_events

    owner, members = get_private_thread_members(user_private_thread)
    assert owner == moderator
    assert members == [user, other_user, moderator]

    ThreadEvent.objects.get(
        thread=user_private_thread,
        action=ThreadEventActionName.TOOK_OWNERSHIP,
    )


def test_private_thread_detail_view_ownership_thread_moderation_action_makes_moderator_thread_owner_in_htmx(
    moderator_client,
    user,
    other_user,
    moderator,
    user_private_thread,
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "ownership"},
    )
    assert_contains(response, "Take ownership of this thread?")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "ownership", "confirm": "true"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, user.username)
    assert_contains(response, other_user.username)
    assert_contains(response, moderator.username)

    user_private_thread.refresh_from_db()
    assert user_private_thread.has_events

    owner, members = get_private_thread_members(user_private_thread)
    assert owner == moderator
    assert members == [user, other_user, moderator]

    ThreadEvent.objects.get(
        thread=user_private_thread,
        action=ThreadEventActionName.TOOK_OWNERSHIP,
    )


def test_private_thread_detail_view_ownership_thread_moderation_action_makes_moderator_thread_owner_and_member(
    moderator_client,
    user,
    other_user,
    moderator,
    user_private_thread,
):
    PrivateThreadMember.objects.filter(
        thread=user_private_thread, user=moderator
    ).delete()

    user_private_thread.has_unapproved_posts = True
    user_private_thread.save()

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "ownership"},
    )
    assert_contains(response, "Take thread ownership")
    assert_contains(response, "Take ownership of this thread?")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "ownership", "confirm": "true"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"thread_id": user_private_thread.id, "slug": user_private_thread.slug},
    )

    user_private_thread.refresh_from_db()
    assert user_private_thread.has_events

    owner, members = get_private_thread_members(user_private_thread)
    assert owner == moderator
    assert members == [user, other_user, moderator]

    ThreadEvent.objects.get(
        thread=user_private_thread,
        action=ThreadEventActionName.TOOK_OWNERSHIP,
    )


def test_private_thread_detail_view_ownership_thread_moderation_action_makes_moderator_thread_owner_and_member_in_htmx(
    moderator_client,
    user,
    other_user,
    moderator,
    user_private_thread,
):
    PrivateThreadMember.objects.filter(
        thread=user_private_thread, user=moderator
    ).delete()

    user_private_thread.has_unapproved_posts = True
    user_private_thread.save()

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "ownership"},
    )
    assert_contains(response, "Take ownership of this thread?")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "ownership", "confirm": "true"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, user.username)
    assert_contains(response, other_user.username)
    assert_contains(response, moderator.username)

    user_private_thread.refresh_from_db()
    assert user_private_thread.has_events

    owner, members = get_private_thread_members(user_private_thread)
    assert owner == moderator
    assert members == [user, other_user, moderator]

    ThreadEvent.objects.get(
        thread=user_private_thread,
        action=ThreadEventActionName.TOOK_OWNERSHIP,
    )


def test_private_thread_detail_view_approve_thread_moderation_action_approves_thread(
    mocker,
    moderator_client,
    user,
    other_user,
    moderator,
    user_private_thread,
    mock_thread_synchronize_categories,
):
    mock_notify_on_new_private_thread = mocker.patch(
        "misago.moderation.thread.notify_on_new_private_thread"
    )

    user_private_thread.is_unapproved = True
    user_private_thread.save()

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "approve"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"thread_id": user_private_thread.id, "slug": user_private_thread.slug},
    )

    user_private_thread.refresh_from_db()
    assert not user_private_thread.is_unapproved
    assert user_private_thread.has_events

    ThreadEvent.objects.get(
        thread=user_private_thread,
        action=ThreadEventActionName.APPROVED,
    )

    mock_thread_synchronize_categories.delay.assert_called_once_with(
        [user_private_thread.category_id]
    )
    mock_notify_on_new_private_thread.delay.assert_called_once_with(
        user.id, user_private_thread.id, UNORDERED([other_user.id, moderator.id])
    )


def test_private_thread_detail_view_require_reply_approval_thread_moderation_action_sets_thread_require_reply_approval_flag(
    moderator_client, user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "require_reply_approval"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"thread_id": user_private_thread.id, "slug": user_private_thread.slug},
    )

    user_private_thread.refresh_from_db()
    assert user_private_thread.require_reply_approval
    assert user_private_thread.has_events

    ThreadEvent.objects.get(
        thread=user_private_thread,
        action=ThreadEventActionName.REQUIRED_REPLY_APPROVAL,
    )


def test_private_thread_detail_view_remove_reply_approval_thread_moderation_action_removes_thread_require_reply_approval_flag(
    moderator_client, user_private_thread
):
    user_private_thread.require_reply_approval = True
    user_private_thread.save()

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "remove_reply_approval"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"thread_id": user_private_thread.id, "slug": user_private_thread.slug},
    )

    user_private_thread.refresh_from_db()
    assert not user_private_thread.require_reply_approval
    assert user_private_thread.has_events

    ThreadEvent.objects.get(
        thread=user_private_thread,
        action=ThreadEventActionName.REMOVED_REPLY_APPROVAL,
    )


def test_private_thread_detail_view_delete_thread_moderation_action_deletes_thread(
    moderator_client, user_private_thread, mock_thread_synchronize_categories
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "delete", "thread": user_private_thread.id},
    )
    assert_contains(response, "Delete thread")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "thread_moderation": "delete",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:private-thread-list")

    with pytest.raises(Thread.DoesNotExist):
        user_private_thread.refresh_from_db()

    mock_thread_synchronize_categories.delay.assert_called_once_with(
        [user_private_thread.category_id]
    )


def test_private_thread_detail_view_lock_posts_moderation_action_locks_posts(
    thread_reply_factory, moderator_client, moderator, user_private_thread
):
    reply = thread_reply_factory(user_private_thread)

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "lock", "posts": [reply.id]},
    )
    assert_contains(response, "Lock posts")
    assert_contains(response, "Reason for locking")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "posts_moderation": "lock",
            "posts": [reply.id],
            "moderation-lock_reason": "Lorem ipsum",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
        + f"#post-{reply.id}"
    )

    reply.refresh_from_db()
    assert reply.is_locked
    assert reply.locked_at
    assert reply.locked_by == moderator
    assert reply.locked_by_name == moderator.username
    assert reply.locked_by_slug == moderator.slug
    assert reply.lock_reason == "Lorem ipsum"


def test_private_thread_detail_view_lock_posts_moderation_action_validates_posts(
    thread_reply_factory, moderator_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread, is_locked=True)

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "lock", "posts": [reply.id]},
    )
    assert_contains(response, "Posts are already locked.")


def test_private_thread_detail_view_unlock_posts_moderation_action_unlocks_posts(
    thread_reply_factory, moderator_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread, is_locked=True)

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "unlock", "posts": [reply.id]},
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
        + f"#post-{reply.id}"
    )

    reply.refresh_from_db()
    assert not reply.is_locked


def test_private_thread_detail_view_unlock_posts_moderation_action_validates_posts(
    thread_reply_factory, moderator_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread)

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "unlock", "posts": [reply.id]},
    )
    assert_contains(response, "Posts are already unlocked.")


def test_private_thread_detail_view_hide_posts_moderation_action_hides_posts(
    thread_reply_factory, moderator_client, moderator, user_private_thread
):
    reply = thread_reply_factory(user_private_thread)

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "hide", "posts": [reply.id]},
    )
    assert_contains(response, "Hide posts")
    assert_contains(response, "Reason for hiding")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "posts_moderation": "hide",
            "posts": [reply.id],
            "moderation-hide_reason": "Lorem ipsum",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
        + f"#post-{reply.id}"
    )

    reply.refresh_from_db()
    assert reply.is_hidden
    assert reply.hidden_at
    assert reply.hidden_by == moderator
    assert reply.hidden_by_name == moderator.username
    assert reply.hidden_by_slug == moderator.slug
    assert reply.hide_reason == "Lorem ipsum"


def test_private_thread_detail_view_hide_posts_moderation_action_validates_posts(
    thread_reply_factory, moderator_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread, is_hidden=True)

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "hide", "posts": [reply.id]},
    )
    assert_contains(response, "Posts are already hidden.")


def test_private_thread_detail_view_hide_posts_moderation_action_validates_first_post(
    moderator_client, user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "hide", "posts": [user_private_thread.first_post_id]},
    )
    assert_contains(response, "Thread&#x27;s first post can&#x27;t be hidden.")


def test_private_thread_detail_view_unhide_posts_moderation_action_unhides_posts(
    thread_reply_factory, moderator_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread, is_hidden=True)

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "unhide", "posts": [reply.id]},
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
        + f"#post-{reply.id}"
    )

    reply.refresh_from_db()
    assert not reply.is_hidden
    assert reply.hidden_at is None
    assert reply.hidden_by is None
    assert reply.hidden_by_name is None
    assert reply.hidden_by_slug is None
    assert reply.hide_reason is None


def test_private_thread_detail_view_unhide_posts_moderation_action_validates_posts(
    thread_reply_factory, moderator_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread)

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "unhide", "posts": [reply.id]},
    )
    assert_contains(response, "Posts are already unhidden.")


def test_private_thread_detail_view_approve_posts_moderation_action_approves_posts(
    post_factory,
    moderator_client,
    user_private_thread,
    mock_posts_synchronize_categories,
    mock_posts_notify_on_new_thread_reply,
):
    reply = post_factory(user_private_thread, is_unapproved=True)

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "approve", "posts": [reply.id]},
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
        + f"#post-{reply.id}"
    )

    reply.refresh_from_db()
    assert not reply.is_hidden
    assert reply.hidden_at is None
    assert reply.hidden_by is None
    assert reply.hidden_by_name is None
    assert reply.hidden_by_slug is None
    assert reply.hide_reason is None

    mock_posts_synchronize_categories.delay.assert_called_with(
        [user_private_thread.category_id]
    )
    mock_posts_notify_on_new_thread_reply.delay.assert_called_with(reply.id)


def test_private_thread_detail_view_approve_posts_moderation_action_validates_posts(
    thread_reply_factory,
    moderator_client,
    user_private_thread,
    mock_posts_synchronize_categories,
    mock_posts_notify_on_new_thread_reply,
):
    reply = thread_reply_factory(user_private_thread)

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "approve", "posts": [reply.id]},
    )
    assert_contains(response, "Posts are already approved.")

    mock_posts_synchronize_categories.delay.assert_not_called()
    mock_posts_notify_on_new_thread_reply.delay.assert_not_called()


def test_private_thread_detail_view_merge_posts_moderation_action_merges_posts(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    user_private_thread,
    mock_posts_synchronize_categories,
):
    target_post = thread_reply_factory(
        user_private_thread, poster=user, original="Target body"
    )
    other_post = thread_reply_factory(
        user_private_thread, poster=user, original="Other body"
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "merge", "posts": [target_post.id, other_post.id]},
    )
    assert_contains(response, "Merge posts")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "posts_moderation": "merge",
            "posts": [target_post.id, other_post.id],
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
        + f"#post-{target_post.id}"
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

    mock_posts_synchronize_categories.delay.assert_called_with(
        [user_private_thread.category_id]
    )


def test_private_thread_detail_view_merge_posts_moderation_action_merges_posts_in_htmx(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    user_private_thread,
    mock_posts_synchronize_categories,
):
    target_post = thread_reply_factory(
        user_private_thread, poster=user, original="Target body"
    )
    other_post = thread_reply_factory(
        user_private_thread, poster=user, original="Other body"
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "merge", "posts": [target_post.id, other_post.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
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

    mock_posts_synchronize_categories.delay.assert_called_with(
        [user_private_thread.category_id]
    )


def test_private_thread_detail_view_merge_posts_moderation_action_merges_posts_with_merge_reason(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    user_private_thread,
    mock_posts_synchronize_categories,
):
    target_post = thread_reply_factory(
        user_private_thread, poster=user, original="Target body"
    )
    other_post = thread_reply_factory(
        user_private_thread, poster=user, original="Other body"
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "merge", "posts": [target_post.id, other_post.id]},
    )
    assert_contains(response, "Merge posts")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "posts_moderation": "merge",
            "posts": [target_post.id, other_post.id],
            "moderation-edit_reason": "Test merge",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
        + f"#post-{target_post.id}"
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

    mock_posts_synchronize_categories.delay.assert_called_with(
        [user_private_thread.category_id]
    )


def test_private_thread_detail_view_merge_posts_moderation_action_merges_posts_with_attachments(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    user_private_thread,
    text_attachment,
    image_attachment,
    mock_posts_synchronize_categories,
):
    target_post = thread_reply_factory(
        user_private_thread, poster=user, original="Target body"
    )
    other_post = thread_reply_factory(
        user_private_thread, poster=user, original="Other body"
    )

    text_attachment.associate_with_post(target_post)
    text_attachment.save()

    image_attachment.associate_with_post(other_post)
    image_attachment.save()

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "merge", "posts": [target_post.id, other_post.id]},
    )
    assert_contains(response, "Merge posts")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "posts_moderation": "merge",
            "posts": [target_post.id, other_post.id],
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
        + f"#post-{target_post.id}"
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

    mock_posts_synchronize_categories.delay.assert_called_with(
        [user_private_thread.category_id]
    )


def test_private_thread_detail_view_merge_posts_moderation_action_orders_posts_from_oldest(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    user_private_thread,
    mock_posts_synchronize_categories,
):
    target_post = thread_reply_factory(
        user_private_thread, poster=user, original="Target body"
    )
    other_post = thread_reply_factory(
        user_private_thread, poster=user, original="Other body"
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "merge", "posts": [other_post.id, target_post.id]},
    )
    assert_contains(response, "Merge posts")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "posts_moderation": "merge",
            "posts": [other_post.id, target_post.id],
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
        + f"#post-{target_post.id}"
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

    mock_posts_synchronize_categories.delay.assert_called_with(
        [user_private_thread.category_id]
    )


def test_private_thread_detail_view_merge_posts_moderation_action_validates_multiple_posts_are_selected(
    thread_reply_factory,
    moderator_client,
    user,
    user_private_thread,
    mock_posts_synchronize_categories,
):
    target_post = thread_reply_factory(
        user_private_thread, poster=user, original="Target body"
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "merge", "posts": [target_post.id]},
    )
    assert_contains(response, "Select at least two posts to merge.")

    target_post.refresh_from_db()
    assert target_post.original == "Target body"

    assert not PostEdit.objects.exists()

    mock_posts_synchronize_categories.delay.assert_not_called()


def test_private_thread_detail_view_merge_posts_moderation_action_validates_posts_are_by_same_user(
    thread_reply_factory,
    moderator_client,
    user,
    other_user,
    user_private_thread,
    mock_posts_synchronize_categories,
):
    target_post = thread_reply_factory(
        user_private_thread, poster=user, original="Target body"
    )
    other_post = thread_reply_factory(
        user_private_thread, poster=other_user, original="Other body"
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "merge", "posts": [target_post.id, other_post.id]},
    )
    assert_contains(response, "Merged posts must belong to the same user.")

    target_post.refresh_from_db()
    assert target_post.original == "Target body"

    other_post.refresh_from_db()
    assert other_post.original == "Other body"

    assert not PostEdit.objects.exists()

    mock_posts_synchronize_categories.delay.assert_not_called()


def test_private_thread_detail_view_merge_posts_moderation_action_validates_posts_are_by_same_deleted_user(
    thread_reply_factory,
    moderator_client,
    user_private_thread,
    mock_posts_synchronize_categories,
):
    target_post = thread_reply_factory(
        user_private_thread, poster="John", original="Target body"
    )
    other_post = thread_reply_factory(
        user_private_thread, poster="Alice", original="Other body"
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "merge", "posts": [target_post.id, other_post.id]},
    )
    assert_contains(response, "Merged posts must belong to the same user.")

    target_post.refresh_from_db()
    assert target_post.original == "Target body"

    other_post.refresh_from_db()
    assert other_post.original == "Other body"

    assert not PostEdit.objects.exists()

    mock_posts_synchronize_categories.delay.assert_not_called()


def test_private_thread_detail_view_delete_posts_moderation_action_deletes_posts(
    thread_reply_factory,
    moderator_client,
    user_private_thread,
    mock_posts_synchronize_categories,
):
    reply = thread_reply_factory(user_private_thread)

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "delete", "posts": [reply.id]},
    )
    assert_contains(response, "Delete posts")
    assert_contains(response, "Are you sure you want to delete the selected posts?")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "posts_moderation": "delete",
            "posts": [reply.id],
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"thread_id": user_private_thread.id, "slug": user_private_thread.slug},
    )

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()

    ThreadEvent.objects.get(
        thread=user_private_thread,
        action=ThreadEventActionName.DELETED_POSTS,
    )

    mock_posts_synchronize_categories.delay.assert_called_with(
        [user_private_thread.category_id]
    )


def test_private_thread_detail_view_delete_posts_moderation_action_deletes_posts_in_htmx(
    thread_reply_factory,
    moderator_client,
    user_private_thread,
    mock_posts_synchronize_categories,
):
    reply = thread_reply_factory(user_private_thread)

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "delete", "posts": [reply.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Are you sure you want to delete the selected posts?")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
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

    ThreadEvent.objects.get(
        thread=user_private_thread,
        action=ThreadEventActionName.DELETED_POSTS,
    )

    mock_posts_synchronize_categories.delay.assert_called_with(
        [user_private_thread.category_id]
    )


def test_private_thread_detail_view_delete_posts_moderation_action_validates_first_post(
    moderator_client, user_private_thread, mock_posts_synchronize_categories
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "delete", "posts": [user_private_thread.first_post_id]},
    )
    assert_contains(response, "Thread&#x27;s first post can&#x27;t be deleted.")

    user_private_thread.first_post.refresh_from_db()

    assert not ThreadEvent.objects.exists()

    mock_posts_synchronize_categories.delay.assert_not_called()


def test_private_thread_detail_view_lock_post_moderation_action_locks_post(
    thread_reply_factory, moderator_client, moderator, user_private_thread
):
    reply = thread_reply_factory(user_private_thread)

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "lock", "post": reply.id},
    )
    assert_contains(response, "Reason for locking")
    assert_contains(response, "Lock post")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "post_moderation": "lock",
            "post": reply.id,
            "moderation-lock_reason": "Lorem ipsum",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
        + f"#post-{reply.id}"
    )

    reply.refresh_from_db()
    assert reply.is_locked
    assert reply.locked_at
    assert reply.locked_by == moderator
    assert reply.locked_by_name == moderator.username
    assert reply.locked_by_slug == moderator.slug
    assert reply.lock_reason == "Lorem ipsum"


def test_private_thread_detail_view_unlock_post_moderation_action_unlocks_post(
    thread_reply_factory, moderator_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread, is_locked=True)

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "unlock", "post": reply.id},
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
        + f"#post-{reply.id}"
    )

    reply.refresh_from_db()
    assert not reply.is_locked


def test_private_thread_detail_view_hide_post_moderation_action_hides_post(
    thread_reply_factory, moderator_client, moderator, user_private_thread
):
    reply = thread_reply_factory(user_private_thread)

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "hide", "post": reply.id},
    )
    assert_contains(response, "Reason for hiding")
    assert_contains(response, "Hide post")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "post_moderation": "hide",
            "post": reply.id,
            "moderation-hide_reason": "Lorem ipsum",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
        + f"#post-{reply.id}"
    )

    reply.refresh_from_db()
    assert reply.is_hidden
    assert reply.hidden_at
    assert reply.hidden_by == moderator
    assert reply.hidden_by_name == moderator.username
    assert reply.hidden_by_slug == moderator.slug
    assert reply.hide_reason == "Lorem ipsum"


def test_private_thread_detail_view_unhide_post_moderation_action_unhides_post(
    thread_reply_factory, moderator_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread, is_hidden=True)

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "unhide", "post": reply.id},
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
        + f"#post-{reply.id}"
    )

    reply.refresh_from_db()
    assert not reply.is_locked
    assert reply.hidden_at is None
    assert reply.hidden_by is None
    assert reply.hidden_by_name is None
    assert reply.hidden_by_slug is None
    assert reply.hide_reason is None


def test_private_thread_detail_view_approve_post_moderation_action_approves_post(
    post_factory,
    moderator_client,
    user_private_thread,
    mock_post_synchronize_categories,
    mock_post_notify_on_new_thread_reply,
):
    reply = post_factory(user_private_thread, is_unapproved=True)

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "approve", "post": reply.id},
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
        + f"#post-{reply.id}"
    )

    reply.refresh_from_db()
    assert not reply.is_unapproved

    user_private_thread.refresh_from_db()
    assert user_private_thread.last_post == reply

    mock_post_synchronize_categories.delay.assert_called_with(
        [user_private_thread.category_id]
    )
    mock_post_notify_on_new_thread_reply.delay.assert_called_with(reply.id)


def test_private_thread_detail_view_merge_post_moderation_action_merges_other_post_into_first_post(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    user_private_thread,
    mock_post_synchronize_categories,
):
    current_post = user_private_thread.first_post
    other_post = thread_reply_factory(
        user_private_thread, poster=user, original="Other body"
    )

    current_post_content = current_post.original

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_not_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:private-thread-post",
                kwargs={
                    "thread_id": user_private_thread.id,
                    "slug": user_private_thread.slug,
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
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
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

    mock_post_synchronize_categories.delay.assert_called_with(
        [user_private_thread.category_id]
    )


def test_private_thread_detail_view_merge_post_moderation_action_merges_other_post_into_first_post_in_htmx(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    user_private_thread,
    mock_post_synchronize_categories,
):
    current_post = user_private_thread.first_post
    other_post = thread_reply_factory(
        user_private_thread, poster=user, original="Other body"
    )

    current_post_content = current_post.original

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "merge", "post": current_post.id},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Other post link")
    assert_not_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:private-thread-post",
                kwargs={
                    "thread_id": user_private_thread.id,
                    "slug": user_private_thread.slug,
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

    mock_post_synchronize_categories.delay.assert_called_with(
        [user_private_thread.category_id]
    )


def test_private_thread_detail_view_merge_post_moderation_action_merges_current_post_into_other(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    user_private_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_private_thread, poster=user, original="Current body"
    )
    other_post = thread_reply_factory(
        user_private_thread, poster=user, original="Other body"
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:private-thread-post",
                kwargs={
                    "thread_id": user_private_thread.id,
                    "slug": user_private_thread.slug,
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
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
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

    mock_post_synchronize_categories.delay.assert_called_with(
        [user_private_thread.category_id]
    )


def test_private_thread_detail_view_merge_post_moderation_action_merges_current_post_into_other_in_htmx(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    user_private_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_private_thread, poster=user, original="Current body"
    )
    other_post = thread_reply_factory(
        user_private_thread, poster=user, original="Other body"
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "merge", "post": current_post.id},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:private-thread-post",
                kwargs={
                    "thread_id": user_private_thread.id,
                    "slug": user_private_thread.slug,
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

    mock_post_synchronize_categories.delay.assert_called_with(
        [user_private_thread.category_id]
    )


def test_private_thread_detail_view_merge_post_moderation_action_merges_other_post_into_current(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    user_private_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_private_thread, poster=user, original="Current body"
    )
    other_post = thread_reply_factory(
        user_private_thread, poster=user, original="Other body"
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:private-thread-post",
                kwargs={
                    "thread_id": user_private_thread.id,
                    "slug": user_private_thread.slug,
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
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
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

    mock_post_synchronize_categories.delay.assert_called_with(
        [user_private_thread.category_id]
    )


def test_private_thread_detail_view_merge_post_moderation_action_merges_other_post_into_current_in_htmx(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    user_private_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_private_thread, poster=user, original="Current body"
    )
    other_post = thread_reply_factory(
        user_private_thread, poster=user, original="Other body"
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "merge", "post": current_post.id},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:private-thread-post",
                kwargs={
                    "thread_id": user_private_thread.id,
                    "slug": user_private_thread.slug,
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

    mock_post_synchronize_categories.delay.assert_called_with(
        [user_private_thread.category_id]
    )


def test_private_thread_detail_view_merge_post_moderation_action_merges_posts_with_edit_reason(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    user_private_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_private_thread, poster=user, original="Current body"
    )
    other_post = thread_reply_factory(
        user_private_thread, poster=user, original="Other body"
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:private-thread-post",
                kwargs={
                    "thread_id": user_private_thread.id,
                    "slug": user_private_thread.slug,
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
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
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

    mock_post_synchronize_categories.delay.assert_called_with(
        [user_private_thread.category_id]
    )


def test_private_thread_detail_view_merge_post_moderation_action_merges_posts_with_attachments(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    user_private_thread,
    text_attachment,
    image_attachment,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_private_thread, poster=user, original="Current body"
    )
    other_post = thread_reply_factory(
        user_private_thread, poster=user, original="Other body"
    )

    text_attachment.associate_with_post(current_post)
    text_attachment.save()

    image_attachment.associate_with_post(other_post)
    image_attachment.save()

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:private-thread-post",
                kwargs={
                    "thread_id": user_private_thread.id,
                    "slug": user_private_thread.slug,
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
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
        + f"#post-{current_post.id}"
    )

    current_post.refresh_from_db()
    assert current_post.original == "Current body\n\nOther body"
    assert current_post.last_edit_reason == "Test merge"

    text_attachment.refresh_from_db()
    assert text_attachment.post == current_post

    image_attachment.refresh_from_db()
    assert image_attachment.post == current_post

    post_edit = PostEdit.objects.get(post=current_post)
    assert post_edit.user == moderator
    assert post_edit.edit_reason == "Test merge"
    assert post_edit.old_content == "Current body"
    assert post_edit.new_content == "Current body\n\nOther body"
    assert post_edit.attachments[0]["id"] == image_attachment.id
    assert post_edit.attachments[0]["change"] == "+"
    assert post_edit.attachments[1]["id"] == text_attachment.id
    assert post_edit.attachments[1]["change"] == "="

    with pytest.raises(Post.DoesNotExist):
        other_post.refresh_from_db()

    mock_post_synchronize_categories.delay.assert_called_with(
        [user_private_thread.category_id]
    )


def test_private_thread_detail_view_merge_post_moderation_action_merges_posts_using_global_post_link(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    user_private_thread,
    text_attachment,
    image_attachment,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_private_thread, poster=user, original="Current body"
    )
    other_post = thread_reply_factory(
        user_private_thread, poster=user, original="Other body"
    )

    text_attachment.associate_with_post(current_post)
    text_attachment.save()

    image_attachment.associate_with_post(other_post)
    image_attachment.save()

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse("misago:post", kwargs={"post_id": other_post.id}),
            "moderation-direction": "current",
            "moderation-edit_reason": "Test merge",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
        + f"#post-{current_post.id}"
    )

    current_post.refresh_from_db()
    assert current_post.original == "Current body\n\nOther body"
    assert current_post.last_edit_reason == "Test merge"

    text_attachment.refresh_from_db()
    assert text_attachment.post == current_post

    image_attachment.refresh_from_db()
    assert image_attachment.post == current_post

    post_edit = PostEdit.objects.get(post=current_post)
    assert post_edit.user == moderator
    assert post_edit.edit_reason == "Test merge"
    assert post_edit.old_content == "Current body"
    assert post_edit.new_content == "Current body\n\nOther body"
    assert post_edit.attachments[0]["id"] == image_attachment.id
    assert post_edit.attachments[0]["change"] == "+"
    assert post_edit.attachments[1]["id"] == text_attachment.id
    assert post_edit.attachments[1]["change"] == "="

    with pytest.raises(Post.DoesNotExist):
        other_post.refresh_from_db()

    mock_post_synchronize_categories.delay.assert_called_with(
        [user_private_thread.category_id]
    )


def test_private_thread_detail_view_merge_post_moderation_action_validates_other_post_link(
    thread_reply_factory,
    moderator_client,
    user,
    user_private_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_private_thread, poster=user, original="Current body"
    )
    other_post = thread_reply_factory(
        user_private_thread, poster=user, original="Other body"
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
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


def test_private_thread_detail_view_merge_post_moderation_action_validates_thread_post_link_post_exists(
    thread_reply_factory,
    moderator_client,
    user,
    user_private_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_private_thread, poster=user, original="Current body"
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:private-thread-post",
                kwargs={
                    "thread_id": user_private_thread.id,
                    "slug": user_private_thread.slug,
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


def test_private_thread_detail_view_merge_post_moderation_action_validates_thread_post_link_is_current_thread(
    thread_reply_factory,
    moderator_client,
    user,
    user_private_thread,
    other_user_private_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_private_thread, poster=user, original="Current body"
    )
    other_post = thread_reply_factory(
        other_user_private_thread, poster=user, original="Other body"
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:private-thread-post",
                kwargs={
                    "thread_id": other_user_private_thread.id,
                    "slug": other_user_private_thread.slug,
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


def test_private_thread_detail_view_merge_post_moderation_action_validates_thread_post_link_post_is_different_post(
    thread_reply_factory,
    moderator_client,
    user,
    user_private_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_private_thread, poster=user, original="Current body"
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:private-thread-post",
                kwargs={
                    "thread_id": user_private_thread.id,
                    "slug": user_private_thread.slug,
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


def test_private_thread_detail_view_merge_post_moderation_action_validates_global_post_link_post_exists(
    thread_reply_factory,
    moderator_client,
    user,
    user_private_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_private_thread, poster=user, original="Current body"
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
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


def test_private_thread_detail_view_merge_post_moderation_action_validates_global_post_link_post_permission(
    thread_reply_factory,
    moderator_client,
    user,
    private_thread,
    user_private_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_private_thread, poster=user, original="Current body"
    )
    other_post = thread_reply_factory(
        private_thread, poster=user, original="Other body"
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
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


def test_private_thread_detail_view_merge_post_moderation_action_validates_global_post_link_post_is_in_current_thread(
    thread_reply_factory,
    moderator_client,
    user,
    user_private_thread,
    other_user_private_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_private_thread, poster=user, original="Current body"
    )
    other_post = thread_reply_factory(
        other_user_private_thread, poster=user, original="Other body"
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
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


def test_private_thread_detail_view_merge_post_moderation_action_validates_global_post_link_post_is_different_post(
    thread_reply_factory,
    moderator_client,
    user,
    user_private_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_private_thread, poster=user, original="Current body"
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
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


def test_private_thread_detail_view_merge_post_moderation_action_validates_first_post_merge_into_current_post(
    thread_reply_factory,
    moderator_client,
    user,
    user_private_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_private_thread, poster=user, original="Current body"
    )
    first_post_content = user_private_thread.first_post.original

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:private-thread-post",
                kwargs={
                    "thread_id": user_private_thread.id,
                    "slug": user_private_thread.slug,
                    "post_id": user_private_thread.first_post.id,
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

    user_private_thread.first_post.refresh_from_db()
    assert user_private_thread.first_post.original == first_post_content

    mock_post_synchronize_categories.delay.assert_not_called()


def test_private_thread_detail_view_merge_post_moderation_action_validates_posts_are_by_same_user(
    thread_reply_factory,
    moderator_client,
    user,
    other_user,
    user_private_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_private_thread, poster=user, original="Current body"
    )
    other_post = thread_reply_factory(
        user_private_thread, poster=other_user, original="Other body"
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:private-thread-post",
                kwargs={
                    "thread_id": user_private_thread.id,
                    "slug": user_private_thread.slug,
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


def test_private_thread_detail_view_merge_post_moderation_action_validates_posts_are_by_same_deleted_user(
    thread_reply_factory,
    moderator_client,
    user_private_thread,
    mock_post_synchronize_categories,
):
    current_post = thread_reply_factory(
        user_private_thread, poster="Bob", original="Current body"
    )
    other_post = thread_reply_factory(
        user_private_thread, poster="Elice", original="Other body"
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "merge", "post": current_post.id},
    )
    assert_contains(response, "Merge post")
    assert_contains(response, "Other post link")
    assert_contains(response, "Merge direction")
    assert_contains(response, "Reason for merging")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "post_moderation": "merge",
            "post": current_post.id,
            "moderation-other_post": "http://testserver"
            + reverse(
                "misago:private-thread-post",
                kwargs={
                    "thread_id": user_private_thread.id,
                    "slug": user_private_thread.slug,
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


def test_private_thread_detail_view_delete_post_moderation_action_deletes_post(
    thread_reply_factory,
    moderator_client,
    user_private_thread,
    mock_post_synchronize_categories,
):
    reply = thread_reply_factory(user_private_thread)

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "delete", "post": reply.id},
    )
    assert_contains(response, "Delete post")
    assert_contains(response, "Are you sure you want to delete this post?")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "post_moderation": "delete",
            "post": reply.id,
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"thread_id": user_private_thread.id, "slug": user_private_thread.slug},
    )

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()

    ThreadEvent.objects.get(
        thread=user_private_thread,
        action=ThreadEventActionName.DELETED_POSTS,
    )

    mock_post_synchronize_categories.delay.assert_called_with(
        [user_private_thread.category_id]
    )


def test_private_thread_detail_view_delete_post_moderation_action_deletes_post_in_htmx(
    thread_reply_factory,
    moderator_client,
    user_private_thread,
    mock_post_synchronize_categories,
):
    reply = thread_reply_factory(user_private_thread)

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"post_moderation": "delete", "post": reply.id},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Are you sure you want to delete this post?")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
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

    ThreadEvent.objects.get(
        thread=user_private_thread,
        action=ThreadEventActionName.DELETED_POSTS,
    )

    mock_post_synchronize_categories.delay.assert_called_with(
        [user_private_thread.category_id]
    )
