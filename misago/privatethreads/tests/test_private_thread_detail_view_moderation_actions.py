import pytest
from django.urls import reverse

from ...test import UNORDERED, assert_contains
from ...threads.models import Thread
from ...threadupdates.enums import ThreadUpdateActionName
from ...threadupdates.models import ThreadUpdate


@pytest.fixture
def mock_synchronize_categories(mocker):
    return mocker.patch("misago.moderation.thread.synchronize_categories")


def test_private_thread_detail_view_executes_lock_thread_moderation_action(
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
        {"thread_moderation": "lock"},
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
    assert user_private_thread.is_locked
    assert user_private_thread.has_updates

    ThreadUpdate.objects.get(
        thread=user_private_thread,
        action=ThreadUpdateActionName.LOCKED,
    )


def test_private_thread_detail_view_executes_unlock_thread_moderation_action(
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
    assert user_private_thread.has_updates

    ThreadUpdate.objects.get(
        thread=user_private_thread,
        action=ThreadUpdateActionName.UNLOCKED,
    )


def test_private_thread_detail_view_executes_hide_thread_moderation_action(
    moderator_client, moderator, user_private_thread, mock_synchronize_categories
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
    assert_contains(response, "Reason for hiding")
    assert_contains(response, "Hide thread")

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
            "moderation-hidden_reason": "Lorem ipsum",
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
    assert user_private_thread.hidden_reason == "Lorem ipsum"
    assert user_private_thread.has_updates

    ThreadUpdate.objects.get(
        thread=user_private_thread,
        action=ThreadUpdateActionName.HIDDEN,
    )

    mock_synchronize_categories.delay.assert_called_once_with(
        [user_private_thread.category_id]
    )


def test_private_thread_detail_view_executes_unhide_thread_moderation_action(
    moderator_client, user_private_thread, mock_synchronize_categories
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
    assert user_private_thread.hidden_reason is None
    assert user_private_thread.has_updates

    ThreadUpdate.objects.get(
        thread=user_private_thread,
        action=ThreadUpdateActionName.UNHIDDEN,
    )

    mock_synchronize_categories.delay.assert_called_once_with(
        [user_private_thread.category_id]
    )


def test_private_thread_detail_view_executes_approve_thread_moderation_action(
    mocker,
    moderator_client,
    user,
    other_user,
    moderator,
    user_private_thread,
    mock_synchronize_categories,
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
    assert user_private_thread.has_updates

    ThreadUpdate.objects.get(
        thread=user_private_thread,
        action=ThreadUpdateActionName.APPROVED,
    )

    mock_synchronize_categories.delay.assert_called_once_with(
        [user_private_thread.category_id]
    )
    mock_notify_on_new_private_thread.delay.assert_called_once_with(
        user.id, user_private_thread.id, UNORDERED([other_user.id, moderator.id])
    )


def test_private_thread_detail_view_executes_require_reply_approval_thread_moderation_action(
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
    assert user_private_thread.has_updates

    ThreadUpdate.objects.get(
        thread=user_private_thread,
        action=ThreadUpdateActionName.REQUIRED_REPLY_APPROVAL,
    )


def test_private_thread_detail_view_executes_remove_reply_approval_thread_moderation_action(
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
    assert user_private_thread.has_updates

    ThreadUpdate.objects.get(
        thread=user_private_thread,
        action=ThreadUpdateActionName.REMOVED_REPLY_APPROVAL,
    )


def test_private_thread_detail_view_executes_delete_thread_moderation_action(
    moderator_client, user_private_thread, mock_synchronize_categories
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

    mock_synchronize_categories.delay.assert_called_once_with(
        [user_private_thread.category_id]
    )


def test_private_thread_detail_view_lock_posts_moderation_action_locks_posts(
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
        {"posts_moderation": "lock", "posts": [reply.id]},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"thread_id": user_private_thread.id, "slug": user_private_thread.slug},
    )

    reply.refresh_from_db()
    assert reply.is_locked


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
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"thread_id": user_private_thread.id, "slug": user_private_thread.slug},
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
    assert_contains(response, "Reason for hiding")
    assert_contains(response, "Hide posts")

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
            "moderation-hidden_reason": "Lorem ipsum",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"thread_id": user_private_thread.id, "slug": user_private_thread.slug},
    )

    reply.refresh_from_db()
    assert reply.is_hidden
    assert reply.hidden_at
    assert reply.hidden_by == moderator
    assert reply.hidden_by_name == moderator.username
    assert reply.hidden_by_slug == moderator.slug
    assert reply.hidden_reason == "Lorem ipsum"


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
    assert_contains(response, "Thread&#x27;s original post can&#x27;t be hidden.")


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
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"thread_id": user_private_thread.id, "slug": user_private_thread.slug},
    )

    reply.refresh_from_db()
    assert not reply.is_hidden
    assert reply.hidden_at is None
    assert reply.hidden_by is None
    assert reply.hidden_by_name is None
    assert reply.hidden_by_slug is None
    assert reply.hidden_reason is None


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


def test_private_thread_detail_view_executes_lock_post_moderation_action(
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
        {"post_moderation": "lock", "post": reply.id},
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


def test_private_thread_detail_view_executes_unlock_post_moderation_action(
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


def test_private_thread_detail_view_executes_hide_post_moderation_action(
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
            "moderation-hidden_reason": "Lorem ipsum",
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
    assert reply.hidden_reason == "Lorem ipsum"


def test_private_thread_detail_view_executes_unhide_post_moderation_action(
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
    assert reply.hidden_reason is None
